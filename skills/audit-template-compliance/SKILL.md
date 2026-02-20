---
name: audit-template-compliance
description: "Compare a project's LaTeX preamble against the working paper template. Reports missing features, conflicts, and redundancies. Optional --apply mode syncs changes interactively."
allowed-tools: Read, Glob, Grep, Edit, Write, Bash(ls*), Bash(latexmk*), Bash(lualatex*), Bash(biber*), AskUserQuestion, Skill
argument-hint: [project-path] [--apply]
---

# Template Compliance

> Compare a research project's LaTeX preamble against the working paper template (`templates/latex-wp/your-template.sty` + `your-bib-template.sty`). Classify every difference, produce a scored report, and optionally apply changes interactively.

## When to Use

- After the template has been updated and you want to check older papers
- Before submission — verify the preamble is clean and up to date
- When a paper has mysterious compilation issues (often a stale preamble)
- During periodic maintenance or `/system-audit`
- When starting work on a paper that hasn't been touched in a while

## When NOT to Use

- **Setting up a new project** — use `/init-project-research` instead (it copies the template)
- **Fixing compilation errors** — use `/latex-autofix` first, then run this
- **Non-LaTeX projects** — this skill is LaTeX-specific

---

## Critical Rules

1. **Never edit without `--apply`.** Default mode is report-only. Without `--apply`, the skill produces a report and exits.
2. **Never auto-apply Conflict items.** Conflicts always require explicit user confirmation via `AskUserQuestion`.
3. **Semantic comparison, not line-by-line.** Compare packages, options, commands, and environments as logical units — not raw text diffs.
4. **Preserve project-specific additions.** Items classified as **Keep** are informational. Never suggest removing them unless they conflict with a template feature.
5. **Template is the reference, not the authority.** Projects may legitimately diverge. The skill reports differences — the user decides what to act on.
6. **Compile after applying.** If `--apply` makes any changes, always verify with `/latex-autofix`.

---

## Protocol

### Phase 1: Locate & Parse

1. **Resolve the project path.** Accept as argument or use CWD. Resolve to absolute path.
2. **Find the project's preamble files.** The canonical location is the **Overleaf document**, accessed via the `paper/` symlink in the project directory. Search in this order:
   - **New format (`.sty` files):** `paper/your-template.sty` + `paper/your-bib-template.sty` (Overleaf symlink — **preferred**)
   - **Legacy format:** `paper/settings.tex` (Overleaf symlink)
   - If no `paper/` symlink exists, check for an Overleaf folder directly: `~/Library/CloudStorage/YOUR-CLOUD/Apps/Overleaf/<Paper Name>/your-template.sty` (or `settings.tex`)
   - Project root: `your-template.sty` + `your-bib-template.sty` or `settings.tex` (for local-only projects without Overleaf)
   - Any `\input{settings}` or `\usepackage{your-template}` in `main.tex` pointing elsewhere

   **NEVER** check settings/style files in subdirectories like `docs/`, `to-sort/`, `docs/venues/`, or any non-paper location. Only the main paper's preamble is relevant.

   If no preamble files are found, report error and exit.

3. **Read the template.** Search in this order:
   - `~/Library/CloudStorage/YOUR-CLOUD/Apps/Overleaf/Template/your-template.sty` + `your-bib-template.sty` (Overleaf source)
   - `~/Library/CloudStorage/YOUR-CLOUD/Task Management/templates/latex-wp/your-template.sty` + `your-bib-template.sty` (local copy — identical)
   - Legacy fallback: `settings.tex` in either location

   If no template files are found, report "Template not found — cannot compare. Verify that the Overleaf Template folder exists or the local copy in `templates/latex-wp/`." and exit.

4. **Parse both files into semantic blocks:**

   | Block | What to extract |
   |-------|----------------|
   | **Packages** | Package name + options (e.g., `[dvipsnames]{xcolor}`) |
   | **Hyperref** | All `\hypersetup{}` key-value pairs + `\urlstyle` |
   | **Bibliography** | System (biblatex/natbib), all options, `\addbibresource`, source mappings, field clearing (`\AtEveryBibitem`), possessive citation commands |
   | **Custom commands** | All `\newcommand`, `\renewcommand`, `\DeclareMathOperator`, `\newcolumntype` |
   | **Theorem environments** | All `\newtheorem` declarations with their styles and counters |
   | **Build config** | `.latexmkrc` content (engine, output dir, PDF copy-back) |

   For packages, normalise options: `\usepackage[a,b]{pkg}` and `\usepackage[b,a]{pkg}` are equivalent.

---

### Phase 2: Compare

For each semantic block, compare the project against the template:

#### Packages

