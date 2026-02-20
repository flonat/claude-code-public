# Audit Check Details

> Detailed check specifications for `/audit-project-structure`. The SKILL.md has pointers here — read this when executing the relevant phase.

---

## Phase 3.5: Recognized Growth Patterns

Projects naturally grow beyond the initial scaffold. These are documented in `/init-project-research` as expected additions:

| Pattern | Recognized as |
|---------|---------------|
| `experiments/` | Experiment configs, sweep logs, results |
| `experiments/configs/` | Parameter sweep definitions |
| `scripts/` | Utility scripts (data processing, plotting) |
| `legacy/` | Preserved old code/data (per `/project-safety`) |
| `docs/venues/<venue>/revision-N/` | Reviewer comments and response materials per R&R round |
| `docs/venues/<venue>/camera-ready/` | Final accepted version |
| `notes.md` | Quick research notes, meeting summaries |
| `SETUP.md` | Environment setup instructions |
| `pyproject.toml` | Python package management |
| `.venv/` | Virtual environment |

When a recognized pattern is found, report it as **Info** — present and expected.

### Unrecognized items

Any top-level directory or file that is **not** part of the common core, conditional structure, or recognized growth patterns should be flagged as **Info — unrecognized** for user review. Do not flag hidden files/directories that are standard (`.git/`, `.DS_Store`, etc.).

---

## Phase 3.6: Pre-Template Detection & Remediation

### Pre-template project detection

If the project has **no `.context/`** AND **no `.claude/`**, flag it as a **pre-template project** and add a consolidated note:

```
Pre-template project detected
===============================
This project predates the current init-project-research template.
To bring it into the framework, consider adding:

  1. mkdir -p .context && touch .context/current-focus.md .context/project-recap.md
  2. mkdir -p .claude && copy settings.local.json from another project
  3. Create a CLAUDE.md (see /init-project-research Phase 3 for template)
  4. mkdir to-sort && touch to-sort/.gitkeep
  5. Run /sync-permissions to set up symlinks

Or run /init-project-research in "retrofit" mode if available.
```

### Remediation suggestions

For each missing common core item, include a one-line remediation suggestion:

| Missing item | Suggestion |
|-------------|------------|
| `.context/` | `mkdir -p .context && touch .context/current-focus.md .context/project-recap.md` |
| `.gitignore` | Copy template from `/init-project-research` Phase 3 |
| `.claude/settings.local.json` | Run `/sync-permissions` to create |
| `to-sort/` | `mkdir to-sort && touch to-sort/.gitkeep` |
| `CLAUDE.md` | See `/init-project-research` Phase 3 for template |
| `README.md` | See `/init-project-research` Phase 3 for template |
| `docs/` | `mkdir -p docs/{literature-review,readings}` |
| `docs/literature-review/` | `mkdir -p docs/literature-review && touch docs/literature-review/.gitkeep` — `/literature` outputs go here |
| `docs/venues/` | `mkdir -p docs/venues && touch docs/venues/.gitkeep` |
| `log/` | `mkdir log && touch log/.gitkeep` |
| `MEMORY.md` | Seed from `/init-project-research` Phase 3 template (research or teaching variant) |

---

## Phase 3.7: Overleaf Separation Check

If `paper/` exists (symlink or directory), scan it for files that violate the Overleaf separation rule. **This is a hard rule — any violations are flagged as Missing (not Info).**

### Forbidden file types in `paper/`

| Pattern | Category |
|---------|----------|
| `*.py`, `*.R`, `*.jl`, `*.m`, `*.sh`, `*.ipynb`, `*.do` | Code |
| `*.csv`, `*.xlsx`, `*.json` (non-LaTeX), `*.dta`, `*.parquet`, `*.rds`, `*.pkl`, `*.feather`, `*.h5` | Data |
| `requirements.txt`, `pyproject.toml`, `renv.lock` | Package management |
| `.venv/`, `__pycache__/`, `node_modules/` | Runtime artifacts |

### Allowed in `paper/`

- `.tex`, `.sty`, `.cls`, `.bst`, `.bbl`, `.bib`
- `.pdf`, `.png`, `.eps`, `.jpg`, `.svg`, `.tikz` (figures)
- `.latexmkrc`, `latexmkrc`
- `out/` (build directory)
- `.gitignore`, `README.md` (if Overleaf-generated)

### Required in `paper/`

| File | Check | Severity |
|------|-------|----------|
| `.latexmkrc` | Must exist — needed for `out/` build convention and local compilation | **Missing** if absent |

The `.latexmkrc` should contain at minimum `$out_dir = 'out';` and an `END {}` block to copy the PDF back. If it exists but is missing `$out_dir`, flag as **Degraded**.

### How to check

```bash
# Recursively find forbidden file types inside paper/
find "<project-path>/paper/" -type f \( \
  -name "*.py" -o -name "*.R" -o -name "*.jl" -o -name "*.m" \
  -o -name "*.sh" -o -name "*.ipynb" -o -name "*.do" \
  -o -name "*.csv" -o -name "*.xlsx" -o -name "*.dta" \
  -o -name "*.parquet" -o -name "*.rds" -o -name "*.pkl" \
  -o -name "*.feather" -o -name "*.h5" \
  -o -name "requirements.txt" -o -name "pyproject.toml" \
  -o -name "renv.lock" \
\) 2>/dev/null
```

Also check for directories that should never exist inside `paper/`:
```bash
find "<project-path>/paper/" -type d \( \
  -name ".venv" -o -name "__pycache__" -o -name "node_modules" \
  -o -name "renv" \
\) 2>/dev/null
```

### Report format

For each violation found:

```
✗ Overleaf separation violation: paper/<path-to-file>
  Category: Code / Data / Package management / Runtime artifact
  Remediation: Move to <suggested-project-directory>
```

Suggested destinations follow the rule in `.claude/rules/overleaf-separation.md`:
- Code files → `code/` or `src/`
- Data files → `data/raw/` or `data/processed/`
- Package files → project root
- Notebooks → `code/` or `experiments/`
