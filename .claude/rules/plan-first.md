# Rule: Plan Before Implementing

## When This Applies

- Multi-file edits (touching 3+ files)
- New features or significant additions
- Unclear or ambiguous scope
- Refactoring existing code or structure

## When to Skip

- Single-file fixes (typos, one-line bugs)
- Running existing skills (`/proofread`, `/validate-bib`, etc.)
- Informational questions ("What does this function do?")
- Updating context files (`.context/current-focus.md`)

## Quick Mode

When the task is clearly experimental or exploratory, skip the full planning protocol.

**Triggers** (any of these):
- the user says "quick", "try this", "experiment", "prototype", "just see if"
- Task is a single-file script exploration or simulation test
- the user explicitly says "skip planning"

**What changes:**
- Skip plan-first (no plan file, no approval step)
- Orchestrator still runs but threshold drops to 60/100 (vs 80/90 normally)
- Must-haves: code runs, results are correct, goal documented in a comment at the top
- Not needed: docs, tests, perfect style, session log

**What stays:** Verification (code must run), learn tags, all safety rules.

**Kill switch:** the user can say "stop" or "abandon" at any point — no guilt, no cleanup needed.

**Escalation:** If the exploration succeeds and the user wants to build on it, normal plan-first + orchestrator rules resume.

## Protocol

1. **Draft a plan** before writing any code or making changes
2. **Save the plan** to `log/plans/YYYY-MM-DD_description.md`
3. **Get approval** — present the plan to the user and wait for confirmation
4. **Implement via orchestrator** — see `orchestrator-protocol.md` for the verify/review/fix/score loop. For tasks where the orchestrator doesn't apply (see its "When to Skip"), implement directly, noting any deviations.

### Plan Format

```markdown
# Plan: [Short Description]

## Context
[Why this is needed]

## Changes
[List of files to create/modify with brief descriptions]

## Order of Operations
1. Write session log (`/session-log`)
2. Update project context (`/update-focus` or `/save-context`)
3. [Implementation steps...]

## Risks / Open Questions
[Anything that could go wrong or needs clarification]
```

## Phase Boundaries

When a plan spans 2+ distinct activities (e.g., code + experiments + writing), split into phases with explicit stop points:

1. Each phase gets its own session (or section of a session)
2. At each phase boundary, create `HANDOFF.md` in the project root summarising:
   - What was accomplished
   - What outputs exist and where
   - What the next phase should use
3. Run `/session-log` at each boundary, not just at session end
4. Do NOT start the next phase without the user's go-ahead

Signs a plan needs phases: 5+ implementation steps, multiple distinct tool chains (Python + LaTeX), or estimated context usage that could hit compression.

## Session Recovery

When starting a new session or after context compression:

1. Read the most recent file in `log/plans/`
2. Read the most recent file in `log/`
3. Read `.context/current-focus.md`

This provides enough context to continue without re-explaining.

## Important

- **Never `/clear`** — rely on auto-compression to manage context
- Plans are living documents — update them if scope changes mid-implementation
- Quick plans (3-5 lines) are fine for medium tasks; full format for large ones
