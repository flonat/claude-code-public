---
name: learn
description: "Extract reusable knowledge from the current session into a persistent skill.\nUse when you discover something non-obvious, create a workaround, or develop\na multi-step workflow that future sessions would benefit from."
allowed_tools:
  - Read
  - Write
  - Edit
  - Glob
  - Grep
  - AskUserQuestion
---

# Learn: Session Knowledge Extraction

Extract reusable workflows, workarounds, and multi-step procedures discovered during a session into persistent skills. Complementary to the `learn-tags` rule — while `[LEARN]` tags record one-liner corrections in MEMORY.md, `/learn` creates full skill definitions in `skills/`.

## When to Use

- You discovered a non-obvious multi-step procedure
- You built a workaround for a recurring problem
- You developed a workflow that future sessions would benefit from
- the user says "save this as a skill", "learn this", or "remember how to do this"

## Phase 1: Evaluate

Before creating anything, answer these 4 self-assessment questions:

1. **Non-obvious?** Would a future session figure this out without help, or would it waste time rediscovering it?
2. **Future benefit?** Will this come up again across sessions or projects?
3. **Repeatable?** Is this a procedure that can be followed step-by-step, or was it a one-off?
4. **Multi-step?** Does it involve 2+ non-trivial steps that benefit from being documented together?

**Decision rule:** If at least 3 of 4 answers are "yes", proceed to Phase 2. Otherwise, suggest recording as a `[LEARN]` tag in MEMORY.md instead (simpler, lower overhead).

If borderline, ask the user:
> "This seems useful but may not warrant a full skill. Should I create a skill or just add a [LEARN] tag to MEMORY.md?"

## Phase 2: Check Existing Skills

Search for potential duplicates or overlaps:

1. Read `skills/` directory listing
2. For each candidate match, read the SKILL.md to check scope
3. If overlap exists:
   - **Subset:** Don't create — suggest adding to the existing skill
   - **Partial overlap:** Ask the user whether to extend the existing skill or create a new one
   - **No overlap:** Proceed to Phase 3

## Phase 3: Create the Skill

Write `skills/{name}/SKILL.md` with this structure:

```yaml
---
name: {kebab-case-name}
description: "{One-line description of when to use this skill}"
allowed_tools:
  - {minimum set of tools needed}
---
```

Then the markdown body:

```markdown
# {Skill Name}: {Short Description}

## Problem

[What situation triggers this skill — be specific about the symptoms or context]

## Trigger Conditions

[When should Claude invoke this? Natural language triggers and /command triggers]

- "..." — natural language examples
- `/{name}` — slash command

## Solution

### Step 1: {Action}

[Precise instructions]

### Step 2: {Action}

[Precise instructions]

...

## Verification

[How to confirm the solution worked — expected output, state changes, etc.]

## Example

[A concrete example showing the skill in action — input → steps → output]

## Notes

[Edge cases, limitations, things that don't work]
```

### Naming Conventions

- **Directory and name:** `kebab-case`, descriptive, 2-4 words
- **Avoid generic names:** `fix-bug` is bad; `fix-overleaf-sync-conflict` is good
- **Match the trigger:** If the natural trigger is "compile my slides", the name should relate to slide compilation

### Allowed Tools

Follow principle of least privilege:
- Report-only skills: `Read`, `Glob`, `Grep` only
- File-creating skills: add `Write`, `Edit`
- Shell-needing skills: add specific `Bash(command*)` patterns
- Interactive skills: add `AskUserQuestion`

## Phase 4: Quality Gates

Before finalising, verify:

| Gate | Check |
|------|-------|
| **Specific triggers** | Would Claude know when to invoke this? Are trigger conditions clear? |
| **Verified solution** | Has the procedure been tested in this session? Don't encode untested workflows. |
| **No secrets** | No API keys, tokens, or passwords in the skill |
| **Balanced specificity** | Specific enough to be actionable, general enough to apply across projects |
| **Minimum tools** | Only the tools actually needed are in `allowed_tools` |
| **No duplication** | Doesn't duplicate an existing skill's core functionality |

If any gate fails, fix before saving.

## After Creation

1. Confirm the skill appears: check that `~/.claude/skills/{name}/SKILL.md` exists (via the symlink)
2. Tell the user: "Created `/{name}` — [one-line summary]. It's available immediately in all projects."
3. If the skill is substantial, suggest updating `docs/skills.md` with the new entry

## What This Skill Does NOT Do

- **Does not replace `[LEARN]` tags** — one-liner corrections still go in MEMORY.md via the `learn-tags` rule
- **Does not create agents** — agents need separate context and persistent memory; use `/agents` for that
- **Does not modify existing skills** — if an existing skill needs updating, do that directly rather than through `/learn`
