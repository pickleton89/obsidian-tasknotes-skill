#!/usr/bin/env python3
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///
"""Obsidian TaskNotes Skill -- CLI Orchestrator

Routes commands to the best available tool: mtn (file mode), tn (API mode),
or direct HTTP API. All operations are deterministic -- the LLM calls this
script rather than manipulating task files directly.

Usage:
    uv run python scripts/tn_manager.py --vault <path> <command> [options]

Commands:
    status              Task overview and counts
    create              Create a new task
    nlp                 Create task from natural language
    update              Update an existing task
    complete            Mark a task as completed
    delete              Delete a task
    list                List and filter tasks
    search              Search tasks by content
    today               Tasks due or scheduled today
    overdue             Overdue incomplete tasks
    start-timer         Start time tracking
    stop-timer          Stop time tracking
    timer-log           Show time tracking log
    projects            List projects
    pomodoro            Pomodoro timer (API-only)
    setup               Install/configure CLI tools
    help                Show available commands
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# Ensure the scripts directory is on the path for sibling imports
sys.path.insert(0, str(Path(__file__).parent))

from common import (
    api_request,
    check_api_available,
    detect_tools,
    discover_vault,
    load_plugin_settings,
    now_iso,
    output,
    require_any_tool,
    resolve_api_config,
    resolve_statuses,
    run_cli,
    today_str,
)


# ---------------------------------------------------------------------------
# Tool Selection
# ---------------------------------------------------------------------------


def select_tool(tools: dict, prefer_api: bool = False) -> str | None:
    """Select the best available tool.

    Default preference: mtn (file) > tn (API).
    If prefer_api is True: tn > mtn.
    """
    if prefer_api:
        return "tn" if tools.get("tn") else ("mtn" if tools.get("mtn") else None)
    return "mtn" if tools.get("mtn") else ("tn" if tools.get("tn") else None)


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------


def cmd_status(args):
    """Show task overview: counts by status, overdue, today's tasks."""
    tools = detect_tools()
    api_config = resolve_api_config(args.vault)
    api_ok = not args.file_only and check_api_available(api_config)

    # tn stats supports --json; mtn stats does not
    if api_ok and tools["tn"]:
        if args.json:
            result = run_cli("tn", ["stats", "--json"], json_out=True)
        else:
            result = run_cli("tn", ["stats"], json_out=False)
        if result is not None:
            if args.json and isinstance(result, dict):
                print(json.dumps(result, indent=2, ensure_ascii=False))
            elif isinstance(result, str):
                print(result)
            else:
                print("--=={ TaskNotes Status }==--\n")
                for k, v in (result if isinstance(result, dict) else {}).items():
                    if not k.startswith("_"):
                        print(f"  {k.replace('_', ' ').title()}: {v}")
            return

    if tools["mtn"]:
        # mtn stats has no --json flag; capture text output
        result = run_cli("mtn", ["stats"], json_out=False)
        if result is not None:
            if args.json:
                print(json.dumps({"_raw": result}, indent=2))
            else:
                print(result)
            return

    # Direct API fallback
    if api_ok:
        result = api_request("GET", "/api/stats", api_config)
        data = result.get("data", result)
        def _print():
            print("--=={ TaskNotes Status }==--\n")
            for k, v in data.items():
                label = k.replace("_", " ").replace("-", " ").title()
                print(f"  {label}: {v}")
        output(data, _print, json_mode=args.json)
        return

    # Provide specific guidance based on what's available
    print("Error: Could not retrieve task status.", file=sys.stderr)
    if tools["mtn"]:
        print("  mtn is installed but failed. Enable 'mdbase spec' in:", file=sys.stderr)
        print("  TaskNotes Settings -> Integrations -> Enable mdbase spec", file=sys.stderr)
    if tools["tn"]:
        print("  tn is installed but API is unreachable. Ensure:", file=sys.stderr)
        print("  1. Obsidian is running", file=sys.stderr)
        print("  2. HTTP API is enabled in TaskNotes Settings -> Integrations", file=sys.stderr)
    if not tools["mtn"] and not tools["tn"]:
        print("  No CLI tools installed. Run: /tn setup", file=sys.stderr)
    sys.exit(1)


