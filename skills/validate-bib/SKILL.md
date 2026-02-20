---
name: validate-bib
description: "Cross-reference \\cite{} keys against .bib files or embedded \\bibitem entries. Finds missing, unused, and typo'd citation keys. Read-only — never edits files."
allowed-tools: Read, Glob, Grep
argument-hint: [project-path or tex-file]
---

# Bibliography Validation

**Read-only skill.** Never edit source files — produce a categorised report only.

**Citation key rule:** the user's existing keys always take precedence. They come from Paperpile (his reference management system) and are canonical. When suggesting replacements (typo corrections, preprint upgrades, metadata fixes), always keep the user's key and update the `.bib` entry metadata around it — never suggest renaming a key to match some "standard" format.

## When to Use

- Before compiling a final version of a paper
- After adding new citations to check nothing was missed
- When `biber`/`bibtex` reports undefined citations
- As part of a pre-submission checklist (pair with `/proofread`)

## When NOT to Use

- **Finding new references** — use `/literature` for discovery
- **Building a bibliography from scratch** — use `/literature` with `.bib` generation
- **General proofreading** — use `/proofread` (which also flags citation format issues)

## Phase 0: Session Log (Suggested)

Bibliography validation with preprint staleness checks can be context-heavy (OpenAlex lookups, web searches for published versions). Before starting, **suggest** running `/session-log` to capture prior work as a recovery checkpoint. If the user declines, proceed without it.

## Convention

**Default bibliography file is `paperpile.bib`** — this is the standard across all projects (per the `/latex` skill convention). However, the skill also supports:

- Any `.bib` file found in the same directory as the `.tex` files being audited
- Embedded bibliographies using `\begin{thebibliography}` / `\bibitem{key}` blocks
- Both external and embedded simultaneously (rare but possible)

## Bibliography Detection

At the start of validation, detect which bibliography method the project uses:

### 1. External `.bib` file (standard)

Look for `.bib` files in the project directory. Priority order:
1. `paperpile.bib` (preferred — standard naming convention across all projects)
2. Any other `.bib` file in the same directory as the `.tex` files

If **multiple `.bib` files** are found, validate all of them and produce a combined report. Note which file each issue belongs to. If `paperpile.bib` exists alongside other `.bib` files, flag the extras as a potential cleanup opportunity (the project may have migrated from a different naming convention).

Full validation applies: cross-reference checks **and** quality checks.

### 2. Embedded `\begin{thebibliography}` / `\bibitem{key}`

Some LaTeX documents define references inline rather than using an external `.bib` file. Detect by scanning `.tex` files for `\begin{thebibliography}`.

Extract keys from `\bibitem` entries:
- `\bibitem{key}` — standard form, key is the argument in braces
- `\bibitem[label]{key}` — optional label form (e.g., `\bibitem[Smith et al., 2020]{smith2020}`), key is in the **second** set of braces

Only **cross-reference checks** apply (missing keys, unused keys, typos). Quality checks (required fields, year, author formatting) are **skipped** because embedded bibliographies don't have structured metadata.

### 3. Both (rare)

If a project has both a `.bib` file and `\begin{thebibliography}` blocks, validate both:
- Run full validation on the `.bib` file
- Run cross-reference checks on `\bibitem` entries
- Merge both key sets when checking for missing citations

## Workflow

1. **Find files**: Locate all `.tex` files in the project
2. **Detect bibliography type**: Check for `.bib` files and/or `\begin{thebibliography}` blocks
3. **Extract citation keys from .tex**: Scan for all citation commands
4. **Extract entry keys from bibliography source(s)**:
   - External: Parse all `@type{key,` entries from `.bib` file(s)
   - Embedded: Parse all `\bibitem{key}` and `\bibitem[label]{key}` entries
5. **Cross-reference**: Compare the two sets
6. **Quality checks**: Validate `.bib` entry completeness (external only)
7. **Produce report**: Write results to stdout (or save if requested)

## Citation Commands to Scan

Scan `.tex` files for all of these patterns:

| Command | Example |
|---------|---------|
| `\cite{key}` | Basic citation |
| `\citet{key}` | Textual: Author (Year) |
| `\citep{key}` | Parenthetical: (Author, Year) |
| `\textcite{key}` | biblatex textual |
| `\autocite{key}` | biblatex auto |
| `\parencite{key}` | biblatex parenthetical |
| `\citeauthor{key}` | Author name only |
| `\citeyear{key}` | Year only |
| `\nocite{key}` | Include in bibliography without in-text citation |

