# TaskNotes — API & CLI Reference

> Quick reference for the HTTP API endpoints and CLI tool commands.

## HTTP API

### Configuration

- **Base URL:** `http://localhost:8080` (port configurable)
- **Enable:** Settings -> TaskNotes -> Integrations -> HTTP API
- **Auth:** Optional Bearer token (`Authorization: Bearer <token>`)
- **Desktop only** -- not available on mobile

### Response Format

```json
// Success
{ "success": true, "data": { ... } }

// Error
{ "success": false, "error": "Error message" }
```

### System Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/health` | Service state and vault metadata |
| `GET` | `/api/docs` | OpenAPI JSON |
| `GET` | `/api/docs/ui` | Swagger UI |
| `GET` | `/api/stats` | Summary counts: total, completed, active, overdue, archived |
| `GET` | `/api/filter-options` | Available filter values for UI builders |

### Task Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/tasks` | List tasks (paginated: `limit`, `offset`) |
| `POST` | `/api/tasks` | Create task (required: `title`) |
| `GET` | `/api/tasks/:id` | Get task by URL-encoded path |
| `PUT` | `/api/tasks/:id` | Partial update |
| `DELETE` | `/api/tasks/:id` | Delete task |
| `POST` | `/api/tasks/:id/toggle-status` | Toggle status via workflow |
| `POST` | `/api/tasks/:id/archive` | Toggle archive state |
| `POST` | `/api/tasks/:id/complete-instance` | Complete recurring instance |
| `POST` | `/api/tasks/query` | Advanced filtering (FilterQuery) |

**Important:** `GET /api/tasks` rejects filter params — use `POST /api/tasks/query`.

### Create Task Request Body

```json
{
  "title": "Buy groceries",
  "status": "open",
  "priority": "high",
  "due": "2025-01-15",
  "scheduled": "2025-01-14T09:00",
  "tags": ["shopping"],
  "contexts": ["@home"],
  "projects": ["[[Household]]"],
  "timeEstimate": 30,
  "recurrence": "DTSTART:20250115;FREQ=WEEKLY"
}
```

### FilterQuery (POST /api/tasks/query)

```json
{
  "filter": {
    "conjunction": "AND",
    "conditions": [
      { "property": "status", "operator": "is", "value": "open" },
      { "property": "priority", "operator": "is", "value": "high" }
    ]
  },
  "sort": { "property": "due", "direction": "asc" },
  "limit": 50,
  "offset": 0
}
```

**Filter operators:** `is`, `is-not`, `contains`, `does-not-contain`, `before`, `after`,
`empty`, `not-empty`, `greater-than`, `less-than`

**Filter properties:** `title`, `status`, `priority`, `tags`, `contexts`, `projects`,
`due`, `scheduled`, `completed`, `created`, `modified`, `archived`, `estimate`

### NLP Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/nlp/parse` | Parse natural language (returns parsed + taskData) |
| `POST` | `/api/nlp/create` | Parse and create task (returns task + parsed) |

```bash
curl -X POST http://localhost:8080/api/nlp/create \
  -H "Content-Type: application/json" \
  -d '{"text": "Buy groceries tomorrow high priority @home #errands"}'
```

### Time Tracking Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/tasks/:id/time/start` | Start tracking |
| `POST` | `/api/tasks/:id/time/start-with-description` | Start with description |
| `POST` | `/api/tasks/:id/time/stop` | Stop tracking |
| `GET` | `/api/tasks/:id/time` | Per-task time summary |
| `GET` | `/api/time/active` | Currently active sessions |
| `GET` | `/api/time/summary` | Aggregate summary (`period`, `from`, `to`) |

### Pomodoro Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/pomodoro/start` | Start session (optional: `taskId`, `duration`) |
| `POST` | `/api/pomodoro/stop` | Stop and reset |
| `POST` | `/api/pomodoro/pause` | Pause |
| `POST` | `/api/pomodoro/resume` | Resume |
| `GET` | `/api/pomodoro/status` | Current state |
| `GET` | `/api/pomodoro/sessions` | History (`limit`, `date`) |
| `GET` | `/api/pomodoro/stats` | Today's stats |