def cmd_create(args):
    """Create a new task."""
    tools = detect_tools()
    require_any_tool(tools)

    # Build NLP-style text from title + explicit options
    text = args.title
    if args.due:
        text += f" due {args.due}"
    if args.scheduled:
        text += f" scheduled {args.scheduled}"
    if args.priority and args.priority != "normal":
        text += f" {args.priority} priority"
    if args.tags:
        for t in args.tags.split(","):
            t = t.strip()
            if t:
                text += f" #{t}"
    if args.contexts:
        for c in args.contexts.split(","):
            c = c.strip()
            if c:
                text += f" @{c}"
    if args.projects:
        for p in args.projects.split(","):
            p = p.strip()
            if p:
                text += f" +{p}"
    if args.time_estimate:
        text += f" ~{args.time_estimate}m"

    tool = select_tool(tools)
    if tool == "mtn":
        cli_args = ["create", text]
        if args.json:
            cli_args.append("--json")
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        cli_args = [text]
        if args.json:
            cli_args.append("--json")
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        # Direct API
        api_config = resolve_api_config(args.vault)
        body = {"title": args.title}
        if args.status:
            body["status"] = args.status
        if args.priority:
            body["priority"] = args.priority
        if args.due:
            body["due"] = args.due
        if args.scheduled:
            body["scheduled"] = args.scheduled
        if args.tags:
            body["tags"] = [t.strip() for t in args.tags.split(",") if t.strip()]
        if args.contexts:
            body["contexts"] = [c.strip() for c in args.contexts.split(",") if c.strip()]
        if args.projects:
            body["projects"] = [p.strip() for p in args.projects.split(",") if p.strip()]
        if args.time_estimate:
            body["timeEstimate"] = int(args.time_estimate)
        result = api_request("POST", "/api/tasks", api_config, body=body)
        result = result.get("data", result)

    if result is None:
        sys.exit(1)

    if args.json:
        if isinstance(result, dict):
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result)
    elif isinstance(result, str):
        print(result)
    else:
        print(f"Created task: {args.title}")


def cmd_nlp(args):
    """Create a task from natural language text."""
    tools = detect_tools()
    require_any_tool(tools)

    text = args.text
    tool = select_tool(tools)

    if tool == "mtn":
        cli_args = ["create", text]
        if args.json:
            cli_args.append("--json")
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        cli_args = [text]
        if args.json:
            cli_args.append("--json")
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        api_config = resolve_api_config(args.vault)
        if check_api_available(api_config):
            result = api_request("POST", "/api/nlp/create", api_config, body={"text": text})
            result = result.get("data", result)
        else:
            print("Error: NLP creation requires a running TaskNotes API or CLI tools.", file=sys.stderr)
            sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json:
        if isinstance(result, dict):
            print(json.dumps(result, indent=2, ensure_ascii=False))
        else:
            print(result)
    elif isinstance(result, str):
        print(result)
    else:
        print(f"Created task from: {text}")


def cmd_update(args):
    """Update an existing task."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)

    if tool == "mtn":
        # mtn update: --status, --priority, --due, --scheduled, --title,
        #             --add-tag, --remove-tag, --add-context, --remove-context
        cli_args = ["update", args.title]
        if args.status:
            cli_args += ["--status", args.status]
        if args.priority:
            cli_args += ["--priority", args.priority]
        if args.due:
            cli_args += ["--due", args.due]
        if args.scheduled:
            cli_args += ["--scheduled", args.scheduled]
        if args.add_tag:
            cli_args += ["--add-tag", args.add_tag]
        if args.remove_tag:
            cli_args += ["--remove-tag", args.remove_tag]
        if args.add_context:
            cli_args += ["--add-context", args.add_context]
        if args.remove_context:
            cli_args += ["--remove-context", args.remove_context]
        result = run_cli("mtn", cli_args, json_out=False)

    elif tool == "tn":
        # tn update: --status, --priority, --due, --scheduled, --title,
        #            --add-tags, --remove-tags, --add-contexts, --remove-contexts (plural!)
        cli_args = ["update", args.title]
        if args.status:
            cli_args += ["--status", args.status]
        if args.priority:
            cli_args += ["--priority", args.priority]
        if args.due:
            cli_args += ["--due", args.due]
        if args.scheduled:
            cli_args += ["--scheduled", args.scheduled]
        if args.add_tag:
            cli_args += ["--add-tags", args.add_tag]
        if args.remove_tag:
            cli_args += ["--remove-tags", args.remove_tag]
        if args.add_context:
            cli_args += ["--add-contexts", args.add_context]
        if args.remove_context:
            cli_args += ["--remove-contexts", args.remove_context]
        result = run_cli("tn", cli_args, json_out=False)
    else:
        print("Error: No CLI tools available for update.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)
    else:
        print(f"Updated task: {args.title}")


def cmd_complete(args):
    """Mark a task as completed."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["complete", args.title]
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)
    else:
        print(f"Completed task: {args.title}")


