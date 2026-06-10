#!/usr/bin/env python3
"""Block until the user nudges the HUD, then print all unconsumed events and exit.

Events accumulate silently in <workspace>/events.jsonl; this script wakes when a
line with "type": "nudge" arrives (or on any new line with --on any), prints the
whole backlog since the cursor, advances <workspace>/.events.cursor, and exits.
Run it again after handling the output to keep listening.

The cursor file is re-read on every poll, so events consumed elsewhere (e.g. by
pending-events.py when the user talks to the agent directly) are never delivered
twice.

Usage: watch-events.py <workspace> [--on nudge|any] [--timeout SECONDS]
Exits 0 with the new JSON lines on stdout, or 0 with "TIMEOUT" if nothing came.
"""
import argparse
import json
import sys
import time
from pathlib import Path


def read_cursor(cursor: Path) -> int:
    try:
        return int(cursor.read_text() or 0)
    except (OSError, ValueError):
        return 0


def has_nudge(text: str) -> bool:
    for line in text.splitlines():
        if not line.strip():
            continue
        try:
            if json.loads(line).get("type") == "nudge":
                return True
        except json.JSONDecodeError:  # partial line still being written
            continue
    return False


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--on", choices=["nudge", "any"], default="nudge", dest="wake")
    parser.add_argument("--timeout", type=float, default=600)
    args = parser.parse_args()

    events = Path(args.workspace) / "events.jsonl"
    cursor = Path(args.workspace) / ".events.cursor"

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        offset = read_cursor(cursor)
        size = events.stat().st_size if events.exists() else 0
        if size < offset:  # file was truncated/reset
            cursor.write_text("0")
            continue
        if size > offset:
            with events.open("rb") as f:
                f.seek(offset)
                raw = f.read()
            new = raw.decode("utf-8", errors="replace")
            if args.wake == "any" or has_nudge(new):
                cursor.write_text(str(offset + len(raw)))
                sys.stdout.write(new)
                return
        time.sleep(0.2)
    waited_for = "user events" if args.wake == "any" else "nudge"
    print(f"TIMEOUT: no {waited_for} after {int(args.timeout)}s")


if __name__ == "__main__":
    main()
