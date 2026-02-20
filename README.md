# Claude Code for Academic Research

A complete Claude Code infrastructure for PhD researchers — skills, agents, hooks, and rules for academic workflows. Built for researchers who write papers in LaTeX, manage bibliographies, run experiments, and want AI assistance that understands academic conventions.

## What's Included

| Component | Count | Description |
|-----------|-------|-------------|
| **Skills** | 31 | Slash commands for common tasks (`/proofread`, `/latex-autofix`, `/literature`, etc.) |
| **Agents** | 6 | Specialised reviewers (peer review, referee 2, proposal review, paper critic, domain review, fixer) |
| **Hooks** | 8 | Automated guardrails (destructive git protection, context monitoring, source file protection, etc.) |
| **Rules** | 9 | Always-on policies (plan before implementing, scope discipline, design before results, etc.) |
| **Context library** | — | Structured files that give Claude persistent memory about you, your projects, and your workflows |
| **OpenAlex MCP** | — | Scholarly search server for academic literature discovery |

## Quick Start

### 1. Clone

```bash
git clone https://github.com/flonat/claude-code-public.git
cd claude-code-public
```

### 2. Run setup

```bash
./scripts/setup.sh
```

This creates symlinks so Claude Code can find your skills, agents, hooks, and rules from any project directory.

### 3. Customise your context

Edit these files with your own details:

- `.context/profile.md` — Your name, institution, research areas, supervisors
- `.context/current-focus.md` — What you're working on right now
- `.context/projects/_index.md` — Your active research projects
- `CLAUDE.md` — Conventions, tool preferences, Notion database IDs

### 4. Configure settings

Edit `.claude/settings.json` to adjust:
- Allowed/denied commands
- Hook configuration
- Model preferences

### 5. Start using it

```bash
cd ~/your-research-project
claude
```

Claude will automatically load your context, skills, and rules. Try:

- `/proofread` — Academic proofreading for a LaTeX paper
- `/latex-autofix` — Compile LaTeX with automatic error fixing
- `/validate-bib` — Check citation keys against your `.bib` file
- `/literature` — Search for academic papers and manage bibliography
- `/session-log` — Create a timestamped progress log
- `/code-review` — 11-category quality review for R/Python scripts

## Project Structure

```
claude-code-public/
├── CLAUDE.md                    # Main instruction file (customise this)
├── README.md                    # This file
├── MEMORY.md                    # Accumulated knowledge (auto-populated)
├── .claude/
│   ├── agents/                  # 6 specialised review agents
│   ├── rules/                   # 9 auto-loaded policy rules
│   └── settings.json            # Permissions, hooks, model config
├── skills/                      # 31 slash commands
│   ├── shared/                  # Shared utilities (palettes, scoring, rhetoric)
│   ├── proofread/               # Academic proofreading
│   ├── latex-autofix/           # LaTeX compilation + auto-fix
│   ├── literature/              # Literature search + synthesis
│   └── ...                      # See docs/skills.md for full list
├── hooks/                       # 8 automated guardrails
├── .context/                    # AI context library
│   ├── profile.md               # Your identity and background
│   ├── current-focus.md         # What you're working on NOW
│   ├── projects/                # Project metadata
│   ├── preferences/             # Workflow preferences
│   ├── workflows/               # Process guides (daily review, etc.)
│   └── resources/               # Reference data (journal rankings, etc.)
├── .mcp-server-openalex/        # OpenAlex scholarly search server
├── docs/                        # Component documentation
├── log/                         # Session logs (auto-created)
└── scripts/
    └── setup.sh                 # Initial setup script
```

## Key Concepts

### Context Library (`.context/`)

The context library gives Claude persistent memory about you and your work. Instead of re-explaining your research every session, Claude reads these files automatically.

