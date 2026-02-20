# Agents

Custom Claude Code agents that run as autonomous sub-processes with their own context, tools, and persistent memory.

## What Are Agents?

Agents are markdown files in `.claude/agents/` that define specialized personas launched via Claude Code's Task tool. Unlike skills (which provide instructions to the current session), agents run in a **separate context** — solving the "grading your own homework" problem.

Each agent has:
- Its own **personality and instructions** (the markdown body)
- A configurable **tool set** (Read, Write, Bash, etc.)
- A **model preference** (opus, sonnet, haiku)
- **Persistent memory** in `.claude/agent-memory/<agent-name>/`

## How Agents Work

1. You ask Claude for something that matches an agent's description (e.g., "review my paper")
2. Claude launches the agent via the Task tool as a sub-process
3. The agent runs in its own context — it can read files, run code, search the web
4. When finished, the agent returns its results to the main session
5. The agent's memory persists for future invocations

## Why Agents Run in Separate Context

Review agents MUST run as sub-processes via the Task tool — never inline in the main session:

1. **Adversarial independence** — A reviewer grading its own implementation cannot be objective.
2. **Tool isolation** — Read-only agents are physically prevented from modifying files.
3. **Context separation** — Review agents see only the finished artifact, not drafting history.

## The Read-Only Principle

Review agents must never modify the work they are reviewing:

| Agent | Can modify author files? | Enforcement | Can create own artifacts? |
|-------|--------------------------|-------------|---------------------------|
| `referee2-reviewer` | No | Text prohibition | Yes (replication scripts, reports) |
| `peer-reviewer` | No | Text prohibition | Yes (review reports) |
| `proposal-reviewer` | No | Text prohibition | Yes (review reports) |
| `paper-critic` | No | Tool restriction (Read/Glob/Grep only) | No |
| `domain-reviewer` | No | Tool restriction (Read/Glob/Grep only) | No |
| `fixer` | **Yes** (its explicit purpose) | N/A — fixing is the job | Yes (FIX-REPORT.md) |

## Available Agents

| Agent | Description | Trigger |
|-------|-------------|---------|
| `referee2-reviewer` | Formal 6-audit protocol: code, cross-language replication, directory, output automation, empirical methods, novelty. Never modifies author code. | "Review my paper", "Audit my code", "Stress-test my research" |
| `peer-reviewer` | Multi-agent peer review for external papers. Spawns 3 parallel sub-agents: Citation Validator, Novelty Assessor, Methodology Reviewer. | "Review this paper", "I'm a discussant", "Read and review this PDF" |
| `proposal-reviewer` | Multi-agent review for research proposals. Spawns 2 parallel sub-agents: Novelty Assessor, Feasibility Assessor. | "Review my proposal", "Is this idea worth pursuing?" |
| `paper-critic` | Read-only adversarial auditor for LaTeX papers. Produces scored CRITIC-REPORT.md. | "Quality check my paper", "Run the critic" |
| `domain-reviewer` | Substantive correctness: assumptions, derivations, citations, code-theory alignment. | "Check the math", "Does my code match the theory?" |
| `fixer` | Applies fixes from a critic report by priority. No independent editorial decisions. | Launched after paper-critic returns NEEDS REVISION |

## Creating a New Agent

Create a file at `.claude/agents/<agent-name>.md` with YAML frontmatter:

```yaml
---
name: my-agent
description: "What this agent does and when to invoke it"
tools: Read, Glob, Grep, Write
model: opus
color: blue
memory: project
---
```

## Global Access

Agents are made globally available via a symlink created by `setup.sh`:

```
~/.claude/agents/ → <repo>/.claude/agents/
```
