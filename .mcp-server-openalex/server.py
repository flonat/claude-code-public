#!/usr/bin/env python3
"""
OpenAlex MCP Server

Exposes OpenAlex scholarly search as native MCP tools.
Imports the shared OpenAlex client from .scripts/openalex/ — single source of truth.
"""

import asyncio
import sys
from pathlib import Path

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

# Import existing OpenAlex client and helpers
SCRIPTS_DIR = str(
    Path(__file__).parent.parent / ".scripts" / "openalex"
)
sys.path.insert(0, SCRIPTS_DIR)

from openalex_client import OpenAlexClient  # noqa: E402
from query_helpers import (  # noqa: E402
    find_author_works,
    analyze_research_output,
    get_publication_trends,
)

from formatters import (  # noqa: E402
    format_works_table,
    format_author_profile,
    format_trends,
    format_work_detail,
)


def log(msg):
    print(f"[openalex-mcp] {msg}", file=sys.stderr, flush=True)


# Shared client instance (polite pool)
client = OpenAlexClient(email="user@example.com")

server = Server("openalex")
log("Server initialized")


# ---------- Tool definitions ----------

TOOLS = [
    Tool(
        name="openalex_search_works",
        description=(
            "Search OpenAlex for scholarly papers by topic. Supports filters for "
            "year range, minimum citations, open access, and sort order. "
            "Returns a markdown table of results."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search query (topic, keywords, title fragment)",
                },
                "year": {
                    "type": "string",
                    "description": "Year filter: e.g. '2023', '>2020', '2020-2024'",
                },
                "min_citations": {
                    "type": "integer",
                    "description": "Minimum citation count",
                },
                "open_access": {
                    "type": "boolean",
                    "description": "Only return open access papers",
                },
                "sort": {
                    "type": "string",
                    "description": "Sort order: 'cited_by_count:desc' (default), 'publication_date:desc', 'relevance_score:desc'",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results (default 25, max 50)",
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="openalex_author_works",
        description=(
            "Find publications by a specific author. Searches by name, "
            "resolves to OpenAlex author ID, returns their works."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "author_name": {
                    "type": "string",
                    "description": "Author name to search for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results (default 50, max 100)",
                },
            },
            "required": ["author_name"],
        },
    ),
    Tool(
        name="openalex_author_profile",
        description=(
            "Analyze an author's research output: total works, open access %, "
            "publications by year, and top topics."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "author_name": {
                    "type": "string",
                    "description": "Author name to analyze",
                },
                "years": {
                    "type": "string",
                    "description": "Year filter (default: '>2020')",
                },
            },
            "required": ["author_name"],
        },
    ),
    Tool(
        name="openalex_institution_output",
        description=(
            "Analyze an institution's research output: total works, open access %, "
            "publications by year, and top topics."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "institution_name": {
                    "type": "string",
                    "description": "Institution name to analyze",
                },
                "years": {
                    "type": "string",
                    "description": "Year filter (default: '>2020')",
                },
            },
            "required": ["institution_name"],
        },
    ),
    Tool(
        name="openalex_trends",
        description=(
            "Get publication count trends over time for a search term. "
            "Returns yearly publication counts."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Search term to track trends for",
                },
            },
            "required": ["query"],
        },
    ),
    Tool(
        name="openalex_lookup_doi",
        description=(
            "Look up a work by DOI. Returns full metadata including title, "
            "authors, abstract, citations, and open access status."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "doi": {
                    "type": "string",
                    "description": "DOI (with or without https://doi.org/ prefix)",
                },
            },
            "required": ["doi"],
        },
    ),
    Tool(
        name="openalex_citing_works",
        description=(
            "Find papers that cite a given work (forward citation tracking). "
            "Provide a DOI and get back the citing papers."
        ),
        inputSchema={
            "type": "object",
            "properties": {
                "doi": {
                    "type": "string",
                    "description": "DOI of the work to find citations for",
                },
                "limit": {
                    "type": "integer",
                    "description": "Max results (default 25, max 50)",
                },
            },
            "required": ["doi"],
        },
    ),
]


@server.list_tools()
async def list_tools() -> list[Tool]:
    return TOOLS


# ---------- Tool handlers ----------


