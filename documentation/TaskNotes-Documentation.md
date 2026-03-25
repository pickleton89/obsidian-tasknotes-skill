# TaskNotes Documentation

> Complete documentation for the TaskNotes plugin for Obsidian.
> Source: [tasknotes.dev](https://tasknotes.dev/) — Scraped March 25, 2026

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Core Concepts](#core-concepts)
3. [Features](#features)
   - [Task Management](#task-management)
   - [Inline Task Integration](#inline-task-integration)
   - [Calendar Integration](#calendar-integration)
   - [ICS Calendar Event Integration](#ics-calendar-event-integration)
   - [Recurring Tasks](#recurring-tasks)
   - [Time Management](#time-management)
   - [User Fields](#user-fields)
   - [Template Variables Reference](#template-variables-reference)
4. [Views](#views)
   - [Task List View](#task-list-view)
   - [Kanban View](#kanban-view)
   - [Calendar Views](#calendar-views)
   - [Pomodoro View](#pomodoro-view)
   - [Default Base Templates](#default-base-templates)
5. [Settings](#settings)
   - [General Settings](#general-settings)
   - [Task Properties Settings](#task-properties-settings)
   - [Modal Fields Settings](#modal-fields-settings)
   - [Appearance & UI Settings](#appearance--ui-settings)
   - [Features Settings](#features-settings)
   - [Integrations Settings](#integrations-settings)
   - [Defaults & Templates Settings](#defaults--templates-settings)
   - [Advanced Settings](#advanced-settings)
   - [Property Types Reference](#property-types-reference)
6. [Workflows](#workflows)
7. [HTTP API](#tasknotes-http-api)
8. [Troubleshooting](#troubleshooting)
9. [Development](#development)
   - [Translation Workflow](#translation-workflow)
   - [i18n-state-manager](#i18n-state-manager)

---

# Getting Started

TaskNotes is a task and note management plugin for Obsidian that follows the "one note per task" principle. Each task is a Markdown file with structured metadata in YAML frontmatter.

## Requirements

TaskNotes requires Obsidian 1.10.1 or later and depends on the Bases core plugin. Before you begin, open Obsidian Settings and confirm Bases is enabled under Core Plugins.

## 1. Install and Enable

Install TaskNotes from Community Plugins in Obsidian settings, then enable it. If Bases is still disabled, enable it right away so TaskNotes views can open correctly.

## 2. Create Your First Task

Press `Ctrl+P` (or `Cmd+P` on macOS), run **TaskNotes: Create new task**, fill in the modal, and save. If you prefer inline workflows, start with a checkbox like `- [ ] Buy groceries` and convert it using the inline task command.

## 3. Open the Task List

Open your first view from the TaskNotes ribbon icon or by running **TaskNotes: Open tasks view** from the command palette. This opens the default Task List `.base` file inside `TaskNotes/Views`.

## 4. Explore

Use **Core Concepts** to understand the data model, **Features** for workflow capabilities, **Views** for interface behaviour, and **Settings** to tune TaskNotes for your vault.

---

# Core Concepts

TaskNotes follows the "one note per task" principle, where each task lives as a separate Markdown note with structured metadata in YAML frontmatter.

## The Note-Per-Task Approach

Individual Markdown notes replace centralized databases or proprietary formats. Each task file can be read, edited, and backed up with any text editor or automation tool.

### Task Structure

A TaskNotes task is a standard Markdown file with YAML frontmatter:

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

Key points to review:
- Revenue projections
- Budget allocations

## Meeting Notes

Discussion with finance team on 2025-01-10...
```

The frontmatter contains structured, queryable properties. The note body holds freeform content—research findings, meeting notes, checklists, or links to related documents.

### Obsidian Integration

Since tasks are proper notes, they work with Obsidian's core features:

- **Backlinks:** See which notes reference a task
- **Graph View:** Visualize task relationships and project connections
- **Tags:** Use Obsidian's tag system for additional categorization
- **Search:** Find tasks using Obsidian's search
- **Links:** Reference tasks from daily notes, meeting notes, or project documents

This approach creates many small files. TaskNotes stores tasks in a configurable folder (default: `TaskNotes/Tasks/`) to keep them organized. In practice, this lets TaskNotes fit into existing vault habits instead of replacing them. You keep using normal note workflows, and TaskNotes adds structure, filtering, and commands on top.

## YAML Frontmatter

Task properties are stored in YAML frontmatter, a standard format with broad tool support. Treat frontmatter as the machine-readable layer and the note body as the human-readable layer. TaskNotes automations and Bases filters rely on frontmatter; your project notes and context stay in the body.

### Property Types

| Type | Example | Description |
| --- | --- | --- |
| Text | `title: Buy groceries` | Single text value |
| List | `tags: [work, urgent]` | Multiple values |
| Date | `due: 2025-01-15` | ISO 8601 date format |
| DateTime | `scheduled: 2025-01-15T09:00` | Date with time |
| Link | `projects: ["[[Project A]]"]` | Obsidian wikilinks |
| Number | `timeEstimate: 60` | Numeric values (minutes) |

### Field Mapping

Property keys are configurable. If your vault uses `deadline` instead of `due`, you can map TaskNotes to use your existing field names without modifying your files.

### Custom Fields

Add any frontmatter property to your tasks. User-defined fields work in filtering, sorting, and templates. Define custom fields in `Settings -> TaskNotes -> Task Properties` to include them in task modals and views.

## Bases Integration

TaskNotes v4 uses Obsidian's Bases core plugin for its main views. Bases provides:

- **Filtering:** Query tasks using AND/OR conditions
- **Sorting:** Order tasks by any property
- **Grouping:** Organize tasks by status, priority, project, or custom fields
- **Views:** Task List, Kanban, Calendar, and Agenda are all Bases views

Views are stored as `.base` files in `TaskNotes/Views/`. These files contain YAML configuration that defines the view's query and display settings. You can duplicate, modify, or create new views by editing these files. This makes view behavior inspectable and predictable. If a task appears in the wrong place, you can open the `.base` file and see exactly which filter or grouping rule produced that result.

### Enabling Bases

Bases is a core plugin included with Obsidian 1.10.1+:

1. Open `Settings -> Core Plugins`
2. Enable "Bases"
3. TaskNotes views will now function

---

# Features

TaskNotes includes task organization, time tracking, and calendar integration features.

## Features Overview

TaskNotes gives each task a structured set of properties, including status, priority, due and scheduled dates, tags, contexts, and optional estimates. Because these values live in frontmatter, they stay readable and portable while still powering advanced filtering and grouping in Bases.

Reminders can be relative (for example, "3 days before due") or absolute, and completed tasks can be archived automatically to keep active work surfaces focused.

TaskNotes uses Obsidian's Bases engine for filtering, sorting, and grouping. Each view is a `.base` file, so you can inspect or edit its query logic directly instead of relying on hidden plugin state.

Inline task features let you work from normal notes without context switching. Task links can display interactive cards, checkboxes can be converted into full task notes, and project notes can surface subtasks and dependency relationships in place.

Natural language parsing supports date, priority, and context extraction across multiple languages, which helps keep fast capture while preserving structured data.

Time tracking records work sessions per task, and Pomodoro mode supports focused intervals with break handling. Over time, the statistics views help you compare estimated versus actual effort and spot trends in workload distribution.

TaskNotes supports bidirectional OAuth sync with Google Calendar and Microsoft Outlook, plus read-only ICS subscriptions for external feeds.

User fields let you extend the core model with vault-specific metadata like client, energy level, billing code, or review state. Once added, these fields become available in filters, sorting, templates, and formulas.

Beyond calendar sync, TaskNotes includes an HTTP API and webhook support for automation workflows, external dashboards, or custom tooling.

---
## Task Reminders
TaskNotes reminders use iCalendar `VALARM` semantics and support both relative and absolute reminder types.

The reminders system is designed to support both habit-like workflows ("always remind me 15 minutes before") and one-off commitments ("alert me exactly at this date and time"). Most users mix both styles depending on the task.

## Reminder Types

### Relative Reminders

Relative reminders trigger from `due` or `scheduled` dates.

Use relative reminders when you want reminder behavior to stay consistent even when task dates change.

Examples:

- 15 minutes before due date
- 1 hour before scheduled date
- 2 days before due date
- 30 minutes after scheduled date

### Absolute Reminders

Absolute reminders trigger at a fixed date/time.

Use absolute reminders when the reminder itself is tied to a specific moment, independent of task rescheduling.

Examples:

- October 26, 2025 at 9:00 AM
- Tomorrow at 2:30 PM
- Next Monday at 10:00 AM

## Adding Reminders

You can add reminders from:

1. **Task Creation Modal**
2. **Task Edit Modal**
3. **Task Cards** (bell icon)
4. **Reminder field context menu**

From a workflow perspective, task cards and context menus are fastest for quick reminders, while task modals are better for reviewing multiple reminders on the same task.

![Task edit modal](https://tasknotes.dev/assets/feature-task-modal-edit.png)

### Quick Reminder Options

Common shortcuts are available for both due and scheduled anchors, such as:

- 5 minutes before
- 15 minutes before
- 1 hour before
- 1 day before

Quick options appear only when the anchor date exists.

This prevents invalid reminder states and keeps the quick menu focused on options that can be applied immediately.

![Task context menu](https://tasknotes.dev/assets/feature-task-context-menu.png)

## Reminder Data Format

Reminders are stored in YAML frontmatter arrays.

Because reminders are stored in frontmatter, they remain portable and scriptable. You can inspect or transform reminder data with any tooling that reads Markdown + YAML.

### Relative Structure

```yaml
reminders:
  - id: "rem_1678886400000_abc123xyz"
    type: "relative"
    relatedTo: "due"
    offset: "-PT15M"
    description: "Review task details"
```

### Absolute Structure

```yaml
reminders:
  - id: "rem_1678886400001_def456uvw"
    type: "absolute"
    absoluteTime: "2025-10-26T09:00:00"
    description: "Follow up with client"
```

Field meanings:

- `id`: unique identifier
- `type`: `relative` or `absolute`
- `relatedTo`: `due` or `scheduled` (relative only)
- `offset`: ISO 8601 duration, negative before and positive after (relative only)
- `absoluteTime`: ISO 8601 timestamp (absolute only)
- `description`: optional message

You typically do not need to edit these fields manually, but understanding the structure helps when debugging automation or importing task data.

## Visual Indicators

Tasks with reminders show a bell icon on task cards.

- Solid bell indicates active reminders
- Clicking opens quick reminder actions
- Reminder UI shows task context (due/scheduled dates and reminder count)

These indicators are intended to make reminders discoverable in list-heavy views without opening every task.

## Default Reminders

Default reminders can be configured in:

`Settings -> TaskNotes -> Task Properties -> Reminders`

Defaults are applied to:

- Manual task creation
- Instant conversion
- Natural language task creation

Default reminders are useful for recurring habits, such as pre-deadline checks or day-before planning prompts.

![Task properties settings](https://tasknotes.dev/assets/settings-task-properties.png)

## Technical Notes

- Reminders follow iCalendar `VALARM` concepts with ISO 8601 offsets
- The reminder property name can be customized through field mapping

For settings-level behavior (notification channels, enable/disable state), see [Features Settings](https://tasknotes.dev/settings/features/).

---
## Task Management

This section covers task creation, properties, projects, dependencies, recurring tasks, and reminders. For the underlying architecture, see Core Concepts.

### Creating and Editing Tasks

You can create and edit tasks in a variety of ways. The primary method is through the **Task Creation Modal**, which can be accessed via the "Create new task" command or by clicking on dates or time slots in the calendar views. This modal provides an interface for setting all available task properties, including title, status, priority, and due dates.

When creating a task, the title will be automatically sanitized to remove any characters that are forbidden in filenames.

TaskNotes also supports **Natural Language Creation**, which allows you to create tasks by typing descriptions in plain English. The built-in parser can extract structured data from phrases like "Buy groceries tomorrow at 3pm @home #errands high priority."

In most workflows, users combine both approaches: fast capture with natural language, then occasional structured edits in the modal when more precision is needed.

### Auto-Suggestions in Natural Language Input

The natural language input field includes auto-suggestion functionality that activates when typing specific trigger characters:

- `@` — Shows available contexts from existing tasks
- `#` — Shows available tags from existing tasks
- `+` — Shows files from your vault as project suggestions
- `*` — Shows available status options (configurable trigger in Settings → Features)

#### Project Suggestions

When typing `+` in the natural language input, you'll see up to 20 suggestions from your vault's markdown files. The suggestions display additional information to help identify files:

```
project-alpha [title: Alpha Project Development | aliases: alpha, proj-alpha]
meeting-notes [title: Weekly Team Meeting Notes]
simple-project
work-file [aliases: work, office-tasks]
```

Project suggestions search across file names (basename without extension), frontmatter titles (using your configured field mapping), frontmatter aliases, and optional filtering by required tags, folders, and a specific frontmatter property/value defined in Settings → Appearance & UI → Project Autosuggest.

Selecting a project suggestion inserts it as `+[[filename]]`, creating a wikilink to the file while maintaining the `+` project marker that the natural language parser recognizes.

#### Enhanced Project Auto-suggester (configurable cards)

Project suggestions can display configurable multi-row cards and support smarter search. Configure up to 3 rows using a simple token syntax in Settings → Appearance & UI → Project Autosuggest.

Flags:

- `n` or `n(Label)` → show the field name/label before the value
- `s` → include this field in `+` search (in addition to defaults)

Examples:

- `"{title|n(Title)}"` → Title: Alpha Project
- `"🔖 {aliases|n(Aliases)}"` → 🔖 Aliases: alpha, proj-alpha
- `"{file.path|n(Path)|s}"` → include path in `+` search as well as display it

Search behavior: `+` search always includes file basename, title (via your field mapping), and aliases. The `|s` flag adds more searchable fields on top of the defaults. Optional fuzzy matching can be enabled in settings for broader, multi-word matches.

#### Status Suggestions

When typing the status trigger character (default `*`) in the natural language input, you'll see suggestions for all configured status options. For example, typing `*in` shows "In Progress" as a suggestion if that's one of your configured statuses.

Additionally, you can convert any line type in your notes to TaskNotes using the **Instant Conversion** feature. This works with checkboxes, bullet points, numbered lists, blockquotes, headers, and plain text lines.

### Task Properties

Tasks store their data in YAML frontmatter with properties for status, priority, dates, contexts, projects, tags, time estimates, recurrence, and reminders. Custom fields can extend this structure.

This frontmatter-first design keeps task data editable and portable while supporting consistent behavior across views and widgets.

### Projects

TaskNotes supports organizing tasks into projects using note-based linking. Projects are represented as links to actual notes in your vault, allowing you to leverage Obsidian's linking and backlinking features for project management.

This model avoids creating a separate project database. Any note can become a project anchor, and task/project relationships remain visible through normal Obsidian link tooling.

#### Project Assignment

Tasks can be assigned to one or more projects through the task creation or editing interface. When creating or editing a task, click the "Add Project" button to open the project selection modal. This modal provides fuzzy search functionality to quickly find and select project notes from your vault.

#### Project Links

Projects are stored as wikilinks in the task's frontmatter (e.g., `projects: ["[[Project A]]", "[[Project B]]"]`). These links are clickable in the task interface and will navigate directly to the project notes when clicked. Any note in your vault can serve as a project note simply by being linked from a task's projects field.

#### Organization and Filtering

Tasks can be filtered and grouped by their associated projects in all Bases-driven task views. Use the Bases filter editor to add `note.projects` conditions, and configure the grouping menu to organize Task List or Kanban boards by project. Tasks assigned to multiple projects will appear in each relevant project group, providing flexibility in project-based organization.

#### Project Indicators

TaskCards display visual indicators when tasks are used as projects. These indicators help identify which tasks have other tasks linked to them as subtasks, making project hierarchy visible at a glance.

#### Subtask Creation

Tasks can have subtasks created directly from their context menu. When viewing a task that serves as a project, you can select "Create subtask" to create a new task automatically linked to the current project.

### Dependencies

Task dependencies capture prerequisite work using RFC 9253 terminology. Dependencies are stored in frontmatter as structured objects:

```yaml
blockedBy:
  - uid: "[[Operations/Order hardware]]"
    reltype: FINISHTOSTART
    gap: P1D
```

- `uid` references the blocking task, typically through an Obsidian wikilink.
- `reltype` is stored with each dependency and defaults to `FINISHTOSTART` for dependencies created in the UI.
- `gap` is optional and uses ISO 8601 duration syntax (for example `PT4H` or `P2D`).

Whenever a dependency is added, TaskNotes updates the upstream note's `blocking` list so the reverse relationship stays synchronized. Removing a dependency automatically clears both sides.

#### Selecting dependencies in the UI

- The task creation and edit modals expose "Blocked by" and "Blocking" buttons that launch a fuzzy task selector. The picker only offers valid tasks, excludes the current note, and prevents duplicate entries.
- The task context menu provides the same selector, enabling dependency management directly from the Task List, Kanban, and calendar views.
- Task cards show a fork icon whenever a task blocks other work. Clicking it expands an inline list of downstream tasks without triggering the parent card's modal, so you can inspect dependents in place.

These controls currently create and manage finish-to-start style blockers. Advanced `reltype` values and `gap` data are preserved in frontmatter, but blocking evaluation is currently based on whether unresolved dependencies exist rather than relationship-type-specific scheduling rules.

### Automation

#### Auto-Archiving

TaskNotes can automatically archive tasks when they transition into a status that has auto-archiving enabled. This keeps completed work out of your active lists without requiring manual cleanup.

Configure auto-archiving per status from Settings → Task Properties → Task Statuses. Each status card includes an Auto-archive toggle and a Delay (minutes) input (1–1440). When you turn the toggle on for a status, any task moved into that status is queued for archiving once the delay elapses. Moving the task to a different status before the timer expires cancels the pending archive automatically.

The auto-archive queue runs in the background and persists across plugin restarts. If TaskNotes was closed while an archive was pending, the task will be archived shortly after the plugin loads again as long as it still matches the configured status.

### File Management and Templates

TaskNotes supports configurable task folder locations, filename generation patterns, archive behavior, and body templates for newly created tasks. These settings let you align task files with existing vault conventions (for example, date-based folders, project-based routing, or template-driven task note scaffolds).

---

## Inline Task Integration

TaskNotes integrates with the Obsidian editor to allow task management directly within notes. This is achieved through interactive widgets, a conversion feature for checkboxes, and natural language processing. Inline features support capture and task updates without leaving the current note.

### Task Link Overlays

When a wikilink to a task note is created, TaskNotes can replace it with an interactive Task Link Overlay. Enable or disable overlays from `Settings -> TaskNotes -> Features` (`Task link overlay`). The widget displays information about the task, such as status, priority, and due date, and allows actions like status/priority changes or opening the edit modal.

#### Widget Features

The task link overlay displays:

- **Status Dot:** Clickable circular indicator showing current task status. Click to cycle through available statuses.
- **Priority Dot:** Color-coded indicator for task priority (only shown when assigned).
- **Task Title:** Displays the task name (truncated to 80 characters). Click to open the task edit modal.
- **Date Information:** Shows due dates (calendar icon) and scheduled dates (clock icon) with clickable context menus.
- **Recurrence Indicator:** Rotating arrow icon for recurring tasks with modification options.
- **Action Menu:** Ellipsis icon (shown on hover) provides additional task actions.

#### Mode-Specific Behavior

Task link overlays work in both Live Preview and Reading modes:

- **Live Preview Mode:** Widgets hide when the cursor is within the wikilink range, allowing for easy editing.
- **Reading Mode:** Widgets display with full functionality and integrate with the reading mode typography.

The overlays support drag-and-drop to calendar views and provide keyboard shortcuts for quick navigation (`Ctrl/Cmd+Click` to open the source file).

### Create Inline Task Command

The `Create inline task` command allows you to create a new task from the current line in the editor. This command is available in the command palette. When you run the command, the current line is used as the title of the new task. The line is then replaced with a link to the new task file.

### Instant Task Conversion

The Instant Task Conversion feature transforms lines in your notes into TaskNotes files. This works with both checkbox tasks and regular lines of text. Turn the feature on or off from `Settings -> TaskNotes -> Features` (`Show convert button next to checkboxes`). When enabled, a "convert" button appears next to content in edit mode. Clicking this button creates a new task note using the line text as the title and replaces the original line with a link to the new task file.

#### Folder Configuration

By default, converted tasks are placed in the same folder as the current note (`{{currentNotePath}}`). You can change this behavior in `Settings -> TaskNotes -> General` (`Folder for converted tasks`):

- Leave empty: Uses your default tasks folder (configured in the same section)
- `{{currentNotePath}}`: Places tasks in the same folder as the note you're editing (default)
- `{{currentNoteTitle}}`: Creates a subfolder named after the current note
- Custom path: Specify any folder path (e.g., `TaskNotes/Converted`)

#### Supported Line Types

The conversion feature works with checkboxes (`- [ ] Task description`), bullet points (`- Some task idea`), numbered lists (`1. Important item`), blockquoted content (`> Task in callout`), plain text lines (`Important thing to do`), and mixed formats (`> - [ ] Task in blockquote`).

#### Content Processing

When converting lines, special characters like `>`, `#`, `-` are automatically removed from the task title. Original formatting is preserved in the note. Task metadata is extracted from checkbox tasks (due dates, priorities, etc.). Natural language processing can extract dates and metadata from plain text (if enabled). Conversion preserves surrounding formatting, including callouts, outlines, and nested lists.

### Bulk Task Conversion

The Bulk Task Conversion command converts all checkbox tasks in the current note to TaskNotes in a single operation. This command is available in the command palette as "Convert all tasks in note to TaskNotes".

The command scans the entire current note for checkbox tasks (`- [ ]`, `* [ ]`, `1. [ ]`, etc.), includes tasks inside blockquotes, applies the same enhanced conversion logic as instant task conversion, creates individual TaskNote files for each task, replaces the original checkboxes with links to the new task files, and preserves original indentation and formatting.

> **Important Considerations:** This command modifies note content permanently. Before using: create a backup of your note if it contains important data, review the tasks to ensure they should become individual TaskNotes, expect processing time for notes with many tasks, and avoid editing the note while conversion is running.

> **Performance:** Small notes (1-10 tasks): Near-instant. Medium notes (10-50 tasks): 2-5 seconds. Large notes (50+ tasks): 10+ seconds.

### Relationships Widget

New in v4: The Relationships Widget consolidates what were previously three separate widgets (project subtasks, task dependencies, and blocking tasks) into a single dynamic interface.

The widget appears in task notes and automatically displays up to four tabs based on available relationship data:

- **Subtasks Tab (Kanban):** Shows tasks that reference the current note as a project. Uses Kanban layout for visual task management.
- **Projects Tab (List):** Shows projects that the current task belongs to. Uses list layout.
- **Blocked By Tab (List):** Shows tasks that are blocking the current task. Uses list layout.
- **Blocking Tab (Kanban):** Shows tasks that the current task is blocking. Uses Kanban layout.

#### Automatic Tab Management

Tabs automatically show or hide based on the presence of relationship data. If a task has no subtasks, the Subtasks tab does not appear. If there are no blocking relationships, those tabs remain hidden.

#### Features

The widget embeds the `TaskNotes/Views/relationships.base` view directly in the editor. Every filter, grouping rule, or property shown in that `.base` file is exactly what appears inside the widget, so you can customize the experience by editing the file just like any other Bases view.

Additional behavior: collapsible interface with remembered state, persistent grouping, task details display (status, priority, due date, etc.), and real-time updates when tasks are added, modified, or deleted via Bases views.

#### Configuration

Enable or disable the widget in `Settings -> TaskNotes -> Appearance` (`Show relationships widget`). Position the widget at the top (after frontmatter) or bottom of the note using the Relationships Position setting.

#### Expandable Subtasks Chevron

Tasks with subtasks can display an expand/collapse chevron that toggles subtask visibility. The chevron can be positioned on the Right (default, hover to show) or on the Left (always visible, matches group chevrons). Configure this in `Settings -> TaskNotes -> Appearance` (`Subtask chevron position`).

#### Migration from v3

In v3, TaskNotes provided three separate widgets controlled by individual settings (`showProjectSubtasks`, `showTaskDependencies`, `showBlockingTasks`). These are replaced in v4 by `showRelationships` and `relationshipsPosition`. If you had project subtasks enabled in v3, the relationships widget is enabled automatically after upgrading to v4. The underlying Bases file changed from `TaskNotes/Views/project-subtasks.base` to `TaskNotes/Views/relationships.base`. Run the Create default files action in `Settings -> TaskNotes -> Integrations` if `relationships.base` is missing.

### Natural Language Processing

TaskNotes includes a Natural Language Processor (NLP) that parses task descriptions to extract structured data. This allows for task creation from conversational language, such as "Prepare quarterly report due Friday #work high priority," which would automatically set the due date, tag, and priority.

The NLP engine supports multiple languages, including English, Spanish, French, German, Italian, Japanese, Dutch, Portuguese, Russian, Swedish, Chinese, and Ukrainian.

#### Supported Syntax

The NLP engine recognizes:

- **Tags and Contexts:** `#tag` and `@context` syntax (triggers are customizable).
- **Projects:** `+project` for simple projects or `+[[Project Name]]` for projects with spaces.
- **Priority Levels:** Keywords like "high," "normal," and "low". Also supports a trigger character (default: `!`).
- **Status Assignment:** Keywords like "open," "in-progress," and "done". Also supports a trigger character (default: `*`).
- **Dates and Times:** Phrases like "tomorrow," "next Friday," and "January 15th at 3pm".
- **Time Estimates:** Formats like "2h," "30min," and "1h30m".
- **Recurrence Patterns:** Phrases like "daily," "weekly," and "every Monday".
- **User-Defined Fields:** Custom fields can be assigned using configured triggers (e.g., `effort: high`). Supports quoted values for multi-word entries.

#### Rich Markdown Editor

New in v4: The task creation modal uses a rich CodeMirror markdown editor instead of a plain textarea. Keyboard shortcuts include `Ctrl/Cmd+Enter` to save the task and `Esc` or `Tab` to navigate out of the editor.

#### Customizable Triggers

New in v4: Triggers for NLP properties can be customized in `Settings -> TaskNotes -> Features` (`NLP Triggers`). You can configure trigger characters or strings for tags (default: `#`), contexts (default: `@`), projects (default: `+`), status (default: `*`), priority (default: `!`, disabled by default), and user-defined fields (default: `fieldname:`). Triggers support up to 10 characters and can include trailing spaces.

#### Autocomplete

New in v4: When typing a trigger in the NLP editor, an autocomplete menu appears with available values. Navigate suggestions with arrow keys, select with `Enter` or `Tab`. Autocomplete works for tags, contexts, projects, status, priority, and user-defined fields. Tag autocomplete uses Obsidian's native tag suggester when using the `#` trigger. For user fields with multi-word values, wrap the value in quotes (e.g., `effort: "very high"`).

---

## Calendar Integration

TaskNotes provides calendar integration through OAuth-connected calendar services, two Bases-powered calendar views, and read-only ICS calendar subscriptions.

### OAuth Calendar Integration

TaskNotes supports bidirectional synchronization with Google Calendar and Microsoft Outlook using OAuth authentication. This integration allows you to view external calendar events alongside your tasks and sync changes back to the calendar provider.

#### Supported Providers

- **Microsoft Outlook** — OAuth 2.0 authentication with access to calendars in your Microsoft 365 or Outlook.com account
- **Google Calendar** — OAuth 2.0 authentication with access to all calendars in your Google account

#### Setup Requirements

OAuth calendar integration requires creating an OAuth application with your calendar provider. This process takes approximately 15 minutes per provider. You will need to enter credentials in TaskNotes settings (`Settings -> TaskNotes -> Integrations`, OAuth calendar section), obtain client ID and client secret, configure redirect URIs and scopes, and create an OAuth application in Google Cloud Console or Microsoft Azure Portal.

#### Synchronization Behavior

Access tokens are automatically refreshed when expired. Per-calendar visibility toggles allow selective display of calendars. Dragging calendar events to new dates/times updates the event in the calendar provider. Events are also fetched when local changes occur (task creation, updates, rescheduling). Events are fetched automatically every 15 minutes.

#### Token Management

TaskNotes stores OAuth access tokens and refresh tokens locally. Tokens are refreshed automatically before expiration. You can revoke access at any time through the integrations settings.

### Calendar Views

TaskNotes provides Calendar and Mini Calendar views that display tasks alongside OAuth calendar events and ICS subscriptions. Both views support drag-and-drop scheduling.

### Time Entry Editor

TaskNotes includes a time entry editor for tracking time spent on tasks. Time entries are created and managed through the Calendar View.

#### Creating Time Entries

To create a time entry on the Calendar View:

1. Click and drag on a time slot in the calendar to select a time range
2. When the selection menu appears, choose "Create time entry"
3. Choose a task in the task selector modal
4. A time entry is created for that task with the selected start/end range

Time entries are always associated with a specific task and stored in that task's frontmatter. Multiple time entries can exist for one task.

#### Managing Time Entries

The time entry editor modal provides functions to see the total time tracked across all entries for a task, delete time entries, edit the start time, end time, and duration of time entries, and view all time entries for a task. Access the time entry editor by clicking an existing time entry in the calendar.

### ICS Calendar Subscriptions

TaskNotes can subscribe to external calendar feeds using the iCalendar (ICS) format. This provides read-only access to events from calendar services. ICS subscriptions differ from OAuth calendar integration in that they are read-only—dragging ICS events to new dates does not update the source calendar.

Add and manage ICS subscriptions from `Settings -> TaskNotes -> Integrations` (Calendar Subscriptions section).

### Time Blocking

The Calendar View supports time blocking for scheduling dedicated work periods. To create a time block, click and drag on a time slot in the calendar to select a time range, then select "Create timeblock" from the menu (this option only appears if timeblocking is enabled in settings).

Time blocks are stored in the frontmatter of daily notes and can be linked to specific tasks. This differs from time entries, which track actual time spent and are stored in task frontmatter rather than daily notes.

Enable time blocking under `Settings -> TaskNotes -> Features` (Timeblocking section).

---

## ICS Calendar Event Integration

TaskNotes can use ICS calendar events to create notes and tasks directly from calendar entries. ICS integration creates linked notes and tasks from event data without manual re-entry.

### Overview

The ICS integration allows you to create notes from calendar events with customizable templates, generate tasks from events with proper scheduling and context, link existing vault content to calendar events, view detailed information about calendar events, and maintain relationships between events and created content.

### Event Information Modal

When you interact with a calendar event in TaskNotes, an information modal displays event details and available actions.

#### Event Details

Event title and description, start and end times (formatted according to your locale), location information, source calendar name, and event URL (if available).

#### Related Content

The modal shows a list of existing notes and tasks that are linked to the calendar event. Content is automatically categorized as **Note** (files without the task tag) or **Task** (files containing the configured task tag). The relationship is maintained through the ICS Event ID field in the content's frontmatter.

#### Available Actions

- **Create Note** — Opens a creation dialog for generating a new note from the event data.
- **Create Task** — Creates a task immediately using the event information with default settings.
- **Link Note** — Opens a file selection dialog to link an existing note to the calendar event.
- **Refresh** — Reloads the list of related content to reflect recent changes.

### Note Creation from Events

#### Basic Settings

Title defaults to combining event title and date, but can be modified. Folder uses the default ICS note folder if configured. Template is optional for structuring note content.

#### Template Usage

When a template is specified, template content replaces the default event description format, frontmatter from templates is merged with required ICS fields, standard TaskNotes template variables are also available, and the template file is processed with ICS-specific variables.

#### Default Content

Without a template, notes include event title as the main heading, formatted start and end times, location information, source calendar name, event description (if provided), and event URL (if available).

### Task Creation from Events

Tasks created from calendar events include relevant event data:

- **Scheduled Date and Time:** Tasks are scheduled using the event's start time as an ISO timestamp
- **Title:** Uses the event title
- **Status:** Set to the default task status configured in settings
- **Priority:** Set to the default task priority
- **Contexts:** Event location is added as a context (if provided)
- **Time Estimate:** Calculated from event duration (if start and end times are available)
- **Tags:** Includes the ICS event tag and any default task tags

### Linking Existing Content

You can establish connections between existing vault content and calendar events. Select an existing markdown file from your vault, the file's frontmatter is updated to include the event ID, and the connection appears in the related content list. Content can be linked to multiple events (stored as an array), and multiple pieces of content can be linked to a single event.

### Field Mapping Integration

#### ICS Event ID Field

Default field name is `icsEventId`. Stores the unique identifier connecting content to calendar events. Values are stored as arrays to support multiple event associations. Field name can be customized through field mapping settings.

#### ICS Event Tag Field

Default tag is `ics_event`. Tag automatically applied to content created from events. Used to identify ICS-related content throughout the system. Can be customized through field mapping settings.

### Template Variables

Templates used for ICS content creation have access to event-specific variables:

- `{{icsEventTitle}}` — Event title
- `{{icsEventStart}}` — Start date and time (ISO format)
- `{{icsEventEnd}}` — End date and time (ISO format)
- `{{icsEventLocation}}` — Event location
- `{{icsEventDescription}}` — Event description
- `{{icsEventUrl}}` — Event URL
- `{{icsEventSubscription}}` — Calendar subscription name
- `{{icsEventId}}` — Unique event identifier (UUID)

All standard TaskNotes template variables (`{{title}}`, `{{date}}`, `{{time}}`, `{{priority}}`, `{{status}}`, `{{contexts}}`, etc.) remain available.

### Configuration

ICS integration settings are located under `Settings -> TaskNotes -> Integrations`. Configure default templates for consistent content creation from events, set destination folders (supporting template variables for dynamic organization like `Meetings/{{monthName}}` or `Events/{{year}}/{{icsEventTitleKebab}}`), and configure filename formats using the standard TaskNotes filename generation.

---

## Recurring Tasks

TaskNotes recurring tasks use RFC 5545 RRule strings with `DTSTART` support and dynamic next-occurrence scheduling. The model separates recurrence patterns from the next planned instance.

If you are new to recurring tasks in TaskNotes, think of the recurrence rule as the long-term plan and the `scheduled` field as the next concrete commitment. Most day-to-day editing affects `scheduled`, while recurrence editing changes the plan itself.

### Core Concepts

Recurring tasks operate on two independent levels:

1. **Next Occurrence:** The specific date/time when you plan to work on the next instance (controlled by the `scheduled` field)
2. **Recurring Pattern:** Defines when pattern instances appear (controlled by `DTSTART` in the recurrence rule)

This separation lets you reschedule the next occurrence without changing the pattern.

### Setting Up Recurring Tasks

In practice, setup is usually a two-step flow: choose a pattern, then check whether the next scheduled occurrence matches how you actually want to execute the next instance.

#### Creating Recurrence Patterns

You can create recurring tasks through a Custom Recurrence Modal with date/time pickers and RRule configuration, Preset Options such as daily, weekly, or monthly, or the Recurrence Context Menu in task modals for presets or custom options.

#### Required Components

Recurring tasks require a **Scheduled Date** (next occurrence date, independent from the pattern) and a **Recurrence Rule** (RRule string with `DTSTART`).

#### DTSTART Integration

`DTSTART` is the anchor for pattern generation. It controls where the rule begins and, when time is included, the default time for future pattern instances.

- Date and time: `DTSTART:20250804T090000Z;FREQ=DAILY`
- Date-only: `DTSTART:20250804;FREQ=DAILY`

### Recurring Task Due Date

When a recurring task is completed, `scheduled` advances to the next occurrence. By default, `due` does not change.

Enable `Maintain due date offset in recurring tasks` in Settings → TaskNotes → Features → Recurring Tasks to preserve due/scheduled spacing.

Example: Recurrence weekly, Due: `2025-01-03`, Scheduled: `2025-01-01`. If the task advances to `scheduled: 2025-01-08`, the due date becomes `2025-01-10` when this setting is enabled.

### Recurrence Pattern Examples

```
DTSTART:20250804T090000Z;FREQ=DAILY
→ Daily at 9:00 AM, starting August 4, 2025

DTSTART:20250804T140000Z;FREQ=WEEKLY;BYDAY=MO,WE,FR
→ Monday, Wednesday, Friday at 2:00 PM, starting August 4, 2025

DTSTART:20250815;FREQ=MONTHLY;BYMONTHDAY=15
→ 15th of each month (all-day), starting August 15, 2025

DTSTART:20250801T100000Z;FREQ=MONTHLY;BYDAY=-1FR
→ Last Friday of each month at 10:00 AM, starting August 1, 2025
```

### Dynamic Scheduled Dates

The `scheduled` field automatically tracks the next uncompleted occurrence: it can be manually rescheduled independently, recalculates when the rule changes, advances when occurrences are completed, and is initially set to the `DTSTART` date.

#### Example Behavior

```yaml
# Initial state
recurrence: "DTSTART:20250804T090000Z;FREQ=DAILY"
scheduled: "2025-08-04T09:00"
complete_instances: []

# After completing Aug 4
recurrence: "DTSTART:20250804T090000Z;FREQ=DAILY"
scheduled: "2025-08-05T09:00"
complete_instances: ["2025-08-04"]

# After manually rescheduling next occurrence
recurrence: "DTSTART:20250804T090000Z;FREQ=DAILY"
scheduled: "2025-08-05T14:30"
complete_instances: ["2025-08-04"]
```

### Calendar Drag and Drop

Recurring tasks can show **pattern instances** (dashed border) — dragging updates `DTSTART` and future pattern instances — and the **next occurrence** (solid border) — dragging updates only `scheduled`.

### Completion Tracking

Each occurrence can be completed independently (task cards, calendar menus, task edit modal completion calendar). Completed instances are stored in `complete_instances: ["2025-08-04", "2025-08-06", "2025-08-08"]`. When completion changes, `scheduled` updates to the next uncompleted instance.

### Flexible Scheduling

TaskNotes intentionally allows off-pattern scheduling so recurring tasks can absorb real-world disruptions without rewriting the entire recurrence rule. The next occurrence can be far ahead while pattern continues unchanged, at a different time than pattern instances, outside the pattern day, or before `DTSTART`.

### Timezone Handling

Recurring task logic uses a UTC anchor approach. `DTSTART` dates are interpreted as UTC anchors, pattern generation uses UTC dates, display adapts to local timezone, and this prevents common off-by-one date issues.

### Backward Compatibility

Legacy recurrence objects are converted to RRule format. Legacy RRule strings without `DTSTART` continue to work using `scheduled` as anchor. Existing tasks continue to function without migration steps.

---

## Time Management

TaskNotes includes features for time tracking and productivity, such as a time tracker and a Pomodoro timer.

### Time Tracking

TaskNotes has a time tracker to record the time spent on each task. Time tracking information is stored in the `timeEntries` array within each task's YAML frontmatter. Each time entry includes a start time and an end time.

The time tracking interface includes controls to start and stop tracking in task views and task cards. TaskNotes prevents duplicate active sessions on the same task. Active sessions on different tasks can exist at the same time, and total time spent on each task is calculated from completed sessions.

#### Auto-Stop Time Tracking

TaskNotes can automatically stop time tracking when a task is marked as completed. This feature ensures that time tracking data accurately reflects work completion without requiring manual timer management.

The auto-stop feature works by monitoring task status changes across all views and interfaces. When a task's status changes from any non-completed state to a completed state (as defined by the custom status configuration), any active time tracking session for that task is automatically terminated.

Configuration Options (under `Settings -> TaskNotes -> Features`, Time Tracking section):

- **Auto-stop tracking** — Enable or disable the automatic stopping behavior (enabled by default)
- **Completion notification** — Show a notice when auto-stop occurs (disabled by default)

The feature integrates with the custom status system, so completion detection respects your configured workflow statuses rather than relying on hardcoded completion states.

### Pomodoro Timer

TaskNotes also includes a Pomodoro timer, which is a tool for time management that uses a timer to break down work into intervals, separated by short breaks. The Pomodoro timer in TaskNotes has a dedicated view with controls to start, stop, and reset the timer.

When a task is associated with a Pomodoro session, the time is automatically recorded in the task's time tracking data upon completion of the session.

### Productivity Analytics

The Pomodoro Stats View provides analytics and historical data about your Pomodoro sessions. This includes a history of completed sessions, as well as metrics like completion rates and total time spent on tasks. The data can be visualized to show productivity patterns over time.

---

## User Fields

TaskNotes allows you to define your own custom fields for tasks. This feature allows you to add custom data to your tasks and use it for filtering, sorting, and grouping. User fields can store workflow-specific metadata such as owner, effort class, client, or review stage.

### Creating User Fields

User fields are created in the TaskNotes settings, under the "Task Properties" tab. To create a new user field, click the "Add new user field" button.

Each user field has the following properties:

**Type:** The data type of the field. Supported types: Text (a single line of text), Number (a numeric value, supports ranges in filters and sorting), Boolean (a true/false value stored as a checkbox in the task modal), Date (a date), and List (a list of values).

**Default Value (optional):** A default value to pre-fill when creating new tasks. The input format depends on the field type: Text (enter the default text value), Number (enter the default number), Boolean (toggle to set default state), Date (select from presets: None, Today, Tomorrow, or Next Week), List (enter comma-separated default values).

### File Suggestion Filtering (Advanced)

When using text or list type custom fields, you can configure autosuggestion filters to control which files appear in the autocomplete dropdown when you type `[[` in the field.

#### Filter Options

- **Required tags:** Only show files that have ANY of these tags (comma-separated). Supports hierarchical tags.
- **Include folders:** Only show files in these folders (comma-separated). Supports nested folders.
- **Required property key:** Only show files that have this frontmatter property.
- **Required property value:** Expected value for the property (optional). Leave empty to match any value.

When filters are configured, a "Filters On" badge with a funnel icon appears next to the section title.

#### Filter Behavior

Filters only affect autocomplete (not actual field value or validation). No filters = all files. Empty filters are ignored. All filters are combined with AND logic.

#### Example Configurations

**Assignee Field (People Only):**
```
Display Name: Assignee
Property Key: assignee
Type: List
Autosuggestion filters:
  Required tags: person
  Include folders: People/
```

**Project Field (Active Projects):**
```
Display Name: Project
Property Key: project
Type: Text
Autosuggestion filters:
  Required tags: project
  Required property key: status
  Required property value: active
```

### Using User Fields

Once you have created a user field, it will be available in Task Modals, Bases Filters (e.g., `note.effort == "high"`), Sorting (Bases sort menu), and Grouping (Bases group menu for swimlanes or list groupings).

### Frontmatter

User field data is stored in the frontmatter of the task note. The property name you define for the user field is used as the key in the frontmatter:

```yaml
---
my_field: value
---
```

---

## Template Variables Reference

TaskNotes supports template variables for dynamic content generation in body templates, folder paths, and filenames. Variables use the `{{variableName}}` syntax and are replaced with actual values when content is created.

### Overview

Template variables are available in three contexts: **Body templates** (content templates for task and note files), **Folder templates** (dynamic folder paths for file organization), and **Filename templates** (dynamic filename generation). Not all variables are available in every context.

### Task Properties

| Variable | Description | Body | Folder | Example |
| --- | --- | --- | --- | --- |
| `{{title}}` | Task title | Yes | Yes | `My Task` |
| `{{titleLower}}` | Title in lowercase | Yes | Yes | `my task` |
| `{{titleUpper}}` | Title in uppercase | Yes | Yes | `MY TASK` |
| `{{titleSnake}}` | Title in snake_case | Yes | Yes | `my_task` |
| `{{titleKebab}}` | Title in kebab-case | Yes | Yes | `my-task` |
| `{{titleCamel}}` | Title in camelCase | Yes | Yes | `myTask` |
| `{{titlePascal}}` | Title in PascalCase | Yes | Yes | `MyTask` |
| `{{priority}}` | Task priority value | Yes | Yes | `high` |
| `{{priorityShort}}` | First character of priority (uppercase) | Yes | Yes | `H` |
| `{{status}}` | Task status value | Yes | Yes | `active` |
| `{{statusShort}}` | First character of status (uppercase) | Yes | Yes | `A` |
| `{{context}}` | First context from contexts array | No | Yes | `work` |
| `{{contexts}}` | All contexts (comma-separated in body, `/` in folder) | Yes | Yes | `work, home` or `work/home` |
| `{{project}}` | First project from projects array | No | Yes | `ProjectA` |
| `{{projects}}` | All projects joined by `/` | No | Yes | `ProjectA/ProjectB` |
| `{{dueDate}}` | Task due date | Yes | Yes | `2025-01-15` |
| `{{scheduledDate}}` | Task scheduled date | Yes | Yes | `2025-01-10` |

### Body Template Only

| Variable | Description | Example |
| --- | --- | --- |
| `{{details}}` | User-provided details/description | `Task description text` |
| `{{parentNote}}` | Parent note name/path where task was created | `Projects/MyNote` |
| `{{tags}}` | Task tags (comma-separated) | `urgent, review` |
| `{{hashtags}}` | Task tags as space-separated hashtags | `#urgent #review` |
| `{{timeEstimate}}` | Time estimate in minutes | `30` |

### Date and Time

| Variable | Description | Format | Example |
| --- | --- | --- | --- |
| `{{date}}` | Full current date | `YYYY-MM-DD` | `2025-01-07` |
| `{{year}}` | Current year | `YYYY` | `2025` |
| `{{shortYear}}` | Short year | `YY` | `25` |
| `{{month}}` | Current month | `MM` | `01` |
| `{{day}}` | Current day | `DD` | `07` |
| `{{monthName}}` | Full month name | — | `January` |
| `{{monthNameShort}}` | Abbreviated month name | — | `Jan` |
| `{{dayName}}` | Full day name | — | `Tuesday` |
| `{{dayNameShort}}` | Abbreviated day name | — | `Tue` |
| `{{week}}` | Week number of year | `WW` | `02` |
| `{{quarter}}` | Quarter of year | `Q` | `1` |
| `{{shortDate}}` | Compact date | `YYMMDD` | `250107` |

### Time Variables

| Variable | Description | Format | Example |
| --- | --- | --- | --- |
| `{{time}}` | Current time (compact) | `HHmmss` | `143052` |
| `{{time24}}` | 24-hour time | `HH:mm` | `14:30` |
| `{{time12}}` | 12-hour time with AM/PM | `hh:mm a` | `02:30 PM` |
| `{{hour}}` | Current hour (24-hour) | `HH` | `14` |
| `{{hourPadded}}` | Hour with leading zero | `HH` | `14` |
| `{{hour12}}` | Hour in 12-hour format | `hh` | `02` |
| `{{minute}}` | Current minute | `mm` | `30` |
| `{{second}}` | Current second | `ss` | `52` |
| `{{ampm}}` | AM/PM indicator | `a` | `PM` |

### Timestamps

| Variable | Description | Format | Example |
| --- | --- | --- | --- |
| `{{timestamp}}` | Date and time combined | `YYYY-MM-DD-HHmmss` | `2025-01-07-143052` |
| `{{dateTime}}` | Date and time (no seconds) | `YYYY-MM-DD-HHmm` | `2025-01-07-1430` |
| `{{unix}}` | Unix timestamp (seconds) | — | `1736264852` |
| `{{unixMs}}` | Unix timestamp (milliseconds) | — | `1736264852000` |
| `{{milliseconds}}` | Current milliseconds | `SSS` | `123` |
| `{{ms}}` | Milliseconds (alias) | `SSS` | `123` |

### Timezone

| Variable | Description | Example |
| --- | --- | --- |
| `{{timezone}}` | Timezone offset | `+01:00` |
| `{{timezoneShort}}` | Short timezone offset | `+0100` |
| `{{utcOffset}}` | UTC offset | `+01:00` |
| `{{utcOffsetShort}}` | Short UTC offset | `+0100` |
| `{{utcZ}}` | UTC Z indicator | `Z` |

### Unique Identifiers

| Variable | Description | Example |
| --- | --- | --- |
| `{{zettel}}` | Zettelkasten-style ID (date + seconds since midnight in base36) | `250107abc` |
| `{{nano}}` | Unique nano ID (timestamp + random string) | `1736264852000x7k2m` |

### ICS Calendar Event Variables

| Variable | Description | Body | Folder |
| --- | --- | --- | --- |
| `{{icsEventTitle}}` | Event title | Yes | Yes |
| `{{icsEventTitleLower}}` | Event title lowercase | No | Yes |
| `{{icsEventTitleUpper}}` | Event title uppercase | No | Yes |
| `{{icsEventTitleSnake}}` | Event title in snake_case | No | Yes |
| `{{icsEventTitleKebab}}` | Event title in kebab-case | No | Yes |
| `{{icsEventTitleCamel}}` | Event title in camelCase | No | Yes |
| `{{icsEventTitlePascal}}` | Event title in PascalCase | No | Yes |
| `{{icsEventStart}}` | Event start time (ISO format) | Yes | No |
| `{{icsEventEnd}}` | Event end time (ISO format) | Yes | No |
| `{{icsEventLocation}}` | Event location | Yes | Yes |
| `{{icsEventDescription}}` | Event description | Yes | Yes |
| `{{icsEventUrl}}` | Event URL | Yes | No |
| `{{icsEventSubscription}}` | Calendar subscription name | Yes | No |
| `{{icsEventId}}` | Unique event identifier (UUID) | Yes | No |

### Inline Task Conversion Variables

| Variable | Description | Example |
| --- | --- | --- |
| `{{currentNotePath}}` | Path to the current note's folder | `Projects/Notes` |
| `{{currentNoteTitle}}` | Title/name of the current note | `Meeting Notes` |

### Examples

#### Body Template

```yaml
---
created: {{date}}
priority: {{priority}}
status: {{status}}
---

# {{title}}

{{details}}

Created from: {{parentNote}}
Tags: {{hashtags}}
```

#### Folder Template

Organize tasks by project and status: `Tasks/{{project}}/{{status}}` → Result: `Tasks/MyProject/active`

Organize by date hierarchy: `Daily/{{year}}/{{month}}/{{day}}` → Result: `Daily/2025/01/07`

Organize ICS events by year and title: `Events/{{year}}/{{icsEventTitleKebab}}` → Result: `Events/2025/team-meeting`

#### Filename Template

Using Zettelkasten ID: `{{zettel}}-{{titleKebab}}` → Result: `250107abc-my-task.md`

Using timestamp: `{{shortDate}}-{{title}}` → Result: `250107-My Task.md`

### Notes

**YAML Safety:** When used in YAML frontmatter, values containing special characters (colons, brackets, quotes) are automatically quoted to prevent parsing errors.

**Folder Path Sanitization:** In folder templates, title values have filesystem-unsafe characters (`<>:"/\|?*`) replaced with underscores to ensure valid paths.

**Empty Values:** If a variable references data that isn't available (e.g., `{{project}}` when no project is set), it resolves to an empty string.

**Case Transformations:**

| Transform | Input | Output |
| --- | --- | --- |
| `titleLower` | `My Task Name` | `my task name` |
| `titleUpper` | `My Task Name` | `MY TASK NAME` |
| `titleSnake` | `My Task Name` | `my_task_name` |
| `titleKebab` | `My Task Name` | `my-task-name` |
| `titleCamel` | `My Task Name` | `myTaskName` |
| `titlePascal` | `My Task Name` | `MyTaskName` |

---

# Views

TaskNotes provides multiple views for managing tasks and tracking productivity. All task-focused views operate as `.base` files located in the `TaskNotes/Views/` directory and require Obsidian's Bases core plugin to be enabled.

## Task-Focused Views

Task-focused views are different entry points into the same underlying task notes. The **Task List View** is a common starting view for day-to-day planning because it exposes filters, sorting, and grouping in list format. When you want workflow by status, **Kanban View** organizes cards into columns and can optionally add swimlanes for an extra organizational layer. **Calendar Views** are useful when schedule and timing matter more than backlog shape, with month/week/day/year/list modes plus drag-and-drop scheduling and time-block support. **Agenda View** is a preconfigured list-oriented calendar layout designed for short-horizon planning, while **MiniCalendar View** gives a compact month heatmap and fast keyboard navigation.

## Productivity-Focused Views

**Pomodoro View** supports focused intervals directly inside Obsidian, and **Pomodoro Stats View** summarizes completed sessions so you can see pace and consistency over time.

---

## Task List View

The Task List View displays tasks in a scrollable list format with filtering, sorting, and grouping capabilities. In TaskNotes v4, this view operates as a Bases view configured through YAML. This view is optimized for high task volume and explicit filter definitions.

### Bases Architecture

Task List is implemented as a `.base` file located in `TaskNotes/Views/tasks-default.base` by default. It requires the Bases core plugin to be enabled.

When you use the "Open Tasks View" command or ribbon icon, TaskNotes opens the `.base` file configured under `Settings -> TaskNotes -> General` (`View Commands`). The default file is created automatically the first time you use the command, and you can point the command to any other `.base` file if you maintain multiple task-list layouts.

### Configuration

#### Basic Structure

```yaml
# All Tasks

views:
  - type: tasknotesTaskList
    name: "All Tasks"
    order:
      - note.status
      - note.priority
      - note.due
      - note.scheduled
      - note.projects
      - note.contexts
      - file.tags
    sort:
      - column: due
        direction: ASC
```

#### Configuration Options

- `type`: Must be `tasknotesTaskList` for Task List views
- `name`: Display name shown in the view header
- `order`: Array of property names that control which task properties are visible in the task cards
- `sort`: Array of sort criteria (by `column` and `direction`: `ASC` or `DESC`)
- `groupBy`: Optional grouping configuration (by `property` and `direction`)
- `filters`: Optional filter conditions using Bases query syntax

### Property Mapping

| TaskNotes Property | Bases Property Path | Description |
| --- | --- | --- |
| Status | `note.status` | Task status value |
| Priority | `note.priority` | Priority level |
| Due date | `note.due` | Due date/time |
| Scheduled date | `note.scheduled` | Scheduled date/time |
| Projects | `note.projects` | Associated projects |
| Contexts | `note.contexts` | Task contexts |
| Tags | `file.tags` | File tags |
| Checklist progress | `file.tasks` | Markdown checkbox progress bar |
| Time estimate | `note.timeEstimate` | Estimated duration |
| Recurrence | `note.recurrence` | Recurrence pattern |
| Blocked by | `note.blockedBy` | Blocking dependencies |
| Title | `file.name` | Task title (file name) |
| Created | `file.ctime` | File creation date |
| Modified | `file.mtime` | File modification date |

### Filtering and Sorting

#### Adding Filters

```yaml
views:
  - type: tasknotesTaskList
    name: "High Priority Tasks"
    filters:
      and:
        - note.priority == "High"
        - note.status != "Completed"
    order:
      - note.status
      - note.priority
      - note.due
```

#### Filter Operators

Bases supports `==` (equals), `!=` (not equals), `>`, `<`, `>=`, `<=` (comparison), `contains()` (substring/array membership), and boolean logic with `and` and `or`.

### Grouping

Add `groupBy` configuration to your view:

```yaml
views:
  - type: tasknotesTaskList
    name: "Tasks by Status"
    groupBy:
      property: note.status
      direction: ASC
```

Common grouping properties: `note.status`, `note.priority`, `note.contexts`, `note.projects`.

Group headers support interaction: click to expand/collapse, click on project links to navigate, hover with Ctrl to preview. Collapsed/expanded state is preserved across sessions.

### Creating Multiple Views

You can create multiple `.base` files for different task perspectives. Duplicate an existing file in `TaskNotes/Views/`, rename it, and edit the YAML configuration.

### Virtual Scrolling

The Task List View automatically enables virtual scrolling when displaying 100 or more items (tasks + group headers), providing approximately 90% memory reduction for large lists and smooth performance with unlimited task counts.

---

## Kanban View

The Kanban View displays tasks as cards organized in columns, where each column represents a distinct value of a grouped property. Kanban emphasizes state transitions and drag operations over dense list scanning.

### Configuration

Kanban views are stored as `.base` files in `TaskNotes/Views/`. The `groupBy` property determines the column structure—each unique value becomes a column in the board.

#### Core Settings (Bases)

- **Group by:** Required. Defines the property that creates columns (e.g., status, priority)
- **Sort:** Specify the order of tasks within each column
- **Filter:** Define criteria to include or exclude specific tasks
- **Data source:** Select which files or folders to include

#### Kanban-Specific Options

- **Column Order:** Managed automatically when dragging column headers
- **Show items in multiple columns:** When enabled (default), tasks with multiple values in list properties appear in each individual column
- **Hide Empty Columns:** When enabled, columns containing no tasks are hidden
- **Column Width:** Controls width in pixels (200-500px, default: 280px)
- **Swim Lane:** Optional property for horizontal grouping, creating a two-dimensional layout

### Interface Layout

#### Standard Layout

Horizontal row of columns, each with a header showing the property value and task count, a scrollable area containing task cards, and drag-and-drop functionality.

#### Swimlane Layout

When a `swimLane` property is configured, the board displays a grid layout. The horizontal axis represents columns (groupBy values), and the vertical axis represents swimlanes.

### Task Cards

Each task card displays information based on visible properties. To show checklist progress on cards, include `file.tasks` in the view `order` array. Click a card to open the task file, right-click for context menu, drag cards between columns to update properties.

### Column Operations

Drag column headers to reorder columns. Drag task cards between columns to update the `groupBy` property value. In swimlane mode, dragging a task to a different cell updates both properties. When grouping by a list property with "Show items in multiple columns" enabled, dragging modifies the list rather than replacing it.

### Performance Optimization

Virtual scrolling activates for columns or swimlane cells containing 30 or more tasks, reducing memory usage by approximately 85% and maintaining 60fps scrolling.

### Example Configuration

```yaml
---
type: query
source: TaskNotes
view: TaskNotes Kanban
views:
  - name: TaskNotes Kanban
    type: tasknotesKanban
    groupBy:
      property: task.status
    config:
      swimLane: task.priority
      columnWidth: 300
      hideEmptyColumns: true
---
```

---

## Calendar Views

TaskNotes provides two calendar-based views: the Mini Calendar and the Calendar View. Both operate as Bases views (`.base` files) and require the Bases core plugin to be enabled.

### Mini Calendar View

The Mini Calendar displays a month-based view that shows which days contain tasks or other dated notes.

#### Features

- **Date Navigation:** Click any date to open a fuzzy selector modal showing all notes associated with that date
- **Keyboard Navigation:** Navigate using arrow keys and select dates with Enter
- **Heatmap Styling:** Visual indicators show the density of tasks on each day
- **Configurable Date Property:** Set which date property to track (not limited to tasks)
- **Month Navigation:** Browse forward and backward through months

### Calendar View

The Calendar View provides multiple view modes with drag-and-drop scheduling and time-blocking capabilities.

#### View Modes

- **Month:** Month grid showing all-day and timed events
- **Week:** Week view with hourly time slots
- **Day:** Single day view with hourly breakdown
- **Year:** Annual overview showing event distribution
- **List:** Chronological list of events
- **Custom Days:** Configurable multi-day view (2-10 days)

#### Custom Days View

The Custom Days view provides a configurable multi-day calendar (2-10 days). Set the number of days via Settings > Calendar > Custom view day count. Ships with 3 days displayed by default. Useful for planning workflows that need a few days at a glance without the full week.

#### Recurring Task Support

**Visual Hierarchy:** Next Scheduled Occurrence has a solid border with full opacity. Pattern Instances have a dashed border with reduced opacity (70%).

**Drag and Drop Behavior:** Dragging the next scheduled occurrence (solid border) updates only the `scheduled` field and leaves the recurrence pattern unchanged. Dragging pattern instances (dashed border) updates the DTSTART time in the recurrence rule, changing when all future instances appear.

#### View Options

- Show scheduled, Show due, Show timeblocks, Show recurring, Show ICS events, Show time entries
- All-day slot: Show or hide the all-day event area
- **Span tasks between scheduled and due dates:** Display tasks as multi-day bars spanning from scheduled to due date (Gantt chart-style)

#### OAuth Calendar Integration

Google Calendar and Microsoft Outlook events appear alongside TaskNotes tasks. Drag and drop events to reschedule—changes sync back to the external calendar service.

### Pomodoro View

The Pomodoro View provides a timer for working in focused intervals based on the Pomodoro Technique. The timer includes controls to start, stop, and reset. You can associate a task with the timer, and the time will be automatically recorded in the task's time tracking data when the session is complete.

The **Pomodoro Stats View** provides analytics and historical data about your Pomodoro sessions, including completion rates and total time spent on tasks.

---

## Default Base Templates

TaskNotes automatically generates Bases files for its built-in views when you first open them. These templates are configured based on your TaskNotes settings.

### Default Settings Assumptions

The examples assume: visible properties (`status`, `priority`, `due`, `scheduled`, `projects`, `contexts`, `tags`, `blocked`, `blocking`), priorities (`none`, `low`, `normal`, `high`), statuses (`none`, `open`, `in-progress`, `done`), default field mapping, and tag-based task identification using `#task`.

### Included Formulas

All templates include calculated formula properties for use in views, filters, and sorting.

#### Date Calculations

| Formula | Description |
| --- | --- |
| `daysUntilDue` | Days until due date (negative = overdue, positive = remaining, null if no due date) |
| `daysUntilScheduled` | Days until scheduled date |
| `daysSinceCreated` | Days since task file creation |
| `daysSinceModified` | Days since last modification |

#### Boolean Formulas

| Formula | Description |
| --- | --- |
| `isOverdue` | True if past due date and not completed |
| `isDueToday` | True if due today |
| `isDueThisWeek` | True if due within 7 days |
| `isScheduledToday` | True if scheduled for today |
| `isRecurring` | True if task has a recurrence rule |
| `hasTimeEstimate` | True if time estimate > 0 |

#### Time Tracking Formulas

| Formula | Description |
| --- | --- |
| `timeRemaining` | Time estimate minus time tracked (minutes) |
| `efficiencyRatio` | Percentage of estimated time used |
| `timeTrackedThisWeek` | Total minutes tracked in last 7 days |
| `timeTrackedToday` | Total minutes tracked today |

#### Grouping Formulas

| Formula | Description | Example Values |
| --- | --- | --- |
| `dueMonth` | Due date as year-month | "2025-01", "No due date" |
| `dueWeek` | Due date as year-week | "2025-W01", "No due date" |
| `dueDateCategory` | Human-readable due date bucket | "Overdue", "Today", "Tomorrow", "This week", "Later", "No due date" |
| `timeEstimateCategory` | Task size by time estimate | "No estimate", "Quick (<30m)", "Medium (30m-2h)", "Long (>2h)" |
| `ageCategory` | Task age bucket | "Today", "This week", "This month", "Older" |
| `priorityCategory` | Priority as readable label | "High", "Normal", "Low", "No priority" |

#### Sorting Formulas

| Formula | Description |
| --- | --- |
| `priorityWeight` | Numeric weight for priority sorting |
| `urgencyScore` | Combines priority and next date proximity |

#### Display Formulas

| Formula | Description |
| --- | --- |
| `timeTrackedFormatted` | Total time tracked as readable text (e.g., "2h 30m") |
| `dueDateDisplay` | Due date as relative text (e.g., "Today", "Tomorrow", "3d ago") |

### View Templates

The default templates include: **Mini Calendar** (4 date-property tabs: Due, Scheduled, Created, Modified), **Kanban Board** (grouped by status), **Tasks List** (multiple views: All Tasks, Not Blocked, Today, Overdue, This Week, Unscheduled), **Calendar** (full calendar with time slots), **Agenda** (list-based agenda), and **Relationships** (subtasks, projects, blocked by, blocking tabs).

### Customization

If you've customized your TaskNotes settings, generated templates will reflect those changes: custom visible properties in `order` arrays, property-based identification in filters, custom priorities in `priorityWeight` formula, custom statuses in incomplete task filters, and custom property names throughout.

---

# Settings

TaskNotes settings are organized into tabs. Each tab controls a different part of plugin behavior.

## Settings Overview

- **General:** Task identification, storage locations, and task-card click behavior
- **Task Properties:** Schema for frontmatter including status, priority, dates, reminders, projects, and user fields
- **Modal Fields:** Task create/edit experience — which fields are visible and in what order
- **Appearance & UI:** Task card density, calendar defaults, time formatting, and visual toggles
- **Features:** Behavior toggles for inline tasks, natural language input, Pomodoro, reminders, and performance
- **Integrations:** External connectivity — Bases views, OAuth calendar sync, ICS subscriptions, HTTP API, webhooks

---

## General Settings

These settings control the foundational aspects of the plugin, such as task identification, file storage, and click behavior.

### Task Storage

Task storage settings define where new and converted task files are created and how archived tasks are relocated. Default tasks folder sets the base location. Folder for converted tasks appears when instant conversion is enabled and supports `{{currentNotePath}}` and `{{currentNoteTitle}}` placeholders for contextual routing. If archive moves are enabled, completed archived tasks are moved automatically to your configured archive folder.

### Task Identification

TaskNotes can identify task notes using either a tag or a frontmatter property. Use "Identify tasks by" to select a strategy.

- **Tag mode** uses a configured task tag (for example `task`) and can optionally hide that identifying tag in card displays.
- **Property mode** matches a property/value pair (for example `isTask: true` or `category: task`) and is useful when you avoid tag-based identification.

#### Hide Identification Tags

When using tag-based identification, the "Hide identification tags in task cards" setting hides matching tags from visual display while keeping them in frontmatter. Tags that exactly match your task identification tag (e.g., `#task`) and hierarchical child tags (e.g., `#task/project`) will be hidden. Other tags remain displayed.

### Folder Management

Use "Excluded folders" to omit paths from Notes tab indexing and keep large archive areas out of regular task browsing.

### Frontmatter

This section only appears when you have markdown links enabled globally in Obsidian settings. "Use markdown links in frontmatter" switches project/dependency serialization from wikilinks to markdown links. This requires the `obsidian-frontmatter-markdown-links` plugin.

### Task Interaction

Task interaction settings define default click behavior on task cards. You can independently choose single-click and double-click actions (edit task, open note, or no action for double click).

### Release Notes

View release notes opens the release notes view for the current version. Notes also open automatically after updates.

---

## Task Properties Settings

This tab configures all task properties. Each property is displayed as a card containing its configuration options.

### Property Card Structure

Each property card contains: property key (the frontmatter field name), default value (where applicable), NLP trigger toggle and character configuration (where applicable), and property-specific settings.

### Core Properties

#### Title

Filename format options when "Store title in filename" is disabled: Title-based, Zettelkasten-style, Timestamp-based, or Custom template.

#### Status

Task completion state. Configuration options include property key (default: `status`), default status, NLP trigger (default: `*`), and Status Values section with individual status cards. Each status value has: Value, Label, Color, Icon, Completed flag, and Auto-archive (with 1-1440 minute delay). Status cards support drag-and-drop reordering.

**Boolean Status Values:** TaskNotes supports using boolean values (`true` and `false`) as status values, integrating with Obsidian's native checkbox property format.

#### Priority

Task priority level. Configuration includes property key (default: `priority`), default, NLP trigger (default: `!`, disabled by default), and Priority Values section. Priority cards support drag-and-drop reordering.

**Note for Bases users:** Obsidian's Bases plugin sorts priorities alphabetically by Value. To control sort order, name values to sort alphabetically (e.g., `1-urgent`, `2-high`, `3-medium`, `4-normal`, `5-low`).

### Date Properties

- **Due Date:** When the task must be completed. Property key default: `due`. Default options: None, Today, Tomorrow, Next Week.
- **Scheduled Date:** When to work on the task. Property key default: `scheduled`. `due` tracks commitment deadlines, while `scheduled` tracks intended execution time.

### Organization Properties

- **Contexts:** Where or how the task can be done. Property key default: `contexts`. NLP trigger default: `@`.
- **Projects:** Projects the task belongs to. Property key default: `projects`. NLP trigger default: `+`. Includes Autosuggest Filters and Customize Display sections.
- **Tags:** Uses native Obsidian tags. NLP trigger default: `#`.

### Task Details

- **Time Estimate:** Property key default: `timeEstimate`. Default in minutes (0 = no default).
- **Recurrence:** Property key default: `recurrence`. Default options: None, Daily, Weekly, Monthly, Yearly.
- **Reminders:** Property key default: `reminders`. Supports relative reminders (anchor date, offset, direction, description) and absolute reminders (date, time, description).

### Metadata Properties

System-managed properties: Date Created, Date Modified, Completed Date, Archive Tag, Time Entries, Complete Instances, Blocked By.

### Feature Properties

- **Pomodoros:** Written to daily notes when Pomodoro data storage is set to "Daily notes".
- **ICS Event ID:** Added to notes created from ICS calendar events.
- **ICS Event Tag:** Tag for calendar event identification.

### Custom User Fields

Define custom frontmatter properties with Display Name, Property Key, Type (text, number, boolean, date, or list), Default Value, NLP trigger, and Autosuggest Filters.

---

## Modal Fields Settings

The Modal Fields tab lets you decide exactly which fields appear in the task creation and edit modals.

### Field Groups

Fields are organized into draggable groups: Custom Fields, Dependencies, Organization, Metadata, and Basic Information. Each group can be collapsed, and their order matches the order shown in the modal.

### Managing Fields

Every field entry includes a required toggle (where applicable), drag handle for ordering, enable/disable checkbox, and visibility toggles for creation and edit modals. Changes are saved automatically.

### Syncing User Fields

The "Sync User Fields" button pulls the latest user-defined fields from the Task Properties tab into the Custom Fields group. New fields are appended, renamed fields update in place, removed fields drop out.

### Resetting to Defaults

"Reset to Defaults" restores the stock configuration. The reset keeps your existing user field definitions; it only reverts modal layout and visibility.

---

## Appearance & UI Settings

These settings control the visual appearance of the plugin.

### Task Cards

Use "Default visible properties" to decide what metadata appears on task cards. Checklist progress is available as a visible property (source property: `file.tasks`).

### Display Formatting

Use "Time format" to switch between 12-hour and 24-hour display across all TaskNotes surfaces.

### Calendar View

Settings include default view, custom day span, first day of week, weekend visibility, week numbers, today/current-time markers, selection mirror, and calendar locale for region-specific formatting.

### Default Event Visibility

Controls which event layers are enabled when a calendar view opens: scheduled tasks, due dates, due dates for already-scheduled tasks, time entries, recurring tasks, and ICS events.

### Time Settings

Slot duration, earliest visible time, latest visible time, and initial scroll position.

### UI Elements

Toggles for tracked-task status bar entry, project subtasks widget and placement, expandable subtasks in cards, chevron position, and views/filters button alignment.

---

## Features Settings

These settings allow you to enable, disable, and configure the various features of the plugin.

### Inline Tasks

Task link overlay, Instant task convert, Inline task convert folder (supports `{{currentNotePath}}`), and Use task defaults on instant convert.

### Body Template

When enabled, TaskNotes reads the configured template file and expands variables like `{{title}}`, `{{date}}`, `{{time}}`, `{{priority}}`, `{{status}}`, `{{contexts}}`, `{{tags}}`, and `{{projects}}`.

### Natural Language Processing

Enable natural language task input, Default to scheduled, NLP language, and Status suggestion trigger.

### Pomodoro Timer

Interval lengths, long-break cadence, auto-start behavior, end-of-session notifications/sound, and data storage choice (plugin data or daily notes).

### Notifications

Enable reminders globally and choose in-app or system notifications.

### Performance & Behavior

Exclude completed tasks from overdue calculations, disable indexing for very large vaults, tune suggestion debounce timing.

### Time Tracking

Auto-stop running timers on task completion and optional confirmation notification.

### Recurring Tasks

Maintain due date offset in recurring tasks to keep due/scheduled spacing consistent.

### Timeblocking

Enable daily-note scheduling blocks and control calendar visibility.

---

## Integrations Settings

These settings control the integration with other plugins and services.

### Bases Integration

TaskNotes v4 uses Obsidian's Bases core plugin for its main views.

#### View Commands Configuration

Default mappings: Open Mini Calendar View → `mini-calendar-default.base`, Open Kanban View → `kanban-default.base`, Open Tasks View → `tasks-default.base`, Open Calendar View → `calendar-default.base`, Open Agenda View → `agenda-default.base`, Relationships Widget → `relationships.base`. Each command allows a custom `.base` file path with a reset button.

"Create Default Files" button generates all default `.base` files in `TaskNotes/Views/`. Existing files are not overwritten.

### OAuth Calendar Integration

Connect Google Calendar or Microsoft Outlook to sync events bidirectionally. Events refresh every 15 minutes and sync when local changes are made.

#### Google Calendar

Provide Client ID and Client Secret from Google Cloud Console, then use "Connect Google Calendar" to complete OAuth loopback authentication.

#### Microsoft Outlook Calendar

Provide Client ID and Client Secret from Azure App Registration, then use "Connect Microsoft Calendar" to authenticate.

#### Security

OAuth credentials are stored locally. Access tokens refresh automatically. Calendar data syncs directly between Obsidian and the calendar provider (no intermediary servers). Disconnect at any time.

### Calendar Subscriptions (ICS)

Set default template, destination folder, filename strategy, and custom filename template for generated notes. Use "Add Calendar Subscription" to register URLs or local files.

### Automatic ICS Export

Keeps an ICS feed of your tasks updated on a schedule. Configure enable/disable, file path, refresh interval, and manual "Export now" button.

### HTTP API

Controls the local server lifecycle, listening port, and request authentication token. Changes require an Obsidian restart.

> **Warning:** If the authentication token is empty, API requests are unauthenticated.

### Webhooks

Register webhook endpoints for automation.

---

## Defaults & Templates Settings

> **Note:** Default value settings have been moved to the Task Properties tab. Each property card now contains its own default value configuration.

### Where to Find Default Settings

| Setting | Location |
| --- | --- |
| Default status | Task Properties → Status card |
| Default priority | Task Properties → Priority card |
| Default due date | Task Properties → Due Date card |
| Default scheduled date | Task Properties → Scheduled Date card |
| Default contexts | Task Properties → Contexts card |
| Default tags | Task Properties → Tags card |
| Default projects | Task Properties → Projects card |
| Default time estimate | Task Properties → Time Estimate card |
| Default recurrence | Task Properties → Recurrence card |
| Default reminders | Task Properties → Reminders card |

### Body Template

Body template settings are in the Features tab: Body template file (supports template variables), and Use body template toggle.

### Instant Task Conversion

"Use task defaults on instant convert" is in the Features tab.

---

## Advanced Settings

This page documents advanced configuration patterns spread across multiple settings tabs.

### Where Advanced Configuration Lives

TaskNotes v4 uses a 6-tab settings layout: General, Task Properties, Modal Fields, Appearance, Features, Integrations. There is no separate Advanced tab.

### Field Mapping

Controls which frontmatter keys TaskNotes reads and writes for core properties. Location: `Settings -> TaskNotes -> Task Properties`. Use field mapping when you already use different frontmatter key names or are integrating with other plugins.

### User Fields

Custom properties for filters, grouping, sorting, and modal forms. Location: `Settings -> TaskNotes -> Task Properties`. Typical fields: Text (`client`, `assignee`), Number (`effort`, `score`), Date (`reviewDate`), Boolean (`urgent`), List (`labels`, `stakeholders`).

### Status and Priority Workflows

Custom statuses and priorities. Location: `Settings -> TaskNotes -> Task Properties`. Statuses define workflow progression and completion semantics. Priority names sort lexicographically unless your view uses explicit formulas.

### Modal Field Layout

Reconfigure the create/edit modal. Location: `Settings -> TaskNotes -> Modal Fields`.

### Time Tracking and Pomodoro Controls

Location: `Settings -> TaskNotes -> Features`.

### ICS-Specific Field Mapping

`icsEventId` and ICS tag field. Location: `Settings -> TaskNotes -> Task Properties`.

---

## Property Types Reference

This reference documents the expected data types for each frontmatter property.

### Quick Reference

| Property | Type | Example |
| --- | --- | --- |
| title | text | `"My Task"` |
| status | text | `"open"`, `"in-progress"`, `"done"` |
| priority | text | `"low"`, `"normal"`, `"high"` |
| due | text (date) | `"2025-01-15"` |
| scheduled | text (date) | `"2025-01-10"` |
| completedDate | text (date) | `"2025-01-20"` |
| dateCreated | text (datetime) | `"2025-01-01T08:00:00Z"` |
| dateModified | text (datetime) | `"2025-01-15T10:30:00Z"` |
| tags | list | `["work", "urgent"]` |
| contexts | list | `["@office", "@home"]` |
| projects | list | `["[[Project A]]"]` |
| timeEstimate | number | `120` (minutes) |
| recurrence | text | `"FREQ=WEEKLY;BYDAY=MO"` |
| recurrence_anchor | text | `"scheduled"` or `"completion"` |
| timeEntries | list (objects) | See Time Entries |
| blockedBy | list (objects) | See Dependencies |
| reminders | list (objects) | See Reminders |
| complete_instances | list | `["2025-01-08", "2025-01-15"]` |
| skipped_instances | list | `["2025-01-22"]` |
| icsEventId | list | `["event-abc123"]` |

### Property Details

#### Text Properties

**title** — Type: text (string). Example: `title: "Complete project documentation"`

**status** — Type: text (string). Must match one of the configured status values. Default values: `"open"`, `"in-progress"`, `"done"`. Also supports boolean values (`true`/`false`) for Obsidian checkbox compatibility.

**priority** — Type: text (string). Must match one of the configured priority values. Default values: `"low"`, `"normal"`, `"high"`.

#### Date Properties

All date properties are stored as text strings. TaskNotes expects specific formats. Prefer ISO-style values—they sort correctly, travel well through APIs, and parse consistently.

**due** — Format: `YYYY-MM-DD` or ISO 8601 timestamp. Examples: `due: "2025-01-15"` or `due: "2025-01-15T17:00:00"`

**scheduled** — Format: `YYYY-MM-DD` or ISO 8601 timestamp.

**completedDate** — Format: `YYYY-MM-DD`.

**dateCreated** / **dateModified** — Format: ISO 8601 timestamp.

#### List Properties

List properties must be arrays, even when containing a single value.

**tags** — Array of strings. Example: `tags: ["work", "documentation"]`

**contexts** — Array of strings. Example: `contexts: ["office", "computer"]`

**projects** — Array of strings (typically wikilinks). Example: `projects: ["[[Website Redesign]]", "[[Q1 Planning]]"]`

#### Numeric Properties

**timeEstimate** — Type: number, unit: minutes. Example: `timeEstimate: 120` (2 hours)

#### Recurrence Properties

**recurrence** — RFC 5545 RRULE format. Examples: `"FREQ=DAILY"`, `"FREQ=WEEKLY;BYDAY=MO,WE,FR"`, `"FREQ=MONTHLY;BYMONTHDAY=1"`

**recurrence_anchor** — `"scheduled"` or `"completion"`

**complete_instances** / **skipped_instances** — Arrays of date strings in `YYYY-MM-DD` format.

#### Complex Properties

**Time Entries:**

```yaml
timeEntries:
  - startTime: "2025-01-15T10:30:00Z"    # Required: ISO 8601 timestamp
    endTime: "2025-01-15T11:15:00Z"      # Optional: ISO 8601 timestamp
    description: "Initial work"          # Optional: text
```

**Dependencies (blockedBy):**

```yaml
blockedBy:
  - uid: "path/to/blocking-task.md"    # Required: path to blocking task
    reltype: "FINISHTOSTART"           # Required: relationship type
    gap: "P1D"                         # Optional: ISO 8601 duration offset
```

Relationship types: `FINISHTOSTART`, `STARTTOSTART`, `FINISHTOFINISH`, `STARTTOFINISH`

**Reminders (relative):**

```yaml
reminders:
  - id: "rem_1"
    type: "relative"
    relatedTo: "due"
    offset: "-PT1H"
    description: "1 hour before due"
```

**Reminders (absolute):**

```yaml
reminders:
  - id: "rem_2"
    type: "absolute"
    absoluteTime: "2025-01-15T09:00:00Z"
    description: "Morning reminder"
```

### Complete Example

```yaml
---
title: "Complete quarterly report"
status: "in-progress"
priority: "high"
due: "2025-01-31"
scheduled: "2025-01-25"
tags:
  - work
  - reports
contexts:
  - "@office"
projects:
  - "[[Q1 Planning]]"
timeEstimate: 240
dateCreated: "2025-01-01T08:00:00Z"
dateModified: "2025-01-20T14:30:00Z"
timeEntries:
  - startTime: "2025-01-20T10:00:00Z"
    endTime: "2025-01-20T11:30:00Z"
blockedBy:
  - uid: "tasks/gather-data.md"
    reltype: "FINISHTOSTART"
reminders:
  - id: "rem_1"
    type: "relative"
    relatedTo: "due"
    offset: "-P1D"
    description: "Due tomorrow"
---
```

### Field Mapping

All property names can be customized via Settings → Task Properties → Field Mapping. If you change a field mapping, TaskNotes reads and writes using your custom property name. For example, mapping `due` to `dueDate` means TaskNotes will expect `dueDate: "2025-01-15"`.

---

# Workflows

This page describes practical ways to combine TaskNotes features into repeatable workflows.

## Habit Tracking with Recurring Tasks

Habit tracking in TaskNotes is built on recurring task notes. You can create a recurring task from natural language (for example, "Exercise daily" or "Gym every Monday and Wednesday") or configure recurrence explicitly in the task modal. The modal recurrence controls support frequency, interval, weekday selection, and end conditions.

Once a task has a recurrence rule, its edit modal shows a recurrence calendar. That calendar is where you mark completion per occurrence. Completion history is stored in `complete_instances`, so a recurring task can remain open while still recording daily/weekly completion behavior.

```yaml
title: Morning Exercise
recurrence: "FREQ=DAILY"
scheduled: "07:00"
complete_instances:
  - "2025-01-01"
  - "2025-01-02"
  - "2025-01-04"
```

Use Calendar and Agenda views to review upcoming occurrences, and use recurring-task filters for a habit-only planning view.

## Project-Centered Planning

Projects in TaskNotes can be plain text values or wikilinks to project notes. Wikilinks are usually the better long-term option because they connect task execution to project context, backlinks, and graph navigation.

```yaml
title: "Research competitors"
projects: ["[[Market Research]]", "[[Q1 Strategy]]"]
```

During task creation, use the project picker to search and assign one or more projects. In day-to-day planning, open Task List or Kanban, then filter on `note.projects contains [[Project Name]]` to isolate one initiative. Save that filter as a Bases saved view if you revisit it regularly.

When work spans initiatives, assign multiple projects and combine with contexts or tags for secondary organization.

```yaml
title: "Prepare presentation slides"
projects: ["[[Q4 Planning]]"]
contexts: ["@computer", "@office"]
tags: ["#review"]
```

## Execution Workflow (Daily)

A typical daily flow is to start in Task List for prioritization, move to Calendar for schedule placement, and finish in Agenda for near-term sequencing. This keeps backlog management, time allocation, and short-horizon execution in one system.

If you use timeboxing, drag-select on calendar timeline views and create timeblocks directly from the context menu. If you use Pomodoro, run sessions against active tasks so completion and timing data stay attached to task notes.

## Maintenance Workflow (Weekly)

A weekly review usually includes three steps: clean up completed/archived tasks, verify recurring-task completion patterns, and rebalance project filters/views. If calendar integrations are enabled, this is also a good point to refresh subscriptions and confirm sync health.

For teams or complex personal systems, keep project notes as source-of-truth documents and use TaskNotes views as execution dashboards derived from those notes.

---

# TaskNotes HTTP API

The TaskNotes HTTP API provides local HTTP access to tasks, time tracking, pomodoro, calendars, webhooks, and NLP parsing.

## Availability

- Desktop only
- Disabled by default
- Started when Obsidian starts and TaskNotes API is enabled
- Not available on mobile

Enable it in `Settings -> TaskNotes -> Integrations -> HTTP API`.

## Base URL

`http://localhost:{PORT}` — Default port is `8080`.

## Authentication

Authentication is optional. If `apiAuthToken` is empty, all API requests are accepted. If `apiAuthToken` is set, send `Authorization: Bearer <token>`.

```bash
curl -H "Authorization: Bearer YOUR_TOKEN" http://localhost:8080/api/health
```

## Response Format

Success: `{ "success": true, "data": {} }`

Error: `{ "success": false, "error": "Error message" }`

## Endpoint Index

### System

- `GET /api/health` — Returns service state plus vault metadata
- `GET /api/docs` — Returns OpenAPI JSON
- `GET /api/docs/ui` — Returns Swagger UI
- `POST /api/nlp/parse` — Parse natural language input
- `POST /api/nlp/create` — Create task from natural language

### Tasks

- `GET /api/tasks` — List tasks with pagination (limit default 50, max 200; offset default 0). Filtering params are rejected with 400—use `POST /api/tasks/query` instead.
- `POST /api/tasks` — Create one task. Required: `title`. Optional: `details`, `status`, `priority`, `due`, `scheduled`, `tags`, `contexts`, `projects`, `recurrence`, `timeEstimate`.
- `GET /api/tasks/:id` — Get one task by URL-encoded path.
- `PUT /api/tasks/:id` — Update task with partial payload.
- `DELETE /api/tasks/:id` — Delete task file.
- `POST /api/tasks/:id/toggle-status` — Toggle task status via configured workflow.
- `POST /api/tasks/:id/archive` — Toggle archive state.
- `POST /api/tasks/:id/complete-instance` — Complete recurring instance. Optional `date` body param.
- `POST /api/tasks/query` — Advanced filtering with `FilterQuery` object (groups, conditions, conjunctions, sort, grouping).
- `GET /api/filter-options` — Returns filter options for UI builders.
- `GET /api/stats` — Returns summary counts: `total`, `completed`, `active`, `overdue`, `archived`, `withTimeTracking`.

### Time Tracking

- `POST /api/tasks/:id/time/start` — Start active time entry.
- `POST /api/tasks/:id/time/start-with-description` — Start with description.
- `POST /api/tasks/:id/time/stop` — Stop active time entry.
- `GET /api/tasks/:id/time` — Per-task time summary and entries.
- `GET /api/time/active` — Currently active sessions (multiple can exist).
- `GET /api/time/summary` — Aggregate time summary. Params: `period` (today/week/month/all), `from`, `to`.

### Pomodoro

- `POST /api/pomodoro/start` — Start session. Optional: `taskId`, `duration`.
- `POST /api/pomodoro/stop` — Stop and reset.
- `POST /api/pomodoro/pause` — Pause running session.
- `POST /api/pomodoro/resume` — Resume paused session.
- `GET /api/pomodoro/status` — Current state plus totals.
- `GET /api/pomodoro/sessions` — History. Params: `limit`, `date`.
- `GET /api/pomodoro/stats` — Stats for today or provided date.

### Calendars

- `GET /api/calendars` — Provider connectivity overview.
- `GET /api/calendars/google` — Google provider details.
- `GET /api/calendars/microsoft` — Microsoft provider details.
- `GET /api/calendars/subscriptions` — ICS subscriptions with runtime fields.
- `GET /api/calendars/events` — Merged event list. Params: `start`, `end`.

### Webhooks

- `POST /api/webhooks` — Register webhook. Required: `url`, `events`. Optional: `id`, `secret`, `active`, `transformFile`, `corsHeaders`.
- `GET /api/webhooks` — List registered webhooks.
- `DELETE /api/webhooks/:id` — Delete webhook.
- `GET /api/webhooks/deliveries` — Last 100 delivery records.

## Errors

Common status codes: `400` (invalid request), `401` (missing/invalid bearer token), `404` (missing resource), `500` (internal error).

## Security Notes

Current behavior: CORS allows all origins (`*`), transport is HTTP only (no TLS), server binds via `server.listen(port)`.

Practical guidance: Set an auth token, treat API port as sensitive and keep it firewalled, route through a trusted reverse proxy and TLS if exposing outside localhost.

## Troubleshooting

**API unavailable:** Confirm API is enabled, Obsidian is running, port is free. Reload plugin or restart Obsidian after changes.

**401 Authentication required:** Check token value, `Bearer ` prefix, and whitespace.

**Unexpected task list behavior:** If you pass filters to `GET /api/tasks`, the endpoint returns 400 by design. Use `POST /api/tasks/query`.

---

# Troubleshooting

Common issues and solutions for TaskNotes. When debugging, start with the smallest reproducible scenario: one affected task, one affected view, and current settings. Most issues fall into one of three categories: task identification mismatch, malformed frontmatter, or view/cache state.

## Bases and Views (v4)

### Views Not Loading

Symptoms: TaskNotes views show errors or don't display tasks.

First confirm Bases is enabled (`Settings -> Core Plugins -> Bases`), then restart Obsidian once. If views are still missing, verify `.base` files exist in `TaskNotes/Views/`. If needed, regenerate defaults from `Settings -> TaskNotes -> Integrations` (`Create default files`).

### Commands Open Wrong Files

Check command mappings in `Settings -> TaskNotes -> General` (`View Commands`). Reset mappings that were changed unintentionally, then verify each referenced `.base` file exists at the configured path.

## Common Issues

### Tasks Not Appearing in Views

Common causes are task-identification mismatch, excluded folders, invalid frontmatter, or stale view state. Verify the configured task identifier is present, ensure files are not excluded, and confirm YAML frontmatter is valid and wrapped with `---` delimiters. If all data looks correct, reopen the affected view and then restart Obsidian to refresh cache state.

### Task Link Widgets Not Working

Check that Task link overlay is enabled, then verify linked files are actually recognized as tasks (matching tag/property configuration). Links to normal notes will render as normal links by design.

### Instant Conversion Buttons Missing

Instant convert buttons only appear when the feature is enabled, in edit mode, and with cursor proximity to list items.

### Calendar View Performance Issues

Reduce visible event layers first (scheduled/due/recurring/time entries), then increase ICS refresh intervals and shorten displayed date ranges.

### Natural Language Parsing Not Working

Enable NLP in `Settings -> TaskNotes -> Features`, then verify trigger characters and custom mappings.

### Time Tracking Issues

Most tracking issues come from overlapping sessions, interrupted shutdowns, or save failures. Stop active sessions before starting new ones, confirm files are writable, and restart interrupted sessions.

## Data Issues

### Corrupted Task Files

Open the task file directly and validate frontmatter syntax. Quote values that include special characters, and restore from backup for severe corruption.

### Missing Task Properties

Check field mappings first, then confirm Task Defaults. If properties are absent on older notes, add them manually or re-save through TaskNotes.

### Date Format Issues

Use supported formats (`YYYY-MM-DD` or `YYYY-MM-DDTHH:MM:SS`), quote where needed, and re-enter problematic dates via TaskNotes date pickers.

## Performance Troubleshooting

### Slow View Loading

Reduce external calendar subscriptions, increase ICS refresh intervals, exclude large folders, and disable event types you do not use.

## External Calendar Issues

### OAuth Calendar Not Connecting

Verify credentials and loopback redirect configuration (`127.0.0.1` with dynamic local port), ensure app publication/test-user access is correct, and retry after disconnecting.

### OAuth Calendar Not Syncing

Run manual refresh, check last-sync timestamps, reconnect if needed.

### ICS Subscriptions Not Loading

Confirm the ICS URL/file is reachable, run manual refresh, validate the feed format.

### Calendar Sync Problems

Check refresh intervals and force a manual refresh. If source data is current but TaskNotes remains stale, remove and re-add the subscription.

## Getting Help

### Reporting Issues

Report bugs on [GitHub Issues](https://github.com/callumalpass/tasknotes/issues). Include screenshots, error messages (console: `Ctrl/Cmd + Shift + I`), steps to reproduce, OS, and TaskNotes/Obsidian versions.

### Configuration Reset

If all else fails:

1. Close Obsidian
2. Navigate to `.obsidian/plugins/tasknotes/`
3. Rename or delete `data.json`
4. Restart Obsidian

> **Warning:** This resets all settings, status configurations, and calendar subscriptions. Document your settings before resetting.

---

# Development

## Translation Workflow

TaskNotes ships with a lightweight i18n system that keeps interface copy separate from natural-language parsing patterns.

### Folder Structure

- `src/i18n/resources/en.ts` — English source strings (authoritative key set)
- `src/i18n/resources/<locale>.ts` — One file per locale exporting the same key tree
- `src/i18n/I18nService.ts` — Runtime that loads resources, handles fallbacks, and emits locale-change events

### Adding a New Language

1. Duplicate `src/i18n/resources/en.ts` to a new file with the ISO language code, e.g. `de.ts`.
2. Translate only the string values. Keep keys identical so TypeScript's type-checking continues to work.
3. Import the new resource in `src/i18n/index.ts` and add it to `translationResources`.
4. (Optional) Add a human-readable label under `common.languages.<code>` so the language shows up nicely in the UI picker.
5. Run `npm run test:unit -- --runTestsByPath tests/unit/services/i18nService.test.ts` to verify lookups and fallbacks.

### Using Translations in Code

```typescript
import type { TranslationKey } from 'src/i18n';

const t = (key: TranslationKey) => plugin.i18n.translate(key);
button.setText(t('settings.features.uiLanguage.dropdown.name'));
```

- Always prefer translation keys over inline strings for user-facing copy.
- When dynamic parts are needed, use placeholders (`{count}`) and supply them via `plugin.i18n.translate(key, { count })`.
- Use `plugin.i18n.resolveKey('common.languages.fr')` if you need the raw translated string without interpolation.

### UI Language Picker

Users can switch the interface language under Settings → Features → Interface Language. Choosing "System default" tracks the OS/browser locale and falls back to English if unsupported.

### Best Practices

Keep English strings concise; translators use them as context. Update both English and new locale files in the same pull request so CI stays green. If a string is reused in multiple places, create a single translation key instead of duplicating text in code. When adding new UI, wire translations before merging to avoid regressions for non-English users.

---

## i18n-state-manager

i18n-state-manager is a translation management tool developed for TaskNotes and published as an open-source npm package. It addresses a limitation common to most translation tools: the inability to detect when translations become outdated after source text changes.

### Purpose

Traditional translation tools can identify missing translations but cannot determine if existing translations correspond to the current source text. When English text changes from "Save task" to "Save task changes", other languages continue displaying translations of the original text. i18n-state-manager solves this by tracking the relationship between source text and translations using cryptographic hashes.

### How It Works

The tool maintains two files:

**Manifest (`i18n.manifest.json`)** — Contains SHA1 hashes of all source language strings. When source text changes, its hash changes.

**State (`i18n.state.json`)** — Records the source hash each translation was created against.

A translation is considered: **Current** (source hash matches state hash), **Missing** (no translation exists), or **Stale** (source hash has changed since translation was created).

### Integration with TaskNotes

TaskNotes uses i18n-state-manager to manage translations across seven languages. The tool runs in CI to prevent deployment of incomplete or outdated translations.

Available commands:

- `i18n-state generate-template` — Create translation file templates
- `i18n-state check-duplicates` — Detect duplicate translation keys
- `i18n-state find-unused` — Identify unused keys
- `i18n-state check-usage` — Verify all used keys exist
- `i18n-state status` — Display translation coverage statistics
- `i18n-state verify` — Check for missing or stale translations
- `i18n-state sync` — Update manifest and state files

### Requirements

Node.js 16 or later. Commands that scan code (`check-usage`, `find-unused`) require ripgrep.

### Installation

```bash
npm install -D i18n-state-manager
```
