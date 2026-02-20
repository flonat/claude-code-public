---
name: session-log
description: "Create timestamped progress logs for research sessions. Enables continuity between Claude sessions."
allowed-tools: Read, Write, Edit, Bash(mkdir*), Bash(ls*)
argument-hint: [project-name-or-path]
---

# Session Log Skill

> Automatically create timestamped progress logs for research sessions.

## Purpose

Based on Scott Cunningham's Claude Code workflow: "Progress logs are my autosave of the workflow." When sessions end or crash, the next Claude can read logs and pick up exactly where you left off.

## When to Use

At the end of any significant work session, or when asked to "log this session" or "update progress".

## Workflow

1. **Read existing context** - Check `.context/current-focus.md` and recent logs in `log/`
2. **Summarise the session**:
   - What was accomplished
   - Key decisions made
   - Problems encountered
   - What's next
3. **Create timestamped log** in `log/YYYY-MM-DD-HHMM.md`
4. **Update current-focus.md** — offer to run `/update-focus` for a structured update (session rotation, open loops), rather than making ad-hoc edits

## Log Template

```markdown
# Session Log: [Date] [Time]

## Project: [Project Name]

## What We Did
- [Bullet points of accomplishments]

## Key Decisions
- [Any choices made and why]

## Problems/Blockers
- [Issues encountered]

## Next Steps
- [ ] [Actionable next items]

## Files Changed
- [List of modified files]
```

## Example Prompt

"Please log this session - we worked on the research paper, fixed the simulation code, and decided to target Journal B instead of Journal A."