| Check | Detail |
|-------|--------|
| Missing packages | In template but not in project |
| Extra packages | In project but not in template |
| Option differences | Same package loaded with different options |
| Load order | Flag if `hyperref` or `cleveref` are loaded out of order (hyperref must come before cleveref) |
| Duplicate loads | Same package loaded twice in the project |

**Package groups to check explicitly:**

- Core math: `mathtools`, `amssymb`, `amsmath`, `amsfonts`, `amsthm`
- Tables: `booktabs`, `longtable`, `multirow`, `tabularx`, `threeparttable`, `threeparttablex`
- Typography: `microtype`, `setspace`, `fontspec`, `unicode-math`
- Figures: `graphicx`, `subcaption`, `tikz`, `pgfplots`
- Utilities: `etoolbox`, `comment`, `enumitem`, `csquotes`
- Layout: `geometry`, `fancyhdr`, `titlesec`, `pdflscape`, `pdfpages`
- xcolor with `dvipsnames` option

#### Hyperref

| Check | Detail |
|-------|--------|
| Missing keys | Template keys not in project's `\hypersetup` |
| Different values | Same key, different value (e.g., `linkcolor=blue` vs `linkcolor=black`) |
| Missing `\urlstyle{same}` | Template uses it; project should too |
| `cleveref` loaded after `hyperref` | Required ordering |

#### Bibliography

| Check | Detail |
|-------|--------|
| System mismatch | biblatex vs natbib — this is a **Conflict**, never auto-resolved |
| Option differences | Missing or different biblatex options |
| Missing source mappings | Template's Paperpile cleanup maps not in project |
| Missing field clearing | Template's `\AtEveryBibitem` rules not in project |
| Missing possessive citations | `\posscite`, `\Posscite`, `\posscites` commands |
| `\addbibresource` present | Must exist if using biblatex |

#### Custom Commands

| Check | Detail |
|-------|--------|
| Missing commands | Template commands not defined in project |
| Different definitions | Same command name, different body |
| Missing column types | `L`, `C`, `R` column types |
| Missing math commands | `\R`, `\N`, `\E`, `\Prob`, `\indicator` |
| Missing operators | `\argmin`, `\argmax` |

#### Theorem Environments

| Check | Detail |
|-------|--------|
| Missing environments | Template theorems not in project |
| Different styles | Same environment, different `\theoremstyle` |
| Different counters | Same environment, different counter relationship |
| Missing `\numberwithin` | Template uses `\numberwithin{equation}{section}` |

#### Build Config

| Check | Detail |
|-------|--------|
| `.latexmkrc` exists | In project root or paper directory |
| Engine match | Template uses `lualatex` via `$pdf_mode = 4` |
| Output directory | Template uses `$out_dir = 'out'` |
| PDF copy-back | Template has `END { system("cp ...") }` |

---

### Phase 3: Classify

Label every difference from Phase 2 with one of four categories:

| Label | Meaning | Action in `--apply` mode |
|-------|---------|--------------------------|
| **Adopt** | Template feature missing from project. Safe to add. | Apply automatically (with confirmation summary) |
| **Keep** | Project-specific addition not in template. Legitimate. | No action — informational only |
| **Conflict** | Same functionality loaded differently. Needs human judgement. | Always ask user via `AskUserQuestion` |
| **Drop** | Redundant or superseded by a template equivalent. | Apply automatically (with confirmation summary) |

#### Classification Rules

**Adopt** when:
- Package is in template but entirely absent from project
- Template command/environment is missing from project
- Template hyperref key is missing from project
- `.latexmkrc` is missing
- `dvipsnames` option is missing from xcolor

**Keep** when:
- Project loads a package not in the template (project-specific need)
- Project defines commands not in the template
- Project defines extra theorem environments
- Project has extra hyperref settings

**Conflict** when:
- biblatex vs natbib (different bibliography systems)
- Same package with incompatible options
- Same command name with different definitions
- Different `\theoremstyle` for the same environment name
- Different geometry margins

**Drop** when:
- Project loads a package that the template supersedes (e.g., `palatino` when template uses `fontspec`)
- Project defines a command identically to the template (true duplicate)
- Project loads a package twice

---

### Phase 4: Check Auxiliaries

Beyond the preamble files, check consistency of related files:

#### main.tex

| Check | Detail |
|-------|--------|
| Preamble loading present | `\usepackage{your-template}` + `\usepackage{your-bib-template}` (new format) or `\input{settings}` (legacy) |
| `\documentclass` matches | Template uses `[12pt,a4paper]{article}` |
| `\printbibliography` present | Required if using biblatex |
| No `\bibliography{}` | Should not appear if using biblatex |
| No `\bibliographystyle{}` | Should not appear if using biblatex |

#### .latexmkrc

