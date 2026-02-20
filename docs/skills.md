# Skills

> 30 reusable workflow definitions available across all projects.

Skills are structured instruction sets (`SKILL.md` files) that turn Claude into a specialised tool for specific tasks — from compiling LaTeX to reviewing code. Each skill declares its own allowed tools.

## Overview

| Skill | Category | Description |
|-------|----------|-------------|
| `audit-project-structure` | Code & Safety | Audit project structure against template (report only) |
| `audit-template-compliance` | Research & Writing | Compare LaTeX preamble against working paper template |
| `beamer-deck` | Research & Writing | Rhetoric-driven Beamer presentations with multi-agent review |
| `code-archaeology` | Code & Safety | Systematically review and document old code and data files |
| `code-review` | Code & Safety | 11-category scorecard for R/Python scripts (report only) |
| `context-status` | Session Management | On-demand session health check (context usage, plans, focus) |
| `devils-advocate` | Research & Writing | Challenge research assumptions and stress-test arguments |
| `humanizer` | Research & Writing | Remove signs of AI-generated writing |
| `insights-deck` | Utilities | Archive `/insights` HTML and build a Beamer deck |
| `interview-me` | Research & Writing | Interactive interview to formalise a research idea |
| `latex` | Research & Writing | LaTeX compilation with latexmk |
| `latex-autofix` | Research & Writing | **Default compiler** — auto-fixes errors, citation audit |
| `learn` | Session Management | Extract reusable knowledge into persistent skills |
| `literature` | Research & Writing | Academic literature discovery, synthesis, and OpenAlex queries |
| `pre-submission-report` | Publishing | Run all quality checks before submission |
| `project-deck` | Research & Writing | Presentation decks for supervisor meetings |
| `project-safety` | Code & Safety | Safety rules and folder structures to prevent data loss |
| `proofread` | Research & Writing | Academic proofreading — 6-category check (report only) |
| `quarto-deck` | Research & Writing | Reveal.js HTML presentations with rhetoric principles |
| `research-ideation` | Research & Writing | Generate structured research questions with hypotheses |
| `retarget-journal` | Research & Writing | Switch a paper to a different journal |
| `save-context` | Session Management | Save information to context library files |
| `session-close` | Session Management | End-of-session checklist (git, focus, docs, log) |
| `session-log` | Session Management | Timestamped progress logs for session continuity |
| `split-pdf` | Research & Writing | Deep-read academic papers via 4-page splits |
| `sync-permissions` | Utilities | Sync global permissions into projects |
| `system-audit` | Utilities | Run parallel system audits (inventory, conventions, docs) |
| `update-focus` | Session Management | Structured updates to `current-focus.md` |
| `update-project-doc` | Session Management | Update a project's own docs to reflect current state |
| `validate-bib` | Research & Writing | Cross-reference `\cite{}` keys against `.bib` files |

## Skill Categories

### Research & Writing (16 skills)

Tools for the academic writing workflow: compilation, proofreading, literature search, bibliography management, presentations, and journal targeting.

### Session Management (7 skills)

Tools for maintaining context across Claude Code sessions: focus tracking, session logging, context saving, and end-of-session checklists.

### Code & Safety (4 skills)

Tools for code quality and project safety: code review scorecards, code archaeology, project structure auditing, and safety rules.

### Utilities (3 skills)

System-level tools: permission syncing, system auditing, and presentation archiving.

## Using Skills

Invoke a skill by typing its name as a slash command:

```
/proofread
/latex-autofix
/validate-bib
/literature find papers on choice architecture
```

Or describe what you want naturally — Claude will match it to the right skill.

## Skill Structure

Each skill is a directory in `skills/`:

```
skills/
├── proofread/
│   ├── SKILL.md           # Main skill definition
│   └── references/        # Supporting material (optional)
│       └── quality-rubric.md
├── latex-autofix/
│   ├── SKILL.md
│   └── references/
└── shared/                # Utilities shared across skills
    ├── palettes.md
    ├── quality-scoring.md
    └── rhetoric-principles.md
```

### SKILL.md Format

```yaml
---
name: my-skill
description: "What this skill does"
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
argument-hint: <file.tex> or (no arguments)
---

# Skill instructions in markdown...
```

## Global Access

Skills are globally available via a symlink created by `setup.sh`:

```
~/.claude/skills/ → <repo>/skills/
```

## Creating New Skills

1. Create a directory: `skills/my-skill/`
2. Write `SKILL.md` with frontmatter and instructions
3. Optionally add a `references/` directory for supporting material
4. The skill is immediately available as `/my-skill`