def cmd_delete(args):
    """Delete a task."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["delete", args.title]
    if args.force:
        cli_args.append("--force")
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)
    else:
        print(f"Deleted task: {args.title}")


def cmd_list(args):
    """List and filter tasks."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)

    if tool == "mtn":
        # mtn list flags: --status, --priority, --tag, --due, --overdue, --where, --json
        cli_args = ["list"]
        if args.status:
            cli_args += ["--status", args.status]
        if args.priority:
            cli_args += ["--priority", args.priority]
        if args.tag:
            cli_args += ["--tag", args.tag]
        if args.overdue:
            cli_args.append("--overdue")
        if args.today:
            # mtn doesn't have --today; use --where with today's date
            today = today_str()
            cli_args += ["--where", f'due == "{today}" || scheduled == "{today}"']
        if args.where:
            cli_args += ["--where", args.where]
        # mtn doesn't support --context, --project, --completed directly
        # Build a where clause for unsupported filters
        extra_where = []
        if args.context:
            extra_where.append(f'contexts contains "{args.context}"')
        if args.project:
            extra_where.append(f'projects contains "{args.project}"')
        if extra_where:
            if args.where:
                cli_args[-1] = f'({cli_args[-1]}) && {" && ".join(extra_where)}'
            else:
                cli_args += ["--where", " && ".join(extra_where)]
        if args.json:
            cli_args.append("--json")
        result = run_cli("mtn", cli_args, json_out=args.json)

    elif tool == "tn":
        # tn list flags: --today, --overdue, --completed, --filter, --json
        cli_args = ["list"]
        if args.today:
            cli_args.append("--today")
        if args.overdue:
            cli_args.append("--overdue")
        if args.completed:
            cli_args.append("--completed")
        # Build filter expression for tn
        filters = []
        if args.status:
            filters.append(f"status:{args.status}")
        if args.priority:
            filters.append(f"priority:{args.priority}")
        if args.tag:
            filters.append(f"tags:{args.tag}")
        if args.context:
            filters.append(f"contexts:{args.context}")
        if args.project:
            filters.append(f"projects:{args.project}")
        if args.where:
            filters.append(args.where)
        if filters:
            cli_args += ["--filter", " AND ".join(filters)]
        if args.json:
            cli_args.append("--json")
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)


def cmd_search(args):
    """Search tasks by content."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    # Neither mtn search nor tn search supports --json
    cli_args = ["search", args.query]

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=False)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=False)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if isinstance(result, str):
        print(result)


def cmd_today(args):
    """Show tasks due or scheduled today."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["list", "--today"]
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)


def cmd_overdue(args):
    """Show overdue incomplete tasks."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["list", "--overdue"]
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)


def cmd_start_timer(args):
    """Start time tracking for a task."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["timer", "start", args.title]
    if args.description:
        cli_args += ["-d", args.description]
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)
    else:
        print(f"Timer started for: {args.title}")


def cmd_stop_timer(args):
    """Stop time tracking."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["timer", "stop"]
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, dict):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)
    else:
        print("Timer stopped.")


def cmd_timer_log(args):
    """Show time tracking log."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["timer", "log"]
    if args.period:
        cli_args += ["--period", args.period]
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)


