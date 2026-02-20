---
name: literature
description: "Academic literature discovery, synthesis, and bibliography management. Find papers, verify citations, create .bib files, download PDFs, and synthesize literature narratives. Includes OpenAlex API integration for structured scholarly queries."
allowed-tools: Bash(curl*), Bash(wget*), Bash(mkdir*), Bash(ls*), Read, Write, Edit, WebSearch, WebFetch, Task
argument-hint: [topic-or-paper-query]
---

# Literature Skill

**CRITICAL RULE: Every citation must be verified to exist before inclusion.** Never include a paper you cannot find via web search. Hallucinated citations are worse than no citations.

**Python:** Always use `uv run python`. Never bare `python`, `python3`, `pip`, or `pip3`.

**PREPRINT RULE: Always prefer the published version.** If a paper is found on arXiv, SSRN, NBER, or any working paper series, search for a published journal/conference version. Only cite a preprint if no published version can be found.

> Comprehensive academic literature workflow: discover, verify, organize, synthesize.
> Uses parallel sub-agents to search multiple sources, verify citations, and fetch PDFs concurrently.

## When to Use

- Starting a new research project
- Writing a literature review section
- Building a reading list on a topic
- Finding specific citations
- Creating annotated bibliographies

---

## Architecture: Orchestrator + Sub-Agents

```
You (orchestrator)
├── Phase 0: Session log & compact (mandatory — /session-log)
├── Phase 1: Pre-search check (direct — no sub-agent)
├── Phase 2: Parallel search (2-3 Explore agents)
├── Phase 3: Deduplicate + rank (direct — no sub-agent)
├── Phase 4: Parallel verification (general-purpose agents, batches of 5)
├── Phase 5: Parallel PDF download (Bash agents)
├── Phase 6: Assemble .bib (direct — no sub-agent)
└── Phase 7: Synthesize narrative (direct — no sub-agent)
```

**Key principle:** Sub-agents handle independent, parallelizable work. Merging, deduplication, and synthesis stay with you because they need the full picture.

**Full agent prompt templates for all phases:** [references/agent-templates.md](references/agent-templates.md)

---

## Phase 0: Session Log & Compact (Mandatory)

Literature searches are context-heavy. **Always** run `/session-log` before starting to create a recovery checkpoint.

---

## Phase 1: Pre-Search Check (Direct)

Check for existing `.bib` files in project root, `/references`, `/bib`, `/bibliography`:

1. Parse existing entries to avoid duplicates and understand context
2. Identify gaps — note if bibliography skews toward certain years/methods
3. Compile list of existing citation keys to pass to sub-agents

---

## Phase 2: Parallel Search (Sub-Agents)

Spawn **2-3 Explore agents in parallel** in a single message, one per source. Read the full prompt templates from [references/agent-templates.md](references/agent-templates.md#phase-2-search-agent-templates).

Available search agents:
1. **Google Scholar** — broad academic search
2. **Semantic Scholar / arXiv** — CS/ML focused
3. **OpenAlex** (optional) — structured metadata, citation counts, DOIs
4. **Domain-specific** (optional) — SSRN, NBER, specific journals

OpenAlex returns verified DOIs and citation counts, reducing verification work in Phase 4.

---

## Phase 3: Deduplicate and Rank (Direct)

1. **Merge** results from all search agents
2. **Remove duplicates** — match on title similarity and DOI
3. **Rank** by relevance, citation count, and recency
4. **Select top N** to verify (typically 25-30 candidates for 20-25 verified)
5. **Assign batches** of ~5 for verification

---

## Phase 4: Parallel Verification (Sub-Agents)

Spawn **multiple general-purpose agents in parallel**, each verifying ~5 papers. Read the full verification template from [references/agent-templates.md](references/agent-templates.md#phase-4-verification-agent-template).

Key rules enforced by the template:
- DOI verification is mandatory (resolve and confirm)
- ALL authors must be listed (never "et al." in metadata)
- Preprint check: always search for published version
- Results: VERIFIED / NOT FOUND / METADATA MISMATCH

After all return: collect VERIFIED, drop NOT FOUND, check for remaining duplicates.

---

## Phase 5: Parallel PDF Download (Sub-Agents)

Spawn Bash agents in parallel, 3-5 papers each. Read template from [references/agent-templates.md](references/agent-templates.md#phase-5-pdf-download-agent-template). Best-effort — many papers are behind paywalls.

---

## Phase 6: Assemble Bibliography (Direct)

**Two outputs required:**

1. **`docs/literature-review/literature_summary.bib`** — always created, standalone, self-contained
2. **Project canonical bib** (e.g. `paper/paperpile.bib`) — merge into it if it exists

### BibTeX Format

```bibtex
@article{AuthorYear,
  author    = {Last, First and Last, First},
  title     = {Full Title},
  journal   = {Journal Name},
  year      = {2024},
  volume    = {XX},
  pages     = {1--20},
  doi       = {10.1000/example},
  abstract  = {Abstract text here.}
}
```

Rules:
- Citation keys: `AuthorYear` format. Conflicts: append `a`, `b`, etc.
- Only VERIFIED papers — no METADATA MISMATCH entries
- **List ALL authors explicitly** — never "et al." in BibTeX
- Include abstracts when available

---

## Phase 7: Synthesize Narrative (Direct)

1. **Identify themes** — group papers by approach, finding, or debate
2. **Map intellectual lineage** — how did thinking evolve?
3. **Note current debates** — where do researchers disagree?
4. **Find gaps** — what's missing?

Output types: narrative summary (LaTeX), literature deck, annotated bibliography.

---

## Output Structure

```
project/
├── docs/
│   ├── literature-review/
│   │   ├── literature_summary.md      # Thematic narrative (always)
│   │   └── literature_summary.bib     # Standalone .bib (always)
│   └── readings/
│       ├── Smith2024.pdf              # Downloaded PDFs
│       └── ...
└── paper/
    └── paperpile.bib                  # Canonical bib (merge if exists)
```

---

## Sub-Agent Guidelines

0. **Python: ALWAYS use `uv run python`.** Include this in every sub-agent prompt.
1. **Launch independent agents in a single message** for parallelism
2. **Be explicit in prompts** — sub-agents have no context
3. **Include skip lists** of existing citation keys
4. **Batch sizes:** 5 papers per verification agent, 3-5 per PDF agent
5. **Maximum 3 parallel agents at a time** — spawn in waves, write results to disk between waves
6. **Right agent type:** `Explore` for search, `general-purpose` for verification, `Bash` for downloads
7. **Tolerate partial failures** — continue with what you have

---

## OpenAlex Structured Queries

**Setup:** `.scripts/openalex/openalex_client.py` + `.scripts/openalex/query_helpers.py`

| Workflow | What it does |
|----------|-------------|
| Highly-cited papers | Top-cited papers on a topic (filtered by year) |
| Author output | Full publication record for a researcher |
| Institution output | Research output analysis for a university |
| Publication trends | Year-by-year counts for a topic |
| Open-access discovery | Find freely downloadable versions |
| Citation network | Forward citations for a given paper |
| Batch DOI lookup | Verify metadata for multiple papers |

**Full recipes:** [references/openalex-workflows.md](references/openalex-workflows.md)

**MCP server:** `.mcp-server-openalex/` wraps the same client — 7 tools callable directly.

---

## Cross-References

| Skill | When to use instead/alongside |
|-------|-------------------------------|
| `/research-ideation` | Generate research questions first |
| `/interview-me` | Develop a specific idea before searching |
| `/validate-bib` | Cross-check citation keys after assembling `.bib` |
| `/split-pdf` | Deep-read a paper found during search |
