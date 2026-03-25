#!/usr/bin/env python3
"""Obsidian TaskNotes Skill -- Shared Utilities

Common functions used by tn_manager.py:
- Vault auto-discovery
- CLI tool detection (mtn, tn, obsidian)
- Plugin settings loading
- API configuration and HTTP client
- Subprocess wrapper for CLI tools
"""

import json
import os
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime
from pathlib import Path

PLUGIN_DIR = ".obsidian/plugins/tasknotes"
DEFAULT_TASKS_FOLDER = "TaskNotes/Tasks"
DEFAULT_ARCHIVE_FOLDER = "TaskNotes/Archive"
DEFAULT_API_PORT = 8080
DEFAULT_API_HOST = "localhost"

DEFAULT_STATUSES = ["open", "in-progress", "done"]
DEFAULT_PRIORITIES = ["low", "normal", "high"]
DEFAULT_TASK_TAG = "task"

# ---------------------------------------------------------------------------
# Vault Discovery
# ---------------------------------------------------------------------------


def discover_vault(hint: str | None = None) -> Path | None:
    """Try to locate an Obsidian vault with the TaskNotes plugin.

    Search order:
    1. Explicit hint (if provided and contains .obsidian/)
    2. Current working directory (if contains .obsidian/)
    3. Common locations: ~/Documents/Obsidian, ~/Documents, ~/Obsidian, ~/

    Returns the first vault that has the TaskNotes plugin installed,
    or None if no suitable vault is found.
    """
    if hint:
        p = Path(hint).expanduser().resolve()
        if (p / ".obsidian").is_dir():
            return p
        return None

    # Check cwd
    cwd = Path.cwd()
    if (cwd / ".obsidian").is_dir():
        return cwd

    # Scan common parent directories for vaults with TaskNotes
    candidates: list[Path] = []
    search_roots = [
        Path.home() / "Documents" / "Obsidian",
        Path.home() / "Documents",
        Path.home() / "Obsidian",
        Path.home(),
    ]
    for root in search_roots:
        if not root.is_dir():
            continue
        for child in root.iterdir():
            if not child.is_dir() or not (child / ".obsidian").is_dir():
                continue
            # Prefer vaults with TaskNotes installed
            if (child / PLUGIN_DIR).is_dir():
                return child
            candidates.append(child)

    if len(candidates) == 1:
        return candidates[0]
    return None


# ---------------------------------------------------------------------------
# Plugin Settings
# ---------------------------------------------------------------------------


def plugin_data_path(vault_path: str) -> Path:
    """Return the path to TaskNotes data.json."""
    return Path(vault_path) / PLUGIN_DIR / "data.json"


def load_plugin_settings(vault_path: str) -> dict:
    """Load TaskNotes settings from data.json. Returns empty dict if not found."""
    dp = plugin_data_path(vault_path)
    if not dp.exists():
        return {}
    with open(dp, "r", encoding="utf-8") as f:
        return json.load(f)


def resolve_tasks_folder(vault_path: str, settings: dict | None = None) -> str:
    """Get the configured tasks folder path (relative to vault root)."""
    if settings is None:
        settings = load_plugin_settings(vault_path)
    return settings.get("tasksFolder", DEFAULT_TASKS_FOLDER)


def resolve_archive_folder(vault_path: str, settings: dict | None = None) -> str:
    """Get the configured archive folder path."""
    if settings is None:
        settings = load_plugin_settings(vault_path)
    return settings.get("archiveFolder", DEFAULT_ARCHIVE_FOLDER)


def resolve_statuses(settings: dict) -> list[dict]:
    """Extract configured status values from settings."""
    custom = settings.get("customStatuses", [])
    if custom:
        return custom
    return [
        {"value": s, "label": s.replace("-", " ").title(), "isCompleted": s == "done"}
        for s in DEFAULT_STATUSES
    ]


def resolve_priorities(settings: dict) -> list[dict]:
    """Extract configured priority values from settings."""
    custom = settings.get("customPriorities", [])
    if custom:
        return custom
    return [
        {"value": p, "label": p.title(), "weight": i}
        for i, p in enumerate(DEFAULT_PRIORITIES)
    ]


# ---------------------------------------------------------------------------
# Tool Detection
# ---------------------------------------------------------------------------


def detect_tools() -> dict[str, str | None]:
    """Detect available CLI tools. Returns {name: path_or_None}."""
    return {
        "mtn": shutil.which("mtn"),
        "tn": shutil.which("tn"),
        "obsidian": shutil.which("obsidian"),
    }