def cmd_projects(args):
    """List projects or show project details."""
    tools = detect_tools()
    require_any_tool(tools)

    tool = select_tool(tools)
    cli_args = ["projects"]
    if args.show:
        cli_args += ["show", args.show]
    else:
        cli_args.append("list")
        if args.stats:
            cli_args.append("--stats")
    if args.json:
        cli_args.append("--json")

    if tool == "mtn":
        result = run_cli("mtn", cli_args, json_out=args.json)
    elif tool == "tn":
        result = run_cli("tn", cli_args, json_out=args.json)
    else:
        print("Error: No CLI tools available.", file=sys.stderr)
        sys.exit(1)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)


def cmd_pomodoro(args):
    """Pomodoro timer (API-only via tn)."""
    tools = detect_tools()

    if not tools["tn"]:
        print("Error: Pomodoro requires the tn CLI (API mode).", file=sys.stderr)
        print("Install with: /tn setup", file=sys.stderr)
        sys.exit(1)

    action = args.action or "status"
    cli_args = ["pomodoro", action]
    if args.json:
        cli_args.append("--json")

    result = run_cli("tn", cli_args, json_out=args.json)

    if result is None:
        sys.exit(1)

    if args.json and isinstance(result, (dict, list)):
        print(json.dumps(result, indent=2, ensure_ascii=False))
    elif isinstance(result, str):
        print(result)


def cmd_setup(args):
    """Install and configure CLI tools."""
    vault_path = args.vault
    if not vault_path:
        v = discover_vault()
        if v:
            vault_path = str(v)

    tools = detect_tools()
    installed = []

    # Check/install mtn
    if tools["mtn"]:
        print(f"  mtn: already installed ({tools['mtn']})")
    else:
        print("  Installing mdbase-tasknotes (mtn)...")
        r = subprocess.run(
            ["npm", "install", "-g", "mdbase-tasknotes"],
            capture_output=True, text=True,
        )
        if r.returncode == 0:
            print("  mtn: installed successfully")
            installed.append("mtn")
        else:
            print(f"  mtn: install failed -- {r.stderr.strip()}", file=sys.stderr)

    # Check/install tn
    if tools["tn"]:
        print(f"  tn: already installed ({tools['tn']})")
    else:
        tn_dir = Path.home() / ".tasknotes-cli-tool"
        if not tn_dir.exists():
            print("  Cloning tasknotes-cli...")
            r = subprocess.run(
                ["git", "clone", "https://github.com/callumalpass/tasknotes-cli.git", str(tn_dir)],
                capture_output=True, text=True,
            )
            if r.returncode != 0:
                print(f"  tn: clone failed -- {r.stderr.strip()}", file=sys.stderr)
        if tn_dir.exists():
            print("  Installing tasknotes-cli dependencies...")
            subprocess.run(["npm", "install"], cwd=str(tn_dir), capture_output=True, text=True)
            r = subprocess.run(["npm", "link"], cwd=str(tn_dir), capture_output=True, text=True)
            if r.returncode == 0:
                print("  tn: installed successfully")
                installed.append("tn")
            else:
                print(f"  tn: npm link failed -- {r.stderr.strip()}", file=sys.stderr)

    # Configure
    if vault_path:
        # Configure mtn
        if shutil.which("mtn"):
            subprocess.run(
                ["mtn", "config", "--set", f"collectionPath={vault_path}"],
                capture_output=True, text=True,
            )
            print(f"  mtn: configured for vault at {vault_path}")

        # Configure tn
        tn_config_dir = Path.home() / ".tasknotes-cli"
        tn_config_dir.mkdir(exist_ok=True)
        tn_config = tn_config_dir / "config.json"

        # Read API config from plugin settings
        settings = load_plugin_settings(vault_path)
        port = settings.get("apiPort", 8080)
        token = settings.get("apiAuthToken", "")

        config = {
            "host": "localhost",
            "port": port,
            "authToken": token if token else None,
            "maxResults": 50,
        }
        tn_config.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        print(f"  tn: configured for API at localhost:{port}")

        # Check mdbase spec
        if not settings.get("enableMdbaseSpec", False):
            print()
            print("  Note: 'Enable mdbase spec' is OFF in TaskNotes settings.")
            print("  The mtn tool requires this. Enable it in:")
            print("  Settings -> TaskNotes -> Integrations -> Enable mdbase spec")
    else:
        print()
        print("  Warning: No vault found. Configure manually:")
        print("    mtn config --set collectionPath=/path/to/vault")
        print("    tn config")

    # Check Obsidian CLI
    obs = shutil.which("obsidian")
    if obs:
        print(f"  obsidian CLI: available ({obs})")
    else:
        print("  obsidian CLI: not found (optional)")

    print()
    print("Setup complete.")