@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    log(f"call_tool: {name} {arguments}")

    try:
        if name == "openalex_search_works":
            return await _handle_search_works(arguments)
        elif name == "openalex_author_works":
            return await _handle_author_works(arguments)
        elif name == "openalex_author_profile":
            return await _handle_author_profile(arguments)
        elif name == "openalex_institution_output":
            return await _handle_institution_output(arguments)
        elif name == "openalex_trends":
            return await _handle_trends(arguments)
        elif name == "openalex_lookup_doi":
            return await _handle_lookup_doi(arguments)
        elif name == "openalex_citing_works":
            return await _handle_citing_works(arguments)
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    except Exception as e:
        log(f"Error in {name}: {e}")
        return [TextContent(type="text", text=f"**Error:** {e}")]


async def _handle_search_works(args: dict) -> list[TextContent]:
    query = args["query"]
    limit = min(args.get("limit", 25), 50)
    sort = args.get("sort", "cited_by_count:desc")

    filter_params: dict[str, str] = {}
    if args.get("year"):
        filter_params["publication_year"] = args["year"]
    if args.get("min_citations"):
        filter_params["cited_by_count"] = f">{args['min_citations']}"
    if args.get("open_access"):
        filter_params["is_oa"] = "true"

    def _search():
        return client.search_works(
            search=query,
            filter_params=filter_params if filter_params else None,
            per_page=limit,
            sort=sort,
        )

    response = await asyncio.to_thread(_search)
    works = response.get("results", [])
    total = response.get("meta", {}).get("count", 0)

    text = format_works_table(works, title=f"Search: {query}")
    text += f"\n\n*{total:,} total results in OpenAlex (showing top {len(works)})*"
    return [TextContent(type="text", text=text)]


async def _handle_author_works(args: dict) -> list[TextContent]:
    author_name = args["author_name"]
    limit = min(args.get("limit", 50), 100)

    works = await asyncio.to_thread(find_author_works, author_name, client, limit)
    text = format_works_table(works, title=f"Works by {author_name}")
    return [TextContent(type="text", text=text)]


async def _handle_author_profile(args: dict) -> list[TextContent]:
    author_name = args["author_name"]
    years = args.get("years", ">2020")

    analysis = await asyncio.to_thread(
        analyze_research_output, "author", author_name, client, years
    )
    text = format_author_profile(analysis)
    return [TextContent(type="text", text=text)]


async def _handle_institution_output(args: dict) -> list[TextContent]:
    institution_name = args["institution_name"]
    years = args.get("years", ">2020")

    analysis = await asyncio.to_thread(
        analyze_research_output, "institution", institution_name, client, years
    )
    text = format_author_profile(analysis)
    return [TextContent(type="text", text=text)]


async def _handle_trends(args: dict) -> list[TextContent]:
    query = args["query"]

    trends = await asyncio.to_thread(get_publication_trends, query, None, client)
    text = format_trends(trends, search_term=query)
    return [TextContent(type="text", text=text)]


async def _handle_lookup_doi(args: dict) -> list[TextContent]:
    doi = args["doi"]
    if not doi.startswith("https://doi.org/"):
        doi = f"https://doi.org/{doi}"

    work = await asyncio.to_thread(client.get_entity, "works", doi)
    text = format_work_detail(work)
    return [TextContent(type="text", text=text)]


async def _handle_citing_works(args: dict) -> list[TextContent]:
    doi = args["doi"]
    limit = min(args.get("limit", 25), 50)

    if not doi.startswith("https://doi.org/"):
        doi = f"https://doi.org/{doi}"

    work = await asyncio.to_thread(client.get_entity, "works", doi)
    cited_by_url = work.get("cited_by_api_url")

    if not cited_by_url:
        return [TextContent(type="text", text="No citation data available for this work.")]

    import requests

    def _fetch_citing():
        resp = requests.get(
            cited_by_url,
            params={"mailto": client.email, "per-page": limit},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()

    data = await asyncio.to_thread(_fetch_citing)
    citing_works = data.get("results", [])
    total = data.get("meta", {}).get("count", 0)

    title_text = (work.get("title") or "this work")[:60]
    text = format_works_table(citing_works, title=f"Papers citing: {title_text}")
    text += f"\n\n*{total:,} total citing works (showing {len(citing_works)})*"
    return [TextContent(type="text", text=text)]


# ---------- Main ----------

async def main():
    log("Starting MCP server...")
    async with stdio_server() as (read_stream, write_stream):
        log("stdio_server ready, running server...")
        await server.run(
            read_stream, write_stream, server.create_initialization_options()
        )
    log("Server stopped")


if __name__ == "__main__":
    log("Main entry point")
    asyncio.run(main())