Also handle **multi-key citations**: `\citep{key1, key2, key3}`

## Cross-Reference Checks

### Critical: Missing Entries

Citation keys used in `.tex` but not defined in the bibliography source (`.bib` file or `\bibitem` entries).

These will cause compilation errors.

### Warning: Unused Entries

Keys defined in the bibliography source but never cited in any `.tex` file.

Not errors, but may indicate:
- Forgotten citations (should they be `\nocite`?)
- Leftover entries from earlier drafts
- Entries intended for a different paper

### Warning: Possible Typos (Fuzzy Match)

For each missing key, check if a similar key exists in the bibliography using edit distance:
- Edit distance = 1: Very likely a typo
- Edit distance = 2: Possibly a typo
- Flag these with the suggested correction

Common typo patterns:
- Year off by one: `smith2020` vs `smith2021`
- Missing/extra letter: `santanna` vs `sant'anna` vs `santana`
- Underscore vs camelCase: `smith_jones` vs `smithjones`

## Quality Checks on .bib Entries

**These checks apply only to external `.bib` files.** Embedded bibliographies lack structured metadata, so quality checks are skipped for them.

### Required Fields by Entry Type

| Entry Type | Required Fields |
|-----------|----------------|
| `@article` | author, title, journal, year |
| `@book` | author/editor, title, publisher, year |
| `@incollection` | author, title, booktitle, publisher, year |
| `@inproceedings` | author, title, booktitle, year |
| `@techreport` | author, title, institution, year |
| `@unpublished` | author, title, note, year |
| `@phdthesis` | author, title, school, year |

### Year Reasonableness

- Flag entries with year < 1900 or year > current year + 1
- Flag entries with no year at all

### Author Formatting

- Check for inconsistent author formats within the file
- **Flag entries where author field contains "and others" or "et al."** — this is never valid in BibTeX. All authors must be listed explicitly. Severity: **Warning**.
- Flag entries with organisation names that might need `{{braces}}` to prevent splitting

### DOI Resolution (optional — triggered by `--verify-dois` flag or when issues are suspected)

When enabled, resolve each DOI in the `.bib` file by fetching `https://doi.org/[DOI]` and confirm the returned metadata matches the entry:

1. **Title match**: Does the DOI landing page title match the `.bib` title?
2. **Author match**: Does the first author on the landing page match the `.bib` first author?
3. **Journal match**: Does the venue match?

Flag mismatches as:
- **Warning: DOI mismatch** — DOI resolves to a different paper than claimed. This usually means the DOI is wrong (adjacent DOI in the same journal volume) or the authors are wrong (conflation of researchers in the same subfield).

This check catches:
- Wrong DOIs (e.g., off-by-one in the DOI suffix)
- Author conflation (real researchers incorrectly attributed to a paper)
- Metadata copied from secondary sources without verification

Use WebFetch to resolve DOIs. Process in batches of 5 to avoid rate limiting. Only flag confirmed mismatches — if the DOI cannot be resolved (404, timeout), note it as "unresolvable" at Info level.

### Preprint Staleness Check

**For every entry that looks like a preprint**, check whether a peer-reviewed version has since been published.

#### Detection — identify preprint entries by any of:

| Signal | Examples |
|--------|----------|
| URL/DOI contains preprint host | `arxiv.org`, `ssrn.com`, `nber.org`, `repec.org`, `econpapers`, `ideas.repec` |
| Journal/howpublished field | "arXiv preprint", "SSRN", "NBER Working Paper", "Working Paper", "mimeo" |
| Entry type | `@techreport`, `@unpublished`, `@misc` with working-paper-like metadata |
| Note field | Contains "preprint", "working paper", "wp", "discussion paper" |

#### Lookup — find the published version:

1. **OpenAlex first** (preferred — structured data, no rate limits):
   ```python
   # Search by title to find published version
   results = client.search_works(search="<paper title>", per_page=5)
   # Check if any result has a journal/venue and is not itself a preprint
   ```
2. **DOI resolution fallback**: If the preprint has a DOI, check if it redirects to or links to a published version.
3. **Web search last resort**: Search for the paper title + "published" or "journal" if OpenAlex returns nothing.

#### Classification:

