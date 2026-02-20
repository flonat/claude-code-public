# Claude Code for Academic Research

> This file is automatically read when you open this folder with Claude Code.
> Customise it with your own details — see comments marked with `<!-- CUSTOMISE -->`.

## Before You Start

Read these context files to understand the user's situation:

1. `.context/profile.md` — Who you are, your roles, research areas
2. `.context/current-focus.md` — What you're working on NOW
3. `.context/projects/_index.md` — Overview of all projects

## Key Information

<!-- CUSTOMISE: Replace with your own details -->

**Who I am:**
- PhD researcher
- Multiple active research projects
- Teaching responsibilities

**Research areas:**
- Behavioural science
- Decision making
- Experimental methods

**How I work:**
- Flexible/reactive style
- Prefer questions over lists
- Daily reviews work better than weekly
- Full context in task descriptions

## Conventions

### LaTeX Compilation
- **Default method:** Use `/latex-autofix` — it compiles, auto-fixes errors, and runs a citation audit.
- Build artifacts go to `out/`, but the PDF is copied back to the source directory.
- Use `.latexmkrc` with `$out_dir = 'out'` and an `END {}` block to copy the PDF back.
- Never leave build artifacts (`.aux`, `.log`, etc.) in the source directory.

### Python & Package Management
- Always use `uv` to run Python. Never use bare `python` or `pip`.
- Use `uv run python ...` or `uv pip install ...` for all Python operations.

### R
- Use `<-` for assignment, not `=`.

### Git & Remote
- Many repos are local-only, synced via Dropbox. Do NOT assume a remote exists.
- Before pushing, check if a remote is configured with `git remote -v`.

### Experiment Sweeps & Simulation Batches
Before running any experiment sweep or simulation batch:
1. Write sanity-check assertions first.
2. Implement the code.
3. Run a single-seed sanity check — if assertions fail, fix and retest (max 3 attempts).
4. Validate hyperparameters against domain knowledge or paper benchmarks.
5. Only then proceed to full experiments.

### Output Formats
- Academic papers: LaTeX.
- Documents for human use (consent forms, PILs, etc.): `.docx` via `pandoc`.

### Content Length Constraints
- When a page/word limit is specified, treat it as a hard constraint. Draft to 80%, then expand — never exceed and trim.
- Always report the actual page/word count after drafting.

## Notion Integration

<!-- CUSTOMISE: Add your Notion database IDs if using Notion -->

If you use Notion for task management, configure these database IDs:

| Database | ID |
|----------|-----|
| Tasks Tracker | `YOUR-TASKS-DATABASE-ID-HERE` |
| Research Pipeline | `YOUR-PIPELINE-DATABASE-ID-HERE` |

**API usage:** Always fetch the database schema first to get correct property names before making any create/update calls.

## Workflows

Detailed instructions in `.context/workflows/`:
- `daily-review.md` — How to help with daily planning
- `meeting-actions.md` — How to extract action items
- `weekly-review.md` — Weekly reflection template
- `replication-protocol.md` — 4-phase protocol for replicating paper results

## Skills Available

31 skills in `skills/` folder. See [`docs/skills.md`](docs/skills.md) for the full catalogue.

## Agents

6 agents in `.claude/agents/`. See [`docs/agents.md`](docs/agents.md) for when to use each.

## Rules (9 Auto-Loaded)

In `.claude/rules/` — these apply automatically to every session. See [`docs/rules.md`](docs/rules.md) for documentation.

| Rule | Purpose |
|------|---------|
| `plan-first.md` | Draft and save a plan before multi-file changes |
| `scope-discipline.md` | Only make changes explicitly requested |
| `learn-tags.md` | Record corrections as `[LEARN:category]` tags in `MEMORY.md` |
| `read-docs-first.md` | Check project docs before searching |
| `lean-claude-md.md` | Keep CLAUDE.md files lean — pointer pattern |
| `overleaf-separation.md` | No code or data in `paper/` directories |
| `ignore-agents-md.md` | Never read or process `AGENTS.md` files |
| `ignore-gemini-md.md` | Never read or process `GEMINI.md` files |
| `design-before-results.md` | Lock research design before examining point estimates |

## Hooks

8 hook scripts in `hooks/`. See [`docs/hooks.md`](docs/hooks.md) for the full table.

## After Every Session

**Update `.context/current-focus.md`** with:
- What we worked on
- Where things were left off
- What's coming next

## Tips for Working Together

1. **Just ask naturally** — Claude reads the context files and figures it out
2. **Point to specific files** if Claude seems confused
3. **Update current-focus.md** — This is your working memory between sessions
4. **Don't re-explain everything** — The context library has it all

## File Structure

| Path | What lives there |
|------|-----------------|
| `.context/` | AI context library (profile, focus, projects, workflows, preferences) |
| `.claude/agents/` | Agent definitions (6 agents) |
| `.claude/rules/` | Auto-loaded rules (9 rules) |
| `skills/` | 30 skill definitions |
| `hooks/` | 8 hook scripts |
| `.mcp-server-openalex/` | OpenAlex scholarly search MCP server |
| `log/` | Session logs |
| `docs/` | Documentation |