### Calendar Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/api/calendars` | Provider overview |
| `GET` | `/api/calendars/events` | Merged events (`start`, `end` ISO params) |

### Webhook Endpoints

| Method | Path | Description |
|--------|------|-------------|
| `POST` | `/api/webhooks` | Register (required: `url`, `events`) |
| `GET` | `/api/webhooks` | List registered |
| `DELETE` | `/api/webhooks/:id` | Delete |
| `GET` | `/api/webhooks/deliveries` | Last 100 deliveries |

---

## CLI Tools

### mtn (mdbase-tasknotes) — File Mode

Works directly on markdown files. No Obsidian needed.

**Install:** `npm install -g mdbase-tasknotes`
**Config:** `mtn config --set collectionPath=/path/to/vault`
**Requires:** `enableMdbaseSpec: true` in TaskNotes settings

| Command | Description |
|---------|-------------|
| `mtn create "text"` | Create task from NLP text |
| `mtn list [options]` | List tasks with filters |
| `mtn show "title"` | Show task details |
| `mtn complete "title"` | Mark as completed |
| `mtn update "title" [opts]` | Update task fields |
| `mtn delete "title"` | Delete task |
| `mtn archive "title"` | Archive task |
| `mtn search "query"` | Full-text search |
| `mtn timer start "title"` | Start time tracking |
| `mtn timer stop` | Stop time tracking |
| `mtn timer status` | Show active timers |
| `mtn timer log [--period P]` | Time entry log |
| `mtn projects list [--stats]` | List projects |
| `mtn projects show "name"` | Project details |
| `mtn stats` | Task statistics |
| `mtn interactive` | Interactive REPL |
| `mtn config [--list\|--set\|--get]` | Configuration |

**List filters:**
- `--status VALUE`, `--priority VALUE`, `--tag TAG`, `--context CTX`, `--project PROJ`
- `--overdue`, `--today`, `--completed`
- `--where 'EXPR'` (advanced: `due < "2026-03-01" && priority == "urgent"`)

### tn (tasknotes-cli) — API Mode

Talks to TaskNotes HTTP API. Requires Obsidian running.

**Install:** `git clone` + `npm install` + `npm link`
**Config:** `~/.tasknotes-cli/config.json` (host, port, authToken, maxResults)

| Command | Description |
|---------|-------------|
| `tn "text"` | Create task from NLP text |
| `tn list [options]` | List tasks with filters |
| `tn complete "title"` | Mark as completed |
| `tn update "title" [opts]` | Update task fields |
| `tn delete "title"` | Delete task |
| `tn search "query"` | Search tasks |
| `tn timer start "title"` | Start time tracking |
| `tn timer stop` | Stop time tracking |
| `tn timer log [--period P]` | Time entry log |
| `tn pomodoro start` | Start pomodoro session |
| `tn pomodoro stop` | Stop pomodoro |
| `tn pomodoro status` | Pomodoro status |
| `tn projects list [--stats]` | List projects |
| `tn stats` | Task statistics |
| `tn recurring list` | List recurring tasks |
| `tn calendar events [range]` | Calendar events |

All commands support `--json` for machine-readable output.

### NLP Patterns (Both Tools)

| Pattern | Property | Example |
|---------|----------|---------|
| Date words | due/scheduled | `tomorrow`, `friday`, `next week`, `2026-03-01` |
| `#tag` | tags | `#work`, `#errands` |
| `@context` | contexts | `@office`, `@home` |
| `+project` | projects | `+website`, `+[[Project A]]` |
| Priority words | priority | `high priority`, `urgent`, `!!!` |
| Time estimate | timeEstimate | `~2h`, `~30m`, `estimate 45m` |
| Recurrence | recurrence | `daily`, `weekly`, `every monday` |

---

## Error Codes (HTTP API)

| Code | Meaning |
|------|---------|
| 400 | Invalid request (bad params, missing fields) |
| 401 | Missing or invalid auth token |
| 404 | Resource not found |
| 500 | Internal server error |
