---
name: update-project-doc
description: "Update a project's own documentation (CLAUDE.md, README.md, docs/*.md) to reflect its current state. Detects stale file trees, timestamps, counts, and next steps."
allowed-tools: Read, Edit, Write, Glob, Grep, Bash(ls*), Bash(git log*), Bash(git diff*), Bash(readlink*), Bash(wc*), Bash(date*), AskUserQuestion
argument-hint: (no arguments)
---

# Update Project Doc — Refresh Stale Documentation

> Scan a project's documentation files and update sections that have drifted from reality: file trees, timestamps, bibliography counts, next steps, skill/hook tallies, and more.

## When to Use

- After significant project work (new files, completed milestones, structural changes)
- During `/session-close` when offered
- When the user says "update project docs", "refresh docs", "sync my docs", "update my README"
- Periodically to keep documentation accurate

## What It Does NOT Do

- Never rewrites research content (hypotheses, arguments, literature, design decisions)
- Never deletes sections — only updates factual/structural content within existing sections
- Never creates new documentation files — only updates existing ones

---

## Protocol

### Step 1: Detect Documentation Files

Find all documentation files in the project:

1. Check for `CLAUDE.md` in project root
2. Check for `README.md` in project root
3. Scan `docs/` and `docs/*/` for `.md` files containing file trees or counts
4. Note which files exist — only update what's present

**Special case:** Some projects (e.g., the political information paper) have no `CLAUDE.md` because they use a committed `README.md` as their primary project documentation instead. This is intentional for repos meant to be shared or published. In these cases, treat `README.md` as the main documentation file and apply all the same checks to it.

Read each detected file to understand its current content.

### Step 2: Gather Current State

Collect the actual state of the project:

1. **File tree** — use `ls -R` or `Glob` to build the actual directory structure (respect `.gitignore` patterns, skip `out/`, `__pycache__/`, `.venv/`, `node_modules/`)
2. **Recent git history** — `git log --oneline -20` for recent commits
3. **Session logs** — read the latest 1-2 files in `log/` (if the directory exists)
4. **Bibliography count** — count entries in any `.bib` file(s): `grep -c '@' *.bib`
5. **Symlink targets** — `readlink` on any documented symlinks
6. **Context files** — read `.context/current-focus.md` or `.context/project-recap.md` if present

**Task Management only** (detected by presence of `skills/` directory):
7. **Skill count** — count directories in `skills/` that contain `SKILL.md`
8. **Hook count** — count `.sh` files in `hooks/` (if present)
9. **Skill lengths** — `wc -l skills/*/SKILL.md` to identify bloated skills

**CLAUDE.md leanness** (all projects with a CLAUDE.md):
9. **Line count** — `wc -l CLAUDE.md`
10. **Section sizes** — count lines per `##` section, identify any with >15 lines of reference material
11. **Duplication scan** — check if CLAUDE.md content duplicates what's already in README.md, docs/, or .context/ files

### Step 3: Run Staleness Checks

Compare gathered state against documented content. Flag any mismatches:

| Check | How to Detect |
|-------|--------------|
| **File tree** | Generate actual tree, compare against any tree/structure block in docs (look for ``` blocks or indented listings with file paths) |
| **Timestamps** | Flag "Last updated", "w/c", or date stamps older than 7 days |
| **Bibliography count** | Compare actual `.bib` entry count vs any documented count (e.g., "42 references") |
| **Next steps / roadmap** | Cross-reference items against recent commits and session logs — flag items that appear completed |
| **Manuscript status** | Flag sections marked "TODO", "incomplete", or "placeholder" that now have content |
| **Symlinks** | Verify documented symlink targets still resolve with `readlink` |
| **Skill/hook counts** | (Task Management only) Compare actual count vs documented numbers in CLAUDE.md, README.md, and `.tex` files |
| **Venue/target info** | If CLAUDE.md documents a target journal, check it matches `.context/projects/_index.md` (if accessible) |
| **CLAUDE.md leanness** | Count lines in CLAUDE.md. Flag if >200 lines total. Scan each `##` section: flag any with >15 lines of reference material (not safety rules or conventions) that could be extracted to `docs/` with a pointer. Check for content duplicated from other project files. See `lean-claude-md` rule. |
| **SKILL.md lengths** | (Task Management only) Flag any `SKILL.md` over 300 lines — reference material (templates, examples, report formats) should be in `references/` or `templates/` subdirectories with a pointer in the SKILL.md. See `skills/shared/` for cross-skill content. |
| **README.md length** | Flag if `README.md` exceeds 300 lines. Suggest extracting long sections to `docs/`. |

### Step 4: Propose Changes

Present findings grouped by file:

```
Staleness report for [Project Name]:

CLAUDE.md:
  - File structure tree is outdated (missing: X, Y; removed: Z)
  - Skill count says 23, actual is 26
  - "Last updated" date is 3 weeks old

README.md:
  - Directory structure block needs updating
  - Next steps: "Write introduction" appears completed (commit abc1234)
  - Bibliography count says 38, actual is 42

docs/overview.md:
  - No issues detected
```

If nothing is stale, report that and stop.

### Step 5: Ask for Confirmation

Use `AskUserQuestion` to let the user approve, modify, or skip each group:

- **Apply all** — update everything proposed
- **Select by file** — choose which files to update
- **Skip** — make no changes

### Step 6: Apply and Report

For each approved change:

1. Use **targeted `Edit` operations** — never rewrite entire files
2. Preserve all surrounding content
3. When updating file trees, match the existing formatting style (├──, |--, indented, etc.)
4. When updating counts, find the exact number and replace it
5. When marking next-step items as done, use strikethrough (~~item~~) rather than deleting

After all edits, print a summary:

```
Updated project docs:
  CLAUDE.md:  file tree, skill count (23 → 26)
  README.md:  directory structure, bib count (38 → 42), 1 next-step marked complete
  Total: 5 edits across 2 files
```

---

## Key Rules

1. **Targeted edits only** — never rewrite entire files. Use `Edit` with precise `old_string` / `new_string`.
2. **Preserve research content** — hypotheses, questions, literature reviews, design decisions, and arguments are sacred. Only update factual/structural sections.
3. **Always show before applying** — never make silent edits. The proposal step is mandatory.
4. **Match existing style** — if the project uses `├──` trees, don't switch to `|--`. If counts use "X total", don't change to "X skills".
5. **Works in any project** — not just Task Management. Adapt checks to what's present.
6. **Idempotent** — running twice in a row should produce no changes the second time.

## Cross-References

- `/session-close` — offers to run this skill at Step 3.5
- `/update-focus` — updates `current-focus.md` (different purpose: session state, not doc accuracy)
