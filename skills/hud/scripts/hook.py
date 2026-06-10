#!/usr/bin/env python3
"""Install or remove the HUD prompt hook in the current project, leaving no trace.

`install` merges a UserPromptSubmit hook running pending-events.py into
<project>/.claude/settings.local.json (created if needed) and excludes that file
via .git/info/exclude — never .gitignore, so the repo itself is untouched.
`remove` deletes exactly what install added; if the settings file ends up empty
it is deleted too. Both are idempotent.

Claude Code only; hooks load at session start, so a freshly installed hook may
need the user to open /hooks once (or a new session) to take effect.

Usage: hook.py install|remove [--project DIR]
"""
import argparse
import json
import sys
from pathlib import Path

PENDING = Path(__file__).resolve().parent / "pending-events.py"
HOOK = {"type": "command", "command": f"python3 {PENDING}", "timeout": 10}
EXCLUDE_LINE = ".claude/settings.local.json"


def load(path: Path) -> dict:
    try:
        return json.loads(path.read_text())
    except (OSError, json.JSONDecodeError):
        return {}


def is_ours(hook: dict) -> bool:
    return hook.get("type") == "command" and "pending-events.py" in hook.get("command", "")


def ensure_git_exclude(project: Path):
    info = project / ".git" / "info"
    if not info.is_dir():
        return
    exclude = info / "exclude"
    lines = exclude.read_text().splitlines() if exclude.exists() else []
    if EXCLUDE_LINE not in lines:
        exclude.write_text("\n".join(lines + [EXCLUDE_LINE]) + "\n")


def install(project: Path):
    settings_path = project / ".claude" / "settings.local.json"
    settings = load(settings_path)
    groups = settings.setdefault("hooks", {}).setdefault("UserPromptSubmit", [])
    if any(is_ours(h) for g in groups for h in g.get("hooks", [])):
        print(f"already installed: {settings_path}")
        return
    groups.append({"hooks": [HOOK]})
    settings_path.parent.mkdir(parents=True, exist_ok=True)
    settings_path.write_text(json.dumps(settings, indent=2) + "\n")
    ensure_git_exclude(project)
    print(f"installed: {settings_path}")


def remove(project: Path):
    settings_path = project / ".claude" / "settings.local.json"
    if not settings_path.exists():
        print("nothing to remove")
        return
    settings = load(settings_path)
    groups = settings.get("hooks", {}).get("UserPromptSubmit", [])
    for group in groups:
        group["hooks"] = [h for h in group.get("hooks", []) if not is_ours(h)]
    groups = [g for g in groups if g.get("hooks")]
    if groups:
        settings["hooks"]["UserPromptSubmit"] = groups
    else:
        settings.get("hooks", {}).pop("UserPromptSubmit", None)
        if not settings.get("hooks"):
            settings.pop("hooks", None)
    if settings:
        settings_path.write_text(json.dumps(settings, indent=2) + "\n")
        print(f"removed hook, kept other settings: {settings_path}")
    else:
        settings_path.unlink()
        print(f"removed: {settings_path}")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("action", choices=["install", "remove"])
    parser.add_argument("--project", default=".", help="project root (default: cwd)")
    args = parser.parse_args()

    project = Path(args.project).resolve()
    if not PENDING.exists():
        sys.exit(f"pending-events.py not found at {PENDING}")
    (install if args.action == "install" else remove)(project)


if __name__ == "__main__":
    main()
