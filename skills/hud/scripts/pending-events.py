#!/usr/bin/env python3
"""Print unconsumed HUD events from every live workspace, advancing cursors.

Designed to run as a UserPromptSubmit hook (and as an ad-hoc check by the
agent): when the user talks to the agent directly, anything they did in a HUD
since the last sync rides along as context. Silent and fast when no HUD server
is running or nothing is pending, so it is safe on every prompt.
"""
import json
import os
import sys
from pathlib import Path

ROOTS = ["/tmp/claude/hud", "/private/tmp/claude/hud"]  # same dir on macOS


def alive(pid: int) -> bool:
    if pid <= 0:
        return False
    try:
        os.kill(pid, 0)
        return True
    except ProcessLookupError:
        return False
    except PermissionError:  # exists, just not signalable from here
        return True


def live_workspaces():
    seen = set()
    for root in ROOTS:
        for marker in Path(root).glob("*/server.json"):
            workspace = marker.parent.resolve()
            if workspace in seen:
                continue
            seen.add(workspace)
            try:
                info = json.loads(marker.read_text())
            except (OSError, json.JSONDecodeError):
                continue
            if alive(int(info.get("pid", -1))):
                yield workspace


def main():
    for workspace in live_workspaces():
        events = workspace / "events.jsonl"
        cursor = workspace / ".events.cursor"
        try:
            offset = int(cursor.read_text() or 0) if cursor.exists() else 0
        except ValueError:
            offset = 0
        size = events.stat().st_size if events.exists() else 0
        if size < offset:
            cursor.write_text("0")
            offset = 0
        if size <= offset:
            continue
        with events.open("rb") as f:
            f.seek(offset)
            raw = f.read()
        cursor.write_text(str(offset + len(raw)))
        print(f"HUD events since last sync ({workspace}):")
        sys.stdout.write(raw.decode("utf-8", errors="replace"))


if __name__ == "__main__":
    main()
