---
name: obsidian-tasknotes
description: >
  Manage tasks, to-dos, and task lists in Obsidian. The default skill for all
  task management: creating tasks, listing tasks, completing tasks, searching
  tasks, tracking time, viewing overdue/today tasks, and project task views.
  Triggers on: "/tn", "tasks", "task list", "to-do", "todo", "overdue tasks",
  "what's due", "my tasks", "create a task", "task status", "time tracking",
  "pomodoro", or any task/todo-related request involving Obsidian or the vault.
  Do NOT use for ac-tasks, ac-skill, or ac-* commands — those use ac-tasks skill.
version: "1.0.0"
user-invocable: true
context: fork
model: sonnet
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Agent
argument-hint: "[status|create|update|complete|delete|list|search|today|overdue|start-timer|stop-timer|nlp|projects|pomodoro|setup|help] -- manage Obsidian TaskNotes"
---

# Obsidian TaskNotes Skill

Manage tasks for the [TaskNotes](https://tasknotes.dev/) Obsidian plugin directly from
Claude Code. All operations route through deterministic CLI tools (`mtn` for file mode,
`tn` for API mode) with a Python orchestrator handling tool selection and output formatting.

**Plugin docs:** https://tasknotes.dev/
**GitHub:** https://github.com/callumalpass/tasknotes

## Runtime Configuration (Step 0)

Before any operation, resolve the vault and verify tools:

1. **Vault path** -- Check `$ARGUMENTS` for an explicit `--vault PATH`. If absent, run:
   ```bash
   uv run python scripts/tn_manager.py status --json 2>&1 | head -3
   ```
   The script auto-discovers the vault. If not found, ask the user for their vault path.

2. **Tool availability** -- The script auto-detects `mtn`, `tn`, and `obsidian` CLI tools.
   If neither `mtn` nor `tn` is found, run `/tn setup` to install them.

3. **Load reference files** (always, regardless of operation):
   - `references/frontmatter-spec.md` (YAML field reference for task files)
   - `references/api-reference.md` (HTTP API and CLI command reference)

---

## EXECUTE NOW

**Target: $ARGUMENTS**

Parse the command:

| Command | Action |
|---------|--------|
| (none) or `status` | Show task overview and counts |
| `create "Title" [opts]` | Create a new task |
| `nlp "natural language"` | Create task from natural language |
| `update "Title" [opts]` | Update an existing task |
| `complete "Title"` | Mark a task as completed |
| `delete "Title" [--force]` | Delete a task |
| `list [filters]` | List and filter tasks |
| `search "query"` | Search tasks by content |
| `today` | Tasks due or scheduled today |
| `overdue` | Overdue incomplete tasks |
| `start-timer "Title"` | Start time tracking |
| `stop-timer` | Stop time tracking |
| `timer-log [--period P]` | Show time tracking log |
| `projects [list\|show NAME]` | Project overview |
| `pomodoro [start\|stop\|status]` | Pomodoro timer (API-only) |
| `install [--source PATH]` | Install/update skill into vault |
| `check-update` | Check if installed skill is outdated |
| `setup` | Install/configure CLI tools |
| `help` | Show available commands |

**START NOW.** Execute the requested operation using the orchestrator script:

```bash
uv run python scripts/tn_manager.py --vault <vault-path> <command> [options]
```

---

## Data Strategy

**CLI-first, API-enhanced.** The orchestrator detects available tools and routes each
command to the best one. You do not need to choose manually -- the script handles it.

### Tool Fallback Chain

```
mtn (file mode) → tn (API mode) → direct HTTP API → error with guidance
```

- **mtn (mdbase-tasknotes)** -- Reads/writes task markdown files directly. Works offline,
  no Obsidian needed. Supports NLP creation, CRUD, time tracking, search, projects.
  Requires `enableMdbaseSpec: true` in TaskNotes settings.

- **tn (tasknotes-cli)** -- Talks to the TaskNotes HTTP API. Requires Obsidian running
  with API enabled. Adds pomodoro, calendar, recurring task management.

- **Obsidian CLI** -- Quick property reads/writes and vault search when Obsidian is running.

- **Direct HTTP API** -- Ultimate fallback via urllib. Used when CLIs are unavailable but
  the API is reachable.

### Task File Format

Tasks are standard markdown files with YAML frontmatter stored in `TaskNotes/Tasks/`:

```yaml
---
tags:
  - task
title: Review quarterly report
status: in-progress
priority: high
due: 2025-01-15
scheduled: 2025-01-14
contexts:
  - "@office"
projects:
  - "[[Q1 Planning]]"
---

## Notes
Key points to review...
```

The CLIs handle all frontmatter parsing and generation. Do NOT write task files directly --
always use the orchestrator script or CLI tools.

---

## Commands

### /tn status

Show an overview of all tasks: counts by status, overdue, and today's schedule.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> status
```

Add `--json` for machine-readable output.

### /tn create "Title"

Create a new task. The orchestrator builds NLP-compatible text from explicit options.

**Options:**
- `--status VALUE` -- task status (default: open)
- `--priority VALUE` -- priority: low, normal, high
- `--due YYYY-MM-DD` -- due date
- `--scheduled YYYY-MM-DD` -- scheduled date
- `--tags "tag1,tag2"` -- comma-separated tags
- `--contexts "ctx1,ctx2"` -- comma-separated contexts (@ prefix)
- `--projects "proj1,proj2"` -- comma-separated project names (+ prefix)
- `--time-estimate N` -- estimate in minutes
- `--description "text"` -- task body content

```bash
uv run python scripts/tn_manager.py --vault <vault-path> create "Design landing page" \
  --priority high --due 2026-04-15 --tags "design,frontend" --contexts "office"
```

### /tn nlp "natural language"

Create a task from a natural language description. Both `mtn` and `tn` support NLP parsing
with dates, priorities, tags (#), contexts (@), projects (+), and time estimates (~).

```bash
uv run python scripts/tn_manager.py --vault <vault-path> nlp \
  "Buy groceries tomorrow high priority @home #errands ~30m"
```

### /tn update "Title"

Update an existing task by title match.

**Options:**
- `--status VALUE` -- new status
- `--priority VALUE` -- new priority
- `--due YYYY-MM-DD` -- new due date
- `--scheduled YYYY-MM-DD` -- new scheduled date
- `--add-tag TAG` -- add a tag
- `--remove-tag TAG` -- remove a tag
- `--add-context CTX` -- add a context
- `--remove-context CTX` -- remove a context

```bash
uv run python scripts/tn_manager.py --vault <vault-path> update "Design landing" \
  --status in-progress --priority high
```

### /tn complete "Title"

Mark a task as completed.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> complete "Design landing page"
```

### /tn delete "Title"

Delete a task. Use `--force` to skip confirmation.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> delete "Old task" --force
```

### /tn list

List and filter tasks.

**Options:**
- `--status VALUE` -- filter by status
- `--priority VALUE` -- filter by priority
- `--tag TAG` -- filter by tag
- `--context CTX` -- filter by context
- `--project PROJ` -- filter by project
- `--overdue` -- show only overdue tasks
- `--today` -- tasks due/scheduled today
- `--completed` -- include completed tasks
- `--where EXPR` -- advanced filter expression

```bash
uv run python scripts/tn_manager.py --vault <vault-path> list --overdue --priority high
```

Advanced filtering with `--where`:
```bash
uv run python scripts/tn_manager.py --vault <vault-path> list \
  --where 'due < "2026-04-01" && priority == "high"'
```

### /tn search "query"

Search tasks by title, body content, tags, contexts, and projects.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> search "quarterly report"
```

### /tn today

Shortcut for `list --today`. Shows tasks due or scheduled today.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> today
```

### /tn overdue

Shortcut for `list --overdue`. Shows past-due incomplete tasks.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> overdue
```

### /tn start-timer "Title"

Start time tracking for a task.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> start-timer "Design landing page" \
  -d "Working on wireframes"
```

### /tn stop-timer

Stop the active time tracking session.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> stop-timer
```

### /tn timer-log

Show time tracking log. Use `--period` to filter: today, week, month, all.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> timer-log --period today
```

### /tn projects

List projects or show project details.

```bash
# List all projects
uv run python scripts/tn_manager.py --vault <vault-path> projects

# With completion stats
uv run python scripts/tn_manager.py --vault <vault-path> projects --stats

# Show specific project
uv run python scripts/tn_manager.py --vault <vault-path> projects --show "Q1 Planning"
```

### /tn pomodoro

Pomodoro timer (API-only, requires `tn` and Obsidian running).

```bash
uv run python scripts/tn_manager.py --vault <vault-path> pomodoro start
uv run python scripts/tn_manager.py --vault <vault-path> pomodoro status
uv run python scripts/tn_manager.py --vault <vault-path> pomodoro stop
```

### /tn install

Install or update the skill into a vault. Copies `SKILL.md`, `scripts/`, and `references/`
into `{vault}/.claude/skills/obsidian-tasknotes/`. No symlinks -- all files are copied for
Obsidian sync compatibility. The command is idempotent.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> install
```

Use `--source` to specify a different skill repo location:
```bash
uv run python scripts/tn_manager.py --vault <vault-path> install --source /path/to/skill-repo
```

### /tn check-update

Check if the installed skill in the vault is outdated compared to the source repo.

```bash
uv run python scripts/tn_manager.py --vault <vault-path> check-update
```

### /tn setup

Install and configure the CLI tools. Detects what's already installed and only installs
what's missing.

```bash
uv run python scripts/tn_manager.py setup
```

### /tn help

Show available commands and options.

```bash
uv run python scripts/tn_manager.py help
```

---

## Working with the Obsidian CLI

When Obsidian is running, the CLI can supplement script operations:

```bash
# Search for tasks across the vault
obsidian search query="quarterly report" path="TaskNotes/Tasks"

# Set a property on a task file
obsidian property:set name="status" value="done" path="TaskNotes/Tasks/MyTask.md"

# Read a property
obsidian property:get name="priority" path="TaskNotes/Tasks/MyTask.md"
```

**When to use CLI vs scripts:**
- Obsidian CLI: quick single-property reads/writes, vault-wide search
- Scripts (tn_manager.py): all CRUD, bulk operations, filtering, time tracking

---

## Task Matching

Both `mtn` and `tn` support title-based task matching:

1. **Exact** case-insensitive match
2. **Substring/fuzzy** match if no exact match
3. Multiple matches: the CLI lists them and asks for clarification
4. No match: reports "Task not found"

---

## Error Handling

| Situation | Response |
|-----------|----------|
| Neither CLI installed | Prompt to run `/tn setup` |
| `mtn` missing, `tn` available | Use `tn` (API mode), note offline limitation |
| `tn` missing, `mtn` available | Use `mtn` (file mode), note API features unavailable |
| API not available (API-only ops) | Error: "Requires Obsidian running with API enabled" |
| Task not found | Report with suggestions |
| Multiple title matches | List matches, ask user to be specific |
| mdbase spec not enabled | Guide user to enable it in Settings |
| CLI command fails | Print stderr, suggest troubleshooting |
| Vault not found | Ask user for vault path |

---

## Prerequisites

- **TaskNotes plugin** installed and enabled in Obsidian
- **Bases core plugin** enabled in Obsidian
- **mtn** (`npm install -g mdbase-tasknotes`) for file-mode operations
- **tn** (see `/tn setup`) for API-mode operations
- For `mtn`: enable "mdbase spec" in TaskNotes Settings -> Integrations
- For `tn`: enable "HTTP API" in TaskNotes Settings -> Integrations

---

## Integration Notes

- This skill is independent of the obsidian-project-planner skill. TaskNotes and Project
  Planner serve different purposes and manage different data.
- The skill uses the Obsidian CLI skill for CLI operations when beneficial, but does not
  depend on it.
- Task tags created by this skill are Obsidian frontmatter tags (e.g., `#task`), not
  a separate tag system.

---

## Installation & Updates

**Install skill into a vault** (copies files, no symlinks):
```bash
uv run python scripts/tn_manager.py --vault /path/to/vault install
```

**Update the skill** (pull latest from repo, then re-install):
```bash
cd /path/to/obsidian-tasknotes-skill
git pull
uv run python scripts/tn_manager.py --vault /path/to/vault install
```

**Check for updates:**
```bash
uv run python scripts/tn_manager.py --vault /path/to/vault check-update
```

**Install CLI tools** (separate from skill installation):
```bash
uv run python scripts/tn_manager.py --vault /path/to/vault setup
```

**What gets installed into the vault** (via `install`):
- `SKILL.md` -- skill definition
- `scripts/` -- Python orchestrator (common.py, tn_manager.py)
- `references/` -- frontmatter spec and API reference
- `.installed-version` -- version marker for update checks

**What gets installed globally** (via `setup`):
- `mdbase-tasknotes` (npm global) -- provides `mtn` command
- `tasknotes-cli` (git clone + npm link) -- provides `tn` command
- Configuration for both tools pointing to the vault
