---
name: system-audit
description: "Run parallel system audits across skills, hooks, agents, rules, bibliographies, conventions, and documentation freshness. Report-only — never modifies files."
allowed-tools: Bash(ls*), Bash(readlink*), Bash(wc*), Bash(git*), Bash(test*), Bash(stat*), Bash(find*), Read, Glob, Grep, Task
argument-hint: "[no arguments — runs full sweep]"
---

# Maintenance Sweep

> System-wide health check using 4 parallel sub-agents. Produces a consolidated report at `log/system-audit-YYYY-MM-DD.md`. **Report-only — never modifies any files.**

## When to Use

- Periodic system hygiene (monthly or after major changes)
- When the user says "maintenance sweep", "system health check", "audit my setup"
- After adding/removing skills, hooks, agents, or rules
- Before presenting the system to others (ensure everything is consistent)

## Overview

1. **Dispatch** — launch 4 sub-agents in parallel via the Task tool
2. **Collect** — gather each sub-agent's findings
3. **Consolidate** — merge into a single timestamped report with summary dashboard
4. **Present** — show key findings to the user

**Python:** Always use `uv run python` or `uv pip install`. Never bare `python`, `python3`, `pip`, or `pip3`. Include this in sub-agent prompts.

---

## Phase 1: Dispatch Sub-Agents

Launch all 4 in a single message using parallel Task tool calls. Each sub-agent is `subagent_type: Explore`.

All sub-agents receive this shared context:

```
Task Management root: $TASK_MGMT_DIR/
Global Claude config: ~/.claude/
Project index: .context/projects/_index.md
Research projects root: $HOME/Library/CloudStorage/YOUR-CLOUD/Research/
Research project categories (subdirectories of the root above):
  - AI Safety & Governance/
  - Behavioural Decision Science/
  - Environmental Economics/
  - Human-AI Interaction/
  - Operations Research & Optimisation/
  - Organisation & Strategy/
  - Political Science/
Each category contains individual project directories.
```

### Sub-Agent 1: Inventory Auditor

**Prompt:**
```
Audit the Task Management system inventory. Check:

1. **Skill count:** Count directories in skills/ that contain a SKILL.md (exclude .DS_Store, shared/). Compare against documented count in CLAUDE.md, README.md, docs/system.md, docs/skills.md.
2. **Hook count:** Count .sh files in hooks/ (exclude .DS_Store). Compare against documented count in CLAUDE.md, README.md, docs/system.md, docs/hooks.md.
3. **Agent count:** Count .md files in .claude/agents/. Compare against documented count.
4. **Rule count:** Count .md files in .claude/rules/. Compare against documented count.
5. **Symlink health:** Verify these symlinks resolve correctly:
   - ~/.claude/skills/ → Task Management/skills/
   - ~/.claude/agents/ → Task Management/.claude/agents/
   - ~/.claude/rules/ → Task Management/.claude/rules/
   - ~/.claude/hooks/ → Task Management/hooks/
   - ~/.claude/settings.json → Task Management/.claude/settings.json
   - ~/.claude/CLAUDE.md → Task Management/GLOBAL-CLAUDE.md
   - ~/.claude/statusline-command.sh → Task Management/.claude/statusline-command.sh
6. **MCP server tool count:** The MCP server in .mcp-server/server.py registers tools as `skill-<name>` and `agent-<name>`. Count the cached skills and agents it discovers (read the discovery functions in server.py). Compare against actual skill/agent counts.
7. **Undocumented items:** Any skills/hooks/agents/rules that exist on disk but aren't listed in their respective docs file (docs/skills.md, docs/hooks.md, docs/agents.md, docs/rules.md).

Return findings as markdown with sections for each check, using checkmarks for pass and warnings for mismatches.
```

### Sub-Agent 2: Bibliography & Project Hygiene

**Prompt:**
```
Quick scan of bibliography files and project health across the user's research projects. Check:

1. **Find all .bib files** under the research projects root:
   $HOME/Library/CloudStorage/YOUR-CLOUD/Research/
   Categories: AI Safety & Governance, Behavioural Decision Science, Environmental Economics, Human-AI Interaction, Operations Research & Optimisation, Organisation & Strategy, Political Science.
   Search each project directory and its paper/ subdirectory (2 levels deep from category).
   Skip ZZ Topic Finder and ZZ Topic Inventory (these are tooling, not research projects).

2. For each .bib file found:
   - Count entries (grep for @article, @inproceedings, @book, @misc, etc.)
   - Check naming convention (should be paperpile.bib or <project>.bib)
   - Spot-check 3 keys for Paperpile format (AuthorYYYY-xx pattern)
   - Flag any obvious issues (empty files, very large files >500 entries)

3. **MEMORY.md presence:** For each project, check if a MEMORY.md exists in the project root. Projects that have been actively worked on should have one.

4. **Summary table:** Project | Category | Bib file | Entry count | Naming OK | MEMORY.md

Do NOT do a full validation — that's what /validate-bib is for. Just flag projects that should be audited in detail.
```

### Sub-Agent 3: Convention Compliance

