# obsidian-tasknotes-skill

A [Claude Code](https://docs.anthropic.com/en/docs/claude-code) skill for managing [TaskNotes](https://tasknotes.dev/) tasks in Obsidian from the command line. Create, query, update, and track tasks without leaving your terminal.

## How It Works

The skill is a thin Python orchestrator that routes commands to the best available tool:

| Tool | Mode | When Used |
|------|------|-----------|
| **mtn** ([mdbase-tasknotes](https://www.npmjs.com/package/mdbase-tasknotes)) | File-direct | Default. Reads/writes task markdown files directly. Works offline. |
| **tn** ([tasknotes-cli](https://github.com/callumalpass/tasknotes-cli)) | HTTP API | When Obsidian is running with the API enabled. Adds pomodoro, calendars, recurring tasks. |
| **Obsidian CLI** | Obsidian | Quick property reads/writes and vault-wide search. |
| **Direct HTTP API** | HTTP | Fallback when CLIs are unavailable but the API is reachable. |

Both `mtn` and `tn` are maintained by the TaskNotes plugin author and read/write identical task files.

## Prerequisites

- [Obsidian](https://obsidian.md/) with the [TaskNotes plugin](https://github.com/callumalpass/tasknotes) installed
- [Bases](https://help.obsidian.md/bases) core plugin enabled
- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [Node.js](https://nodejs.org/) 14+ and [uv](https://docs.astral.sh/uv/) (Python runner)

## Installation

### 1. Clone the repo

```bash
git clone https://github.com/pickleton89/obsidian-tasknotes-skill.git
cd obsidian-tasknotes-skill
```

### 2. Install into your Obsidian vault

The install command copies the skill files (SKILL.md, scripts, references) into your vault's `.claude/skills/` directory. No symlinks -- all files are copied for Obsidian sync compatibility.

```bash
uv run python scripts/tn_manager.py --vault /path/to/your/vault install
```

### 3. Install and configure the CLI tools

```bash
uv run python scripts/tn_manager.py --vault /path/to/your/vault setup
```

This installs `mtn` (npm global) and `tn` (git clone + npm link), then configures both to point at your vault.

### 4. Enable required plugin settings

In Obsidian, go to **Settings -> TaskNotes -> Integrations** and enable:

- **Enable mdbase spec** -- required for `mtn` (file mode)
- **Enable HTTP API** -- required for `tn` (API mode)

## Updating

Pull the latest version and re-install into your vault:

```bash
cd /path/to/obsidian-tasknotes-skill
git pull
uv run python scripts/tn_manager.py --vault /path/to/your/vault install
```

To check whether an update is available:

```bash
uv run python scripts/tn_manager.py --vault /path/to/your/vault check-update
```

The install command is idempotent -- it overwrites the previous installation with the latest files.

## Usage

In Claude Code, invoke the skill with `/tn`:

```
/tn status                              # Task overview
/tn create "Design landing page" --priority high --due 2026-04-15
/tn nlp "Buy groceries tomorrow @home #errands ~30m"
/tn list --overdue
/tn complete "Design landing page"
```

Or run the orchestrator directly:

```bash
uv run python scripts/tn_manager.py --vault /path/to/vault <command> [options]
```

### Commands

| Command | Description |
|---------|-------------|
| `status` | Task counts by status, overdue, today's schedule |
| `create "Title" [opts]` | Create a new task |
| `nlp "natural language"` | Create task from natural language |
| `update "Title" [opts]` | Update an existing task |
| `complete "Title"` | Mark task as completed |
| `delete "Title" [--force]` | Delete a task |
| `list [filters]` | List and filter tasks |
| `search "query"` | Search tasks by content |
| `today` | Tasks due or scheduled today |
| `overdue` | Overdue incomplete tasks |
| `start-timer "Title"` | Start time tracking |
| `stop-timer` | Stop time tracking |
| `timer-log [--period P]` | Show time tracking log |
| `projects [list\|show]` | Project overview |
| `pomodoro [start\|stop\|status]` | Pomodoro timer (API-only) |
| `install [--source PATH]` | Install/update skill into vault |
| `check-update` | Check if installed skill is outdated |
| `setup` | Install/configure CLI tools |
| `help` | Show all commands and options |

### Common Options

```
--vault PATH           Obsidian vault path
--status VALUE         Task status (open, in-progress, done)
--priority VALUE       Priority (low, normal, high)
--due YYYY-MM-DD       Due date
--scheduled YYYY-MM-DD Scheduled date
--tags "a,b"           Comma-separated tags
--contexts "a,b"       Comma-separated contexts
--projects "a,b"       Comma-separated projects
--json                 Machine-readable JSON output
--file-only            Force file mode (skip API)
```

### Filtering

```bash
# By property
uv run python scripts/tn_manager.py list --status in-progress --priority high

# Advanced expression (mtn)
uv run python scripts/tn_manager.py list --where 'due < "2026-04-01" && priority == "high"'

# Advanced filter (tn)
uv run python scripts/tn_manager.py list --where 'priority:high AND tags:urgent'
```

### Natural Language

Both `mtn` and `tn` parse natural language with dates, priorities, tags, contexts, projects, and time estimates:

```bash
uv run python scripts/tn_manager.py nlp "Call dentist friday high priority @phone #health ~15m"
```

## Project Structure

```
obsidian-tasknotes-skill/
├── SKILL.md                    # Skill definition for Claude Code
├── scripts/
│   ├── common.py               # Vault discovery, tool detection, API client
│   └── tn_manager.py           # CLI orchestrator (routes to mtn/tn/API)
├── references/
│   ├── frontmatter-spec.md     # TaskNotes YAML field reference
│   └── api-reference.md        # HTTP API + CLI command reference
├── documentation/
│   └── TaskNotes-Documentation.md  # Full plugin documentation
└── README_tasknotes.md         # TaskNotes plugin README (reference)
```

When installed into a vault, only `SKILL.md`, `scripts/`, and `references/` are copied to `.claude/skills/obsidian-tasknotes/`.

## How Tasks Work

TaskNotes stores each task as a markdown file with YAML frontmatter:

```yaml
---
tags:
  - task
title: Review quarterly report
status: in-progress
priority: high
due: 2025-01-15
contexts:
  - "@office"
projects:
  - "[[Q1 Planning]]"
---

## Notes
Key points to review...
```

Tasks are identified by the `#task` tag (configurable). All property names are configurable via field mapping in the plugin settings. The skill reads these mappings at runtime.

## Related Projects

- [TaskNotes plugin](https://github.com/callumalpass/tasknotes) -- the Obsidian plugin
- [tasknotes-cli](https://github.com/callumalpass/tasknotes-cli) -- official CLI (API mode)
- [mdbase-tasknotes](https://www.npmjs.com/package/mdbase-tasknotes) -- official CLI (file mode)
- [TaskNotes docs](https://tasknotes.dev/) -- full plugin documentation

## License

MIT
