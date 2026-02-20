---
name: audit-project-structure
description: "Audit a research project's structure against the current init-project-research template. Reports missing directories, files, symlinks, and seed content. Report-only — never modifies the project."
allowed-tools: Bash(ls*), Bash(readlink*), Bash(git*), Read, Glob, Grep
argument-hint: [project-path]
---

# Check Project Structure

> Compare a research project's directory structure against the current `/init-project-research` template and report gaps. **Report-only — never creates, moves, or deletes anything.**

## When to Use

- After revisiting a project set up a while ago
- When the template has been updated and you want to check older projects
- Before submission — verify nothing is missing
- When a project "feels messy" and you want a structured audit

## When NOT to Use

- **Setting up a new project** — use `/init-project-research`
- **Fixing issues** — this skill only reports; user decides what to act on

## Critical Rules

1. **Never modify the project.** Read-only audit.
2. **Detect project type before checking.** Don't flag missing `code/` in theoretical projects.
3. **Distinguish "missing" from "intentionally absent."** Flag but don't alarm.
4. **Check content quality, not just existence.** Empty CLAUDE.md is worth flagging.

---

## Phase 1: Identify Project

1. Resolve to absolute path (argument or CWD)
2. Determine project name from basename (Title Case convention; flag kebab-case as Info)
3. Check if git repo: `git -C "<path>" rev-parse --is-inside-work-tree 2>/dev/null`
4. Detect project type:

| Indicator | Implies |
|-----------|---------|
| `code/` or `data/` | Experimental |
| `src/` or `tests/` | Computational |
| Only `paper/`, `docs/`, `log/` | Theoretical |
| Mix of above | Mixed |

5. Read CLAUDE.md if it exists — extract declared metadata (type, venue, authors)

---

## Phase 2: Check Common Core

Check for every element of the common core scaffold. Record: present / missing / degraded.

#### Directories

| Directory | Check |
|-----------|-------|
| `.context/` | Exists |
| `.claude/` | Exists |
| `docs/` | Exists |
| `docs/literature-review/` | Exists |
| `docs/readings/` | Exists |
| `docs/venues/` | Exists |
| `log/` | Exists |
| `paper/` | Exists (may be symlink) |
| `to-sort/` | Exists |

#### Files

| File | Check |
|------|-------|
| `CLAUDE.md` | Exists and non-empty |
| `README.md` | Exists and non-empty |
| `MEMORY.md` | Exists with research template (notation, estimands, decisions) |
| `.gitignore` | Exists and non-empty |
| `.context/current-focus.md` | Exists and non-empty |
| `.context/project-recap.md` | Exists |
| `.claude/settings.local.json` | Exists |

#### Symlinks

If `paper/` is a real directory (not symlink), flag as informational.

---

## Phase 3: Check Conditional Structure

Based on detected project type:

**Experimental:** `code/`, `code/python/` or `code/R/`, `data/`, `data/raw/`, `data/processed/`, `output/`, `output/figures/`, `output/tables/`

**Computational:** `src/`, `tests/`, `experiments/`, `results/`, `pyproject.toml`, `.python-version`

**Python tooling (all types with .py files):** Flag `requirements.txt` as Degraded. Flag bare `pip`/`python` in docs as Degraded.

**Theoretical:** No additional checks.

**Mixed:** Check whichever elements are present, flag incomplete sets.

---

## Phase 3.5–3.7: Extended Checks

Detailed specifications for growth patterns, pre-template detection, remediation suggestions, and Overleaf separation checks: [references/check-details.md](references/check-details.md).

**Phase 3.5 — Post-Init Growth:** Classify items as recognized growth (Info) or unrecognized (Info — review).

**Phase 3.6 — Pre-Template Detection:** If no `.context/` AND no `.claude/`, flag as pre-template project with consolidated remediation commands.

**Phase 3.7 — Overleaf Separation:** Scan `paper/` for forbidden file types (code, data, package files, runtime artifacts). Hard rule — violations are Missing, not Info. Check for required `.latexmkrc`.

---

## Phase 4: Check Seed Content Quality

Beyond existence — verify meaningful content.

#### CLAUDE.md

| Section | What to look for |
|---------|-----------------|
| Project Overview | Title, authors, venue, type |
| Research Questions | At least one RQ |
| Setup / Overleaf | Symlink path documented |
| Folder Structure | Tree or description |
| Conventions | Compilation convention + uv Python rule |
| Session Continuity | Mentions current-focus.md or log/ |

Flag placeholder text (`<title>`, `TODO`, `TBD`). Check bloat per `lean-claude-md` rule (>200 lines, >15-line reference sections, duplicated content).

#### README.md

Title, authors, abstract/description, status checklist.

#### .gitignore

Must include: `.DS_Store`, `__pycache__/`, `out/`, `paper/` (if Overleaf-managed).

#### .context/current-focus.md

Should be updated beyond "Project just initialised" if commits exist beyond the initial one.

---

## Phase 5: Check Git Health

If **not** a git repo: flag as Missing (local git is default since Feb 2026).

If git repo:

| Check | What to look for |
|-------|-----------------|
| Branch name | `main` or `master`? (template uses `main`) |
| Untracked files | Should be gitignored? |
| Remote | Informational only |
| Nested repos | `.git/` in subdirectories — flag as Missing |

---

## Phase 6: Report

Three severity levels:

| Level | Meaning |
|-------|---------|
| **Missing** | Expected by template, not present |
| **Degraded** | Present but incomplete or has issues |
| **Info** | May be intentional — no action needed unless it bothers you |

Full report format with severity markers and remediation lines: [references/report-format.md](references/report-format.md)

---

## What This Skill Does NOT Do

- Does not create or fix anything — report-only
- Does not check file content beyond seed files
- Does not compare against other projects
- Does not enforce uniformity — identifies unintentional gaps

## Cross-References

- `/init-project-research` — the template this skill audits against
- `/project-safety` — safety rules and folder guardrails
- `/update-project-doc` — fixes stale documentation (run after this audit)