**Prompt:**
```
Check convention compliance across the user's research projects. Scan each project directory under:
$HOME/Library/CloudStorage/YOUR-CLOUD/Research/
Categories: AI Safety & Governance, Behavioural Decision Science, Environmental Economics, Human-AI Interaction, Operations Research & Optimisation, Organisation & Strategy, Political Science.
Skip ZZ Topic Finder and ZZ Topic Inventory.

For each project, check:

1. **LaTeX output directory:** If .tex files exist (in project root or paper/), does an out/ directory exist? Is there a .latexmkrc file?
2. **Overleaf separation:** If a paper/ directory exists, is it a symlink? Check that paper/ contains ONLY LaTeX source files (.tex, .sty, .cls, .bst, .bbl, .bib, .latexmkrc, out/) and figures (.pdf, .png, .eps, .jpg, .svg, .tikz). Flag any code files (.py, .R, .jl, .sh, .ipynb), data files (.csv, .xlsx, .json, .dta, .parquet), or other non-LaTeX artifacts found inside paper/.
3. **Hook executability:** All .sh files in $TASK_MGMT_DIR/hooks/ should be executable (chmod +x).
4. **Python environment:** If .py files exist in the project, is there a pyproject.toml? Any sign of bare pip usage (requirements.txt without pyproject.toml, pip in scripts)?
5. **CLAUDE.md presence:** Does each project have a CLAUDE.md?
6. **Git health:** Is the project a git repo? Any uncommitted changes? Any untracked files that should probably be tracked?

Report per-project compliance as a table:
Project | Category | LaTeX/out | Overleaf sep. | Python env | CLAUDE.md | Git

Only scan top-level project directories — don't recurse deeply into subdirectories.
```

### Sub-Agent 4: Documentation Freshness

**Prompt:**
```
Check documentation freshness in the Task Management system at:
$TASK_MGMT_DIR/

Audit:

1. **Stale counts in docs:** Check these files for numeric claims about skills, hooks, agents, rules, and compare against actual counts on disk:
   - CLAUDE.md: skill count, hook count, agent count, rule count
   - README.md: same counts
   - docs/system.md: same counts, file tree accuracy
   - docs/skills.md: total skill count, category counts, skill catalogue completeness

2. **Broken internal links:** Check markdown links in CLAUDE.md, README.md, docs/system.md, docs/skills.md, docs/hooks.md, docs/agents.md, docs/rules.md — do the referenced files actually exist?

3. **Outdated statuses in .context/:**
   - current-focus.md: when was it last modified? (check file stat or git log)
   - projects/_index.md: compare project list against actual directories in the research projects root. Any projects on disk but missing from the index? Any entries in the index for projects that don't exist?

4. **Old session logs:** What's the most recent file in log/? How many logs exist? Any very old logs (>90 days) that could be archived?

5. **Plan staleness:** Any plans in log/plans/ more than 30 days old that reference incomplete work?

6. **GLOBAL-CLAUDE.md vs CLAUDE.md consistency:** Check that GLOBAL-CLAUDE.md (the slim pointer file) doesn't duplicate detailed content from CLAUDE.md. It should contain only identity, pointers, and global policies.

Return as markdown with severity levels: OK, STALE, BROKEN.
```

---

## Phase 2: Collect and Consolidate

After all 4 sub-agents return, merge their findings into a single report.

### Report Template

Write to `log/system-audit-YYYY-MM-DD.md`:

```markdown
# Maintenance Sweep — YYYY-MM-DD

## Dashboard

| Area | Status | Issues |
|------|--------|--------|
| Inventory | <OK/WARN/FAIL> | <count> |
| Bibliography & Projects | <OK/WARN/FAIL> | <count> |
| Conventions | <OK/WARN/FAIL> | <count> |
| Documentation | <OK/WARN/FAIL> | <count> |

## Inventory Audit
<Sub-agent 1 findings>

## Bibliography & Project Hygiene
<Sub-agent 2 findings>

## Convention Compliance
<Sub-agent 3 findings>

## Documentation Freshness
<Sub-agent 4 findings>

## Recommended Actions
<Prioritised list of things to fix, grouped by effort level>

### Quick Fixes (< 5 min each)
- ...

### Medium Effort (5–30 min)
- ...

### Larger Tasks (> 30 min)
- ...
```

---

## Phase 3: Present

Show the user:
1. The dashboard table
2. Any FAIL-status areas with specifics
3. The quick fixes list
4. Ask if he wants to address any issues now

---

## Error Handling

- **Sub-agent timeout:** If a sub-agent doesn't return, note "timed out" in the report and continue with the others.
- **Missing directories:** If a category folder is empty or doesn't exist, note "no projects found" rather than erroring.
- **Permission issues:** If files can't be read, note "access denied" and continue.

## Integration with Other Skills

| Skill | Relationship |
|-------|-------------|
| `/validate-bib` | Run on projects flagged by the Bibliography Hygiene sub-agent |
| `/audit-project-structure` | Complements Convention Compliance with deeper per-project checks |
| `/update-project-doc` | Fix documentation staleness found by Documentation Freshness |
| `/sync-permissions` | Fix symlink issues found by Inventory Auditor |
| `/audit-research-projects` | Full cross-system audit (local + Paperpile + pipeline) — deeper than this sweep |
| `/insights-deck` | Maintenance findings can feed into system insights presentations |