def cmd_install(args):
    """Install or update the skill into a vault by copying files."""
    source = Path(args.source) if args.source else Path(__file__).parent.parent
    vault_path = args.vault

    if not vault_path:
        vault = discover_vault()
        if vault:
            vault_path = str(vault)
        else:
            print("Error: No vault found. Specify --vault PATH.", file=sys.stderr)
            sys.exit(1)

    if not Path(vault_path).exists():
        print(f"Error: Vault path not found: {vault_path}", file=sys.stderr)
        sys.exit(1)

    if not source.exists():
        print(f"Error: Source directory not found: {source}", file=sys.stderr)
        sys.exit(1)

    target = Path(vault_path) / ".claude" / "skills" / "obsidian-tasknotes"
    updating = target.exists()

    # Files/dirs to copy (runtime-essential only)
    include = ["SKILL.md", "scripts", "references"]

    target.mkdir(parents=True, exist_ok=True)
    copied = []

    for item_name in include:
        src = source / item_name
        dst = target / item_name
        if not src.exists():
            continue
        if src.is_file():
            shutil.copy2(src, dst)
        elif src.is_dir():
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
                "__pycache__", "*.pyc", ".DS_Store",
            ))
        copied.append(item_name)

    # Write a version marker for update checks
    version_file = target / ".installed-version"
    skill_md = source / "SKILL.md"
    version = "1.0.0"
    if skill_md.exists():
        for line in skill_md.read_text(encoding="utf-8").split("\n"):
            if line.strip().startswith("version:"):
                version = line.split(":", 1)[1].strip().strip('"').strip("'")
                break
    version_file.write_text(f"{version}\n", encoding="utf-8")
    copied.append(".installed-version")

    action = "Updated" if updating else "Installed"
    result = {
        "action": action.lower(),
        "source": str(source),
        "target": str(target),
        "version": version,
        "files": copied,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"{action} obsidian-tasknotes skill (v{version})")
        print(f"  Source: {source}")
        print(f"  Target: {target}")
        for name in copied:
            print(f"    + {name}")
        if not updating:
            print()
            print("  Next steps:")
            print("  1. Run: /tn setup   (to install/configure CLI tools)")
            print("  2. Enable 'mdbase spec' in TaskNotes Settings -> Integrations")