def require_any_tool(tools: dict[str, str | None]) -> None:
    """Exit with guidance if no CLI tools are available."""
    if not tools["mtn"] and not tools["tn"]:
        print("Error: No TaskNotes CLI tools found.", file=sys.stderr)
        print("Install them with: /tn setup", file=sys.stderr)
        print("  mtn (file mode):  npm install -g mdbase-tasknotes", file=sys.stderr)
        print("  tn  (API mode):   See /tn setup for instructions", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# API Configuration & Client
# ---------------------------------------------------------------------------


def resolve_api_config(
    vault_path: str | None = None,
    port_override: int | None = None,
    token_override: str | None = None,
) -> dict:
    """Resolve API URL and auth token.

    Priority: explicit args > env vars > plugin settings > defaults.
    """
    # Port
    port = port_override
    if port is None:
        port = os.environ.get("TASKNOTES_API_PORT")
        if port:
            port = int(port)
    if port is None and vault_path:
        settings = load_plugin_settings(vault_path)
        port = settings.get("apiPort", DEFAULT_API_PORT)
    if port is None:
        port = DEFAULT_API_PORT

    # Token
    token = token_override
    if token is None:
        token = os.environ.get("TASKNOTES_API_TOKEN")
    if token is None and vault_path:
        settings = load_plugin_settings(vault_path)
        t = settings.get("apiAuthToken", "")
        if t:
            token = t

    return {
        "base_url": f"http://{DEFAULT_API_HOST}:{port}",
        "token": token,
    }


def check_api_available(api_config: dict, timeout: float = 2.0) -> bool:
    """Check if the TaskNotes HTTP API is reachable."""
    url = f"{api_config['base_url']}/api/health"
    req = urllib.request.Request(url)
    if api_config.get("token"):
        req.add_header("Authorization", f"Bearer {api_config['token']}")
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.status == 200
    except Exception:
        return False


def api_request(
    method: str,
    path: str,
    api_config: dict,
    body: dict | None = None,
    params: dict | None = None,
) -> dict:
    """Make an HTTP request to the TaskNotes API.

    Returns parsed JSON response. Raises on HTTP errors.
    """
    url = f"{api_config['base_url']}{path}"
    if params:
        url += "?" + urllib.parse.urlencode(params)

    data = None
    if body is not None:
        data = json.dumps(body).encode("utf-8")

    req = urllib.request.Request(url, data=data, method=method)
    req.add_header("Content-Type", "application/json")
    if api_config.get("token"):
        req.add_header("Authorization", f"Bearer {api_config['token']}")

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        body_text = e.read().decode("utf-8", errors="replace")
        try:
            err = json.loads(body_text)
            msg = err.get("error", body_text)
        except json.JSONDecodeError:
            msg = body_text
        print(f"API Error ({e.code}): {msg}", file=sys.stderr)
        sys.exit(1)
    except urllib.error.URLError as e:
        print(f"API connection error: {e.reason}", file=sys.stderr)
        sys.exit(1)


# ---------------------------------------------------------------------------
# CLI Subprocess Wrapper
# ---------------------------------------------------------------------------


def run_cli(
    tool: str,
    args: list[str],
    json_out: bool = False,
    capture: bool = True,
    env_extra: dict | None = None,
) -> dict | str | None:
    """Run an external CLI tool and return its output.

    If json_out is True, parses stdout as JSON and returns the dict.
    Otherwise returns stdout as a string.
    """
    cmd = [tool] + args
    env = os.environ.copy()
    if env_extra:
        env.update(env_extra)

    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            env=env,
            timeout=30,
        )
    except FileNotFoundError:
        print(f"Error: '{tool}' not found in PATH.", file=sys.stderr)
        sys.exit(1)
    except subprocess.TimeoutExpired:
        print(f"Error: '{tool}' command timed out.", file=sys.stderr)
        sys.exit(1)

    if result.returncode != 0:
        stderr = result.stderr.strip() if result.stderr else ""
        if stderr:
            print(f"{tool} error: {stderr}", file=sys.stderr)
        else:
            stdout = result.stdout.strip() if result.stdout else ""
            if stdout:
                print(f"{tool}: {stdout}", file=sys.stderr)
            else:
                print(f"{tool} exited with code {result.returncode}", file=sys.stderr)
        return None

    stdout = result.stdout.strip() if result.stdout else ""
    if json_out and stdout:
        try:
            return json.loads(stdout)
        except json.JSONDecodeError:
            # Some tools mix text + JSON; try to extract JSON
            for line in stdout.split("\n"):
                line = line.strip()
                if line.startswith("{") or line.startswith("["):
                    try:
                        return json.loads(line)
                    except json.JSONDecodeError:
                        continue
            # Return raw text if JSON parsing fails
            return {"_raw": stdout}
    return stdout if stdout else None


# ---------------------------------------------------------------------------
# Output Helpers
# ---------------------------------------------------------------------------


def output(data, human_fn, *, json_mode: bool = False):
    """If json_mode, print JSON; otherwise call human_fn."""
    if json_mode:
        if isinstance(data, str):
            print(data)
        else:
            print(json.dumps(data, indent=2, ensure_ascii=False))
    else:
        human_fn()


# ---------------------------------------------------------------------------
# Date Helpers
# ---------------------------------------------------------------------------


def today_str() -> str:
    """Return today's date as YYYY-MM-DD."""
    return datetime.now().strftime("%Y-%m-%d")


def now_iso() -> str:
    """Return current datetime as ISO 8601 string."""
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
