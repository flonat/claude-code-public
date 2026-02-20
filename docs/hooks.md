# Hooks

> 8 automated guardrails that run at specific points in a Claude Code session.

Hooks are scripts that Claude Code executes automatically at defined trigger points. They provide safety guardrails, context loading, and state management without manual intervention.

## Hook Events

| Event | When it fires | Purpose |
|-------|--------------|---------|
| `SessionStart` (startup) | Fresh session begins | Load context files |
| `SessionStart` (resume) | Resuming a session | Restore focus state |
| `SessionStart` (compact) | After context compression | Restore pre-compact state |
| `PreToolUse` | Before a tool executes | Block dangerous operations |
| `PostToolUse` | After a tool executes | Monitor context usage |
| `PreCompact` | Before context compression | Save state snapshot |
| `Stop` | Session ends | Catch unfulfilled promises |

## Available Hooks

### Safety Hooks

#### `block-destructive-git.sh`
**Trigger:** PreToolUse (Bash)

Catches dangerous git and shell commands before they execute:
- `git reset --hard` — discard uncommitted changes
- `git push -f` / `--force` (without `--force-with-lease`) — overwrite remote history
- `git clean -f` — delete untracked files
- `git checkout .` / `git restore .` — discard unstaged changes
- `git branch -D` — force-delete branch
- `rm -rf` — destructive file deletion

Uses a **soft block** — surfaces a permission prompt so you can approve if intentional.

#### `protect-source-files.sh`
**Trigger:** PreToolUse (Edit|Write)

Prompts for confirmation when Claude tries to edit files outside the current project:
- **Allow:** Files inside the current project directory
- **Allow:** Files under `~/.claude/`
- **Ask:** Everything else

Prevents accidental edits to files in other projects.

#### `promise-checker.sh`
**Trigger:** Stop

Detects "performative compliance" — when Claude claims to have remembered, saved, or noted something but never actually called Edit/Write to persist it. Catches patterns like:
- "I'll remember this" / "I've noted that" / "Saved to memory"
- "I'll update the file" / "I've recorded this"

Blocks the session stop if promises were made but no write operations occurred.

### Context Hooks

#### `startup-context-loader.sh`
**Trigger:** SessionStart (startup)

Automatically loads project documentation at the start of a fresh session:
1. Current focus (`.context/current-focus.md`)
2. Project index (`.context/projects/_index.md`)
3. Knowledge base (`MEMORY.md`)
4. Project-specific README
5. Latest session log
6. Latest plan

Provides Claude with full context without manual prompting.

#### `resume-context-loader.sh`
**Trigger:** SessionStart (resume)

Lighter version of the startup loader for resumed sessions:
1. Current focus
2. Latest session log

Designed for quick context restoration when the full context is already loaded.

### State Management Hooks

#### `precompact-autosave.py`
**Trigger:** PreCompact

Saves state before Claude Code compresses the conversation context:
1. **Human-readable snapshot** → `log/{timestamp}-compact.md`
2. **Machine-readable state** → JSON file for automatic restoration

Captures: current focus, active plan status, recent decisions, working directory.

#### `postcompact-restore.py`
**Trigger:** SessionStart (compact)

Restores state after context compression by reading the JSON state saved by `precompact-autosave.py`. Provides Claude with:
- What was being worked on
- Active plan and next step
- Recent decisions
- Recovery actions

#### `context-monitor.py`
**Trigger:** PostToolUse (Bash|Task)

Tracks tool call count as a heuristic for context usage (150 tool calls ~ 100% context). Fires warnings at:
- **60%** (~90 calls): Info — "Consider saving key state"
- **80%** (~120 calls): Warning — "Auto-compact approaching"
- **90%** (~135 calls): Critical — "Complete current task"

Each warning fires once per session to avoid noise.

## Configuration

Hooks are configured in `~/.claude/settings.json` under the `hooks` key. The example settings.json included in this repo has all hooks pre-configured:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup",
        "hooks": [{ "type": "command", "command": "$HOME/.claude/hooks/startup-context-loader.sh" }]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{ "type": "command", "command": "$HOME/.claude/hooks/block-destructive-git.sh" }]
      }
    ]
  }
}
```

## Global Access

Hooks are globally available via a symlink created by `setup.sh`:

```
~/.claude/hooks/ → <repo>/hooks/
```

## Creating New Hooks

1. Create a script in `hooks/` (bash or python)
2. Make it executable: `chmod +x hooks/my-hook.sh`
3. Add it to `~/.claude/settings.json` under the appropriate event
4. The hook output format depends on the event — see [Claude Code docs](https://docs.anthropic.com/en/docs/claude-code) for the hook API