def cmd_check_update(args):
    """Check if the installed skill is outdated compared to the source repo."""
    source = Path(args.source) if args.source else Path(__file__).parent.parent
    vault_path = args.vault

    if not vault_path:
        vault = discover_vault()
        if vault:
            vault_path = str(vault)
        else:
            print("Error: No vault found. Specify --vault PATH.", file=sys.stderr)
            sys.exit(1)

    target = Path(vault_path) / ".claude" / "skills" / "obsidian-tasknotes"
    version_file = target / ".installed-version"

    if not target.exists():
        print("Skill is not installed in this vault.")
        print(f"Run: uv run python scripts/tn_manager.py --vault {vault_path} install")
        return

    installed_version = "unknown"
    if version_file.exists():
        installed_version = version_file.read_text(encoding="utf-8").strip()

    source_version = "unknown"
    skill_md = source / "SKILL.md"
    if skill_md.exists():
        for line in skill_md.read_text(encoding="utf-8").split("\n"):
            if line.strip().startswith("version:"):
                source_version = line.split(":", 1)[1].strip().strip('"').strip("'")
                break

    result = {
        "installed": installed_version,
        "available": source_version,
        "up_to_date": installed_version == source_version,
        "target": str(target),
        "source": str(source),
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        if installed_version == source_version:
            print(f"Skill is up to date (v{installed_version})")
        else:
            print(f"Update available: v{installed_version} -> v{source_version}")
            print(f"Run: uv run python scripts/tn_manager.py --vault {vault_path} install")


def cmd_help(args):
    """Show available commands."""
    print("""Obsidian TaskNotes Skill -- Commands
=====================================
  /tn                              Task overview and status
  /tn create "Title" [opts]        Create a new task
  /tn nlp "natural language"       Create task from natural language
  /tn update "Title" [opts]        Update a task's fields
  /tn complete "Title"             Mark a task as completed
  /tn delete "Title" [--force]     Delete a task
  /tn list [filters]               List and filter tasks
  /tn search "query"               Search tasks by content
  /tn today                        Tasks due or scheduled today
  /tn overdue                      Overdue incomplete tasks
  /tn start-timer "Title"          Start time tracking
  /tn stop-timer                   Stop time tracking
  /tn timer-log [--period P]       Show time tracking log
  /tn projects [list|show NAME]    Project overview
  /tn pomodoro [start|stop|status] Pomodoro timer (API-only)
  /tn install [--source PATH]      Install/update skill into vault
  /tn check-update                 Check if installed skill is outdated
  /tn setup                        Install/configure CLI tools
  /tn help                         This help message

Common options:
  --vault PATH          Obsidian vault path
  --status VALUE        Task status (open, in-progress, done)
  --priority VALUE      Priority (low, normal, high)
  --due YYYY-MM-DD      Due date
  --scheduled YYYY-MM-DD  Scheduled date
  --tags "a,b"          Comma-separated tags
  --contexts "a,b"      Comma-separated contexts
  --projects "a,b"      Comma-separated projects
  --time-estimate N     Estimate in minutes
  --json                Machine-readable JSON output
  --file-only           Force file mode (skip API)

Filter options (for list):
  --tag TAG             Filter by tag
  --context CTX         Filter by context
  --project PROJ        Filter by project
  --overdue             Show only overdue tasks
  --today               Show tasks due/scheduled today
  --completed           Include completed tasks
  --where EXPR          Advanced filter expression

Tools: mtn (file mode) | tn (API mode) | obsidian CLI
Docs: https://tasknotes.dev/""")


# ---------------------------------------------------------------------------
# CLI Argument Parser
# ---------------------------------------------------------------------------


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser."""
    parser = argparse.ArgumentParser(
        prog="tn_manager",
        description="Obsidian TaskNotes Skill -- CLI Orchestrator",
    )
    parser.add_argument("--vault", help="Obsidian vault path")
    parser.add_argument("--json", action="store_true", help="JSON output")
    parser.add_argument("--file-only", action="store_true", help="Force file mode")
    parser.add_argument("--api-port", type=int, help="TaskNotes API port")
    parser.add_argument("--api-token", help="TaskNotes API auth token")

    sub = parser.add_subparsers(dest="command")

    # status
    sub.add_parser("status", help="Task overview and counts")

    # create
    p = sub.add_parser("create", help="Create a new task")
    p.add_argument("title", help="Task title")
    p.add_argument("--status", help="Task status")
    p.add_argument("--priority", help="Priority level")
    p.add_argument("--due", help="Due date (YYYY-MM-DD)")
    p.add_argument("--scheduled", help="Scheduled date (YYYY-MM-DD)")
    p.add_argument("--tags", help="Comma-separated tags")
    p.add_argument("--contexts", help="Comma-separated contexts")
    p.add_argument("--projects", help="Comma-separated projects")
    p.add_argument("--time-estimate", help="Time estimate in minutes")
    p.add_argument("--description", help="Task body/description")

    # nlp
    p = sub.add_parser("nlp", help="Create task from natural language")
    p.add_argument("text", help="Natural language task description")

    # update
    p = sub.add_parser("update", help="Update an existing task")
    p.add_argument("title", help="Task title to match")
    p.add_argument("--status", help="New status")
    p.add_argument("--priority", help="New priority")
    p.add_argument("--due", help="New due date")
    p.add_argument("--scheduled", help="New scheduled date")
    p.add_argument("--add-tag", help="Add a tag")
    p.add_argument("--remove-tag", help="Remove a tag")
    p.add_argument("--add-context", help="Add a context")
    p.add_argument("--remove-context", help="Remove a context")

    # complete
    p = sub.add_parser("complete", help="Mark task as completed")
    p.add_argument("title", help="Task title to match")

    # delete
    p = sub.add_parser("delete", help="Delete a task")
    p.add_argument("title", help="Task title to match")
    p.add_argument("--force", action="store_true", help="Skip confirmation")

    # list
    p = sub.add_parser("list", help="List and filter tasks")
    p.add_argument("--status", help="Filter by status")
    p.add_argument("--priority", help="Filter by priority")
    p.add_argument("--tag", help="Filter by tag")
    p.add_argument("--context", help="Filter by context")
    p.add_argument("--project", help="Filter by project")
    p.add_argument("--overdue", action="store_true", help="Show only overdue")
    p.add_argument("--today", action="store_true", help="Due/scheduled today")
    p.add_argument("--completed", action="store_true", help="Include completed")
    p.add_argument("--where", help="Advanced filter expression")

    # search
    p = sub.add_parser("search", help="Search tasks by content")
    p.add_argument("query", help="Search query")

    # today
    sub.add_parser("today", help="Tasks due or scheduled today")

    # overdue
    sub.add_parser("overdue", help="Overdue incomplete tasks")

    # start-timer
    p = sub.add_parser("start-timer", help="Start time tracking")
    p.add_argument("title", help="Task title")
    p.add_argument("-d", "--description", help="Time entry description")

    # stop-timer
    sub.add_parser("stop-timer", help="Stop time tracking")

    # timer-log
    p = sub.add_parser("timer-log", help="Show time tracking log")
    p.add_argument("--period", help="Period: today, week, month, all")

    # projects
    p = sub.add_parser("projects", help="List projects")
    p.add_argument("--show", help="Show specific project details")
    p.add_argument("--stats", action="store_true", help="Include statistics")

    # pomodoro
    p = sub.add_parser("pomodoro", help="Pomodoro timer (API-only)")
    p.add_argument("action", nargs="?", help="start, stop, pause, resume, status")

    # install
    p = sub.add_parser("install", help="Install/update skill into vault")
    p.add_argument("--source", help="Path to skill repo (default: auto-detect)")

    # check-update
    p = sub.add_parser("check-update", help="Check if installed skill is outdated")
    p.add_argument("--source", help="Path to skill repo (default: auto-detect)")

    # setup
    sub.add_parser("setup", help="Install/configure CLI tools")

    # help
    sub.add_parser("help", help="Show available commands")

    return parser


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------


def main():
    parser = build_parser()
    args = parser.parse_args()

    # Resolve vault path
    if not args.vault:
        vault = discover_vault()
        if vault:
            args.vault = str(vault)

    # Override API config from CLI args
    if hasattr(args, "api_port") and args.api_port:
        os.environ["TASKNOTES_API_PORT"] = str(args.api_port)
    if hasattr(args, "api_token") and args.api_token:
        os.environ["TASKNOTES_API_TOKEN"] = args.api_token

    # Route to command
    cmd = args.command or "status"
    commands = {
        "status": cmd_status,
        "create": cmd_create,
        "nlp": cmd_nlp,
        "update": cmd_update,
        "complete": cmd_complete,
        "delete": cmd_delete,
        "list": cmd_list,
        "search": cmd_search,
        "today": cmd_today,
        "overdue": cmd_overdue,
        "start-timer": cmd_start_timer,
        "stop-timer": cmd_stop_timer,
        "timer-log": cmd_timer_log,
        "projects": cmd_projects,
        "pomodoro": cmd_pomodoro,
        "install": cmd_install,
        "check-update": cmd_check_update,
        "setup": cmd_setup,
        "help": cmd_help,
    }

    handler = commands.get(cmd)
    if handler:
        handler(args)
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        cmd_help(args)
        sys.exit(1)


if __name__ == "__main__":
    main()