| Finding | Severity | Message |
|---------|----------|---------|
| Published version exists | **Warning** | "Preprint `key` appears published in *Journal Name* (Year). Consider updating the .bib entry." |
| Published version exists with different title/authors | **Warning** | "Preprint `key` may have been published as '*new title*' in *Journal*. Verify and update." |
| No published version found | **Info** | "Preprint `key` — no published version found (checked YYYY-MM-DD)." |

#### Report section:

Add a `## Warning: Stale Preprints` section to the report listing all preprints where a published version was found, with the suggested replacement metadata (journal, year, DOI).

## Severity Levels

| Level | Meaning |
|-------|---------|
| **Critical** | Missing entry for a cited key — will cause compilation error |
| **Warning** | Unused entry, possible typo, missing required field |
| **Info** | Year oddity, formatting suggestion, bibliography type note |

## Bibliography Output

After validation, offer these actions if applicable:

- **Embedded bibliography → offer to create `paperpile.bib`**: If the project uses `\begin{thebibliography}`, offer to extract the references into a proper `paperpile.bib` file (one `@misc` entry per `\bibitem`, with the full text as a `note` field). The author can then enrich the entries with proper metadata.
- **Non-standard `.bib` name → offer to rename**: If the existing `.bib` file is not named `paperpile.bib`, offer to rename it to `paperpile.bib` and update the `\bibliography{}` command in the `.tex` file.

These are **offers only** — do not make changes without explicit confirmation.

## Report Format

```markdown
# Bibliography Validation Report

**Project:** [path]
**Date:** YYYY-MM-DD
**Files scanned:** [list of .tex files]
**Bibliography type:** External .bib / Embedded / Both
**Bibliography:** [filename] ([N] entries) | Embedded ([N] \bibitem entries) | Both ([N] .bib + [N] \bibitem)
**Citations found:** [N] unique keys across [N] citation commands

## Summary

| Check | Count |
|-------|-------|
| Missing entries (Critical) | 0 |
| Possible typos (Warning) | 0 |
| Unused entries (Warning) | 0 |
| Missing required fields (Warning) | 0 |
| DOI mismatches (Warning) | 0 |
| Stale preprints (Warning) | 0 |
| Year issues (Info) | 0 |

## Critical: Missing Entries

| Cited Key | File | Line | Suggested Match |
|-----------|------|------|-----------------|
| `smith2020` | main.tex | 42 | `smith2021` (edit dist: 1) |

## Warning: Possible Typos

[Keys with close fuzzy matches]

## Warning: Unused Entries

[Keys in bibliography not cited anywhere — listed for review]

## Warning: Missing Required Fields

*External .bib only — skipped for embedded bibliographies.*

| Key | Type | Missing Fields |
|-----|------|---------------|
| `jones2019` | article | journal |

## Warning: Stale Preprints

| Key | Current Source | Published In | Year | DOI |
|-----|---------------|--------------|------|-----|
| `smith2020arxiv` | arXiv:2020.12345 | *J. of ML Research* | 2022 | 10.xxxx/yyyy |

## Info: Year Issues

[Entries with suspicious years]

## Limitations

*If embedded:* Embedded bibliographies (`\bibitem`) lack structured metadata (author, year, journal as separate fields). Only cross-reference checks were performed. Quality checks (required fields, year reasonableness, author formatting) require an external `.bib` file.
```

## Optional: OpenAlex Metadata Verification

**Python:** Always use `uv run python`. Never bare `python`, `python3`, `pip`, or `pip3`.

When missing entries or suspicious metadata are found, the shared OpenAlex client can verify citation details (DOI, correct year, journal name, author list):

```bash
uv run python -c "
import sys
sys.path.insert(0, '.scripts/openalex')
from openalex_client import OpenAlexClient

client = OpenAlexClient(email='user@example.edu')

# Look up a specific DOI
result = client.get_entity('works', 'doi:10.1016/j.ejor.2024.01.001')

# Search by title to find the correct entry
results = client.search_works(search='decision making under uncertainty', per_page=5)
"
```

Use this when:
- A cited key is missing and you want to confirm whether the paper exists
- Year or author formatting looks suspicious and you want to cross-check
- The user asks to enrich `.bib` entries with verified metadata

Do NOT use this by default — only when the report flags issues worth verifying.

## Cross-References

- **`/proofread`** — For overall paper quality including citation format
- **`/literature`** — For finding and adding new references (includes full OpenAlex workflows)
- **`/latex`** — For compilation with reference checking
- **`/paper-writing`** — After drafting sections with citations, run `/validate-bib` to catch missing/typo'd keys before compilation