| Check | Detail |
|-------|--------|
| Exists | In project root or paper directory |
| Engine | Template: `lualatex` via `$pdf_mode = 4` |
| Output dir | Template: `$out_dir = 'out'` |
| PDF copy-back | `END { system("cp $out_dir/*.pdf . 2>/dev/null") }` |

---

### Phase 5: Report

Produce a structured compliance report. Full format: [`references/report-format.md`](references/report-format.md)

#### Quality Score

Start at **100** and deduct per issue:

| Severity | Deduction | Examples |
|----------|-----------|----------|
| **Major** | -5 | Missing `.latexmkrc`, natbib vs biblatex conflict, missing `hyperref`, missing `cleveref`, `hyperref`/`cleveref` load order wrong |
| **Moderate** | -2 | Missing common packages (booktabs, microtype, enumitem), missing `dvipsnames`, duplicate package loads, missing custom commands (\todo, \red, \blue), missing source mappings, missing field clearing |
| **Minor** | -1 | Missing optional packages, different hyperref colours, missing theorem environments, missing math operators, missing `\numberwithin` |

#### Score Interpretation

| Score | Label |
|-------|-------|
| 90-100 | Excellent — fully aligned |
| 75-89 | Good — minor gaps only |
| 50-74 | Needs attention — several missing features |
| < 50 | Significant drift — consider full resync |

#### Report Sections

1. **Header**: Project name, path, score, date
2. **Summary table**: Counts by classification (Adopt / Keep / Conflict / Drop)
3. **Per-item detail**: Grouped by semantic block, showing classification + what/why
4. **Auxiliaries**: main.tex and .latexmkrc checks
5. **Recommendations**: Prioritised list of suggested actions

If `--apply` is not set, end with:
```
Run `/audit-template-compliance <path> --apply` to interactively apply changes.
```

---

### Phase 6: Apply (--apply mode only)

Apply changes in dependency order to avoid compilation breakage:

1. **Package options** (e.g., add `dvipsnames` to xcolor)
2. **Missing packages** (insert in correct position relative to existing packages)
3. **Hyperref configuration** (update `\hypersetup{}` block)
4. **Bibliography changes** (only if user approves — always `AskUserQuestion` for system changes)
5. **Custom commands** (append after existing commands section)
6. **Theorem environments** (append after existing theorem section)
7. **`.latexmkrc`** (create or update)
8. **Cleanup** (remove duplicates, drop redundancies)

#### Apply Rules

- **Show a summary first.** Before making any edits, present the full list of changes to be applied (Adopt + Drop items) and ask for confirmation.
- **Conflicts are always individual.** Each Conflict item gets its own `AskUserQuestion` with the template version, project version, and context.
- **Keep items are never touched.** They appear in the report but are skipped during apply.
- **Preserve comments and whitespace.** When inserting packages, match the project's existing formatting style (e.g., if packages are grouped with comment headers, add to the right group).
- **Log what was changed.** After applying, list every edit made.

---

### Phase 7: Verify (--apply mode only)

After applying changes:

1. **Compile with `/latex-autofix`.** This handles any secondary issues the changes might introduce.
2. **Report the result:**
   - If compilation succeeds: report success + number of changes applied
   - If compilation fails: report the error, suggest reverting specific changes, and note which change likely caused the issue

---

## What This Skill Does NOT Do

- **Does not rewrite `main.tex` structure.** Only checks `\input{settings}` and bibliography commands.
- **Does not check content quality.** Use `/proofread` for that.
- **Does not manage `.bib` files.** Use `/validate-bib` for bibliography key issues.
- **Does not handle journal-specific formatting.** Use `/retarget-journal` for that.
- **Does not compare across projects.** Checks one project at a time against the template.

---

## Examples

### Report only (default)

> "/audit-template-compliance ~/papers/costly-voice"

Produces a compliance report without making any changes.

### Apply mode

> "/audit-template-compliance ~/papers/costly-voice --apply"

Produces the report, then interactively applies Adopt and Drop changes with user confirmation.

### Current directory

> "Check my template compliance"

Runs on the current working directory in report-only mode.

### After template update

> "I updated the template — check all my papers"

Run on each project individually. This skill checks one project at a time.

---

## Cross-References

- **`templates/latex-wp/your-template.sty`** + **`your-bib-template.sty`** — the canonical template this skill compares against
- **`/latex-autofix`** — used in Phase 7 to verify compilation after applying changes
- **`/audit-project-structure`** — complementary: checks directory structure, this checks LaTeX preamble
- **`/validate-bib`** — complementary: checks citation keys, this checks bibliography system config
- **`/init-project-research`** — creates projects from the template; this skill verifies ongoing compliance
- **`/retarget-journal`** — handles journal-specific formatting (different concern)
