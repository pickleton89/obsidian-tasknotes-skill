# TaskNotes — Frontmatter Specification

> Reference for the YAML frontmatter format used by TaskNotes task files.

## File Location

```
{VaultRoot}/TaskNotes/Tasks/{filename}.md
```

The tasks folder is configurable (default: `TaskNotes/Tasks/`). Filenames use zettel format
by default (timestamp-based) with the title stored in frontmatter.

## Full Template

```yaml
---
tags:
  - task
title: Review quarterly report
status: in-progress
priority: high
due: 2025-01-15
scheduled: 2025-01-14T09:00
contexts:
  - "@office"
  - "@phone"
projects:
  - "[[Q1 Planning]]"
  - "[[Budget Review]]"
timeEstimate: 60
completedDate: null
dateCreated: 2025-01-10T08:30:00
dateModified: 2025-01-14T10:00:00
recurrence: "DTSTART:20250804T090000Z;FREQ=WEEKLY;BYDAY=MO,WE,FR"
recurrence_anchor: "2025-01-10"
complete_instances:
  - "2025-01-06"
  - "2025-01-08"
skipped_instances: []
blockedBy:
  - uid: "[[Operations/Order hardware]]"
    reltype: FINISHTOSTART
    gap: P1D
timeEntries:
  - startTime: "2025-01-14T09:00:00"
    endTime: "2025-01-14T10:30:00"
    description: "Initial review"
reminders:
  - type: relative
    trigger: "-PT15M"
    relativeTo: due
---

## Notes

Key points to review:
- Revenue projections
- Budget allocations

## Meeting Notes

Discussion with finance team on 2025-01-10...
```

## Minimal Template (New Task)

The minimum required fields for a valid TaskNotes task:

```yaml
---
tags:
  - task
title: Buy groceries
status: open
---
```

## Field Reference

### Task Identification

Tasks are identified by the `#task` tag (default) or a frontmatter property,
configured in Settings -> Task Properties -> Task Identification.

| Method | Configuration |
|--------|--------------|
| Tag (default) | `tags` array includes the configured tag (default: `task`) |
| Property | A specific frontmatter key/value pair |

### Core Properties

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `title` | string | — | Task display name (required) |
| `status` | string | `open` | Configurable values (see below) |
| `priority` | string | `normal` | Configurable values (see below) |
| `due` | date | — | `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM` |
| `scheduled` | datetime | — | `YYYY-MM-DD` or `YYYY-MM-DDTHH:MM` |

### Status Values (Default Configuration)

| Value | Label | Completed? |
|-------|-------|-----------|
| `none` | None | No |
| `open` | Open | No |
| `in-progress` | In Progress | No |
| `done` | Done | Yes |

### Priority Values (Default Configuration)

| Value | Label | Weight |
|-------|-------|--------|
| `none` | None | 0 |
| `low` | Low | 1 |
| `normal` | Normal | 2 |
| `high` | High | 3 |

### Organization Properties

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `tags` | list | `["task"]` | YAML list; must include task identification tag |
| `contexts` | list | `[]` | Prefixed with `@` (e.g., `"@office"`) |
| `projects` | list | `[]` | Wiki-links (e.g., `"[[Project A]]"`) |

### Date & Tracking Properties

| Field | Type | Default | Notes |
|-------|------|---------|-------|
| `completedDate` | date | `null` | Set when status changes to a completed state |
| `dateCreated` | datetime | — | ISO 8601 timestamp of creation |
| `dateModified` | datetime | — | ISO 8601 timestamp of last modification |
| `timeEstimate` | number | `0` | Estimated time in minutes |

### Time Tracking

```yaml
timeEntries:
  - startTime: "2025-01-14T09:00:00"
    endTime: "2025-01-14T10:30:00"
    description: "Initial review"
  - startTime: "2025-01-15T14:00:00"
    endTime: null
    description: "Continuing review"
```

Each entry has `startTime` (required), `endTime` (null if active), and optional `description`.

### Recurrence

Uses RFC 5545 RRule format with `DTSTART` anchor:

```yaml
recurrence: "DTSTART:20250804T090000Z;FREQ=DAILY"
recurrence_anchor: "2025-08-04"
scheduled: "2025-08-04T09:00"
complete_instances:
  - "2025-08-04"
  - "2025-08-06"
skipped_instances: []
```

**Common patterns:**
- Daily: `DTSTART:20250804T090000Z;FREQ=DAILY`
- Weekly Mon/Wed/Fri: `DTSTART:20250804T140000Z;FREQ=WEEKLY;BYDAY=MO,WE,FR`
- Monthly on 15th: `DTSTART:20250815;FREQ=MONTHLY;BYMONTHDAY=15`
- Last Friday of month: `DTSTART:20250801T100000Z;FREQ=MONTHLY;BYDAY=-1FR`

### Dependencies

```yaml
blockedBy:
  - uid: "[[Operations/Order hardware]]"
    reltype: FINISHTOSTART
    gap: P1D
```

| Subfield | Required | Notes |
|----------|----------|-------|
| `uid` | yes | Wiki-link to the blocking task |
| `reltype` | yes | `FINISHTOSTART`, `STARTTOSTART`, `FINISHTOFINISH`, `STARTTOFINISH` |
| `gap` | no | ISO 8601 duration (e.g., `PT4H`, `P2D`) |

### Reminders

```yaml
reminders:
  - type: relative
    trigger: "-PT15M"
    relativeTo: due
  - type: absolute
    trigger: "2025-01-14T08:00:00"
```

### Field Mapping

All property names are configurable in Settings -> Task Properties -> Field Mapping.
Default mappings use the field names shown in this document. If a user has customized
field names, the CLI tools and API handle the mapping automatically.

## Date Formats

| Format | Example | Usage |
|--------|---------|-------|
| `YYYY-MM-DD` | `2025-02-14` | Date-only fields (due, scheduled when all-day) |
| `YYYY-MM-DDTHH:MM` | `2025-02-14T09:00` | Date-time fields (scheduled with time) |
| `YYYY-MM-DDTHH:MM:SS` | `2025-02-14T09:00:00` | Full ISO 8601 (timeEntries, dateCreated) |

## NLP Trigger Characters

| Trigger | Property | Example |
|---------|----------|---------|
| `#` | tags | `#work` |
| `@` | contexts | `@office` |
| `+` | projects | `+[[Project A]]` |
| `*` | status | `*in-progress` |
| `!` | priority | `!high` (disabled by default) |

## Computed Properties (in .base views)

| Property | Formula | Description |
|----------|---------|-------------|
| `daysUntilDue` | days between now and due | Days remaining |
| `isOverdue` | due < today AND status != done | Boolean overdue flag |
| `urgencyScore` | priority weight + deadline proximity | Combined urgency metric |
| `efficiencyRatio` | tracked time / estimated time | Time efficiency percentage |