- **`profile.md`** — Who you are (background, supervisors, tools)
- **`current-focus.md`** — What you're doing right now (updated each session)
- **`projects/_index.md`** — All your research projects at a glance
- **`workflows/`** — How you want Claude to help with recurring tasks
- **`preferences/`** — Your priority framework and naming conventions

### Skills (`skills/`)

Skills are slash commands — type `/proofread` and Claude runs a structured academic proofreading protocol. Each skill has a `SKILL.md` file defining its behaviour, and optionally a `references/` directory with supporting material.

See [`docs/skills.md`](docs/skills.md) for the full catalogue.

### Agents (`.claude/agents/`)

Agents are specialised personas for complex review tasks. They use multi-agent architectures (spawning sub-agents for parallel work) and produce formal reports.

| Agent | Use case |
|-------|----------|
| `referee2-reviewer` | Rigorous audit of your own work (code, methods, replication) |
| `peer-reviewer` | Review someone else's paper (spawns citation, novelty, methods sub-agents) |
| `proposal-reviewer` | Review research proposals and extended abstracts |
| `paper-critic` | Adversarial LaTeX paper audit with quality scoring |
| `domain-reviewer` | Substantive correctness (math, assumptions, code-theory alignment) |
| `fixer` | Apply fixes from a critic report |

See [`docs/agents.md`](docs/agents.md) for detailed descriptions.

### Hooks (`hooks/`)

Hooks run automatically at specific points in a Claude Code session to provide guardrails and context.

| Hook | Trigger | What it does |
|------|---------|-------------|
| `block-destructive-git.sh` | Before Bash | Catches dangerous git commands (force push, reset --hard, etc.) |
| `context-monitor.py` | After tool use | Tracks context usage and warns before auto-compact |
| `promise-checker.sh` | Session stop | Catches Claude saying "I'll remember" without actually writing |
| `startup-context-loader.sh` | Session start | Loads context files automatically |
| `resume-context-loader.sh` | Session resume | Restores focus on resume |
| `precompact-autosave.py` | Before compact | Saves state before context compression |
| `postcompact-restore.py` | After compact | Restores state after context compression |
| `protect-source-files.sh` | Before edit/write | Warns when editing files outside the project |

See [`docs/hooks.md`](docs/hooks.md) for full documentation.

### Rules (`.claude/rules/`)

Rules are always-on policies that Claude follows in every session. They enforce good research practices.

See [`docs/rules.md`](docs/rules.md) for full documentation.

## Customisation

### Adding a new research project

1. Create a directory for your project
2. Add a `CLAUDE.md` in the project with project-specific instructions
3. Symlink `paper/` to your Overleaf directory (if applicable)
4. Add the project to `.context/projects/_index.md`
5. Create a paper file in `.context/projects/papers/`

### Adding your own skills

Create a new directory in `skills/` with a `SKILL.md` file:

```
skills/my-custom-skill/
└── SKILL.md
```

The `SKILL.md` needs YAML frontmatter with `name`, `description`, and optionally `allowed-tools`. See any existing skill for the format.

### Connecting Notion

If you use Notion for task management:

1. Set up the [Notion MCP server](https://github.com/anthropics/claude-code) for Claude Code
2. Add your database IDs to `CLAUDE.md`
3. The workflows in `.context/workflows/` reference Notion for daily reviews and task management

### Setting up OpenAlex MCP

The OpenAlex MCP server provides scholarly search capabilities:

1. Edit `.mcp-server-openalex/server.py` — update the email address
2. Add the server to your Claude Code MCP configuration
3. Use `/literature` to search for papers

## Requirements

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) (CLI)
- LaTeX distribution (for paper compilation skills)
- [uv](https://docs.astral.sh/uv/) (for Python package management)
- Git

## Credits

This infrastructure draws on design patterns from [Pedro Sant'Anna's Claude Code workflow](https://github.com/pedrohcgs) (specialist agents, plan-first, quality gates, critic-fixer loops, [LEARN] tags).

## License

MIT
