#!/usr/bin/env python3
"""Block until new user events land in <workspace>/events.jsonl, print them, exit.

A cursor file (<workspace>/.events.cursor) remembers how far previous runs read,
so events that arrive between runs are never lost. Run it again after handling
the output to keep listening.

Usage: watch-events.py <workspace> [--timeout SECONDS]   (default 600)
Exits 0 with the new JSON lines on stdout, or 0 with "TIMEOUT" if nothing came.
"""
import argparse
import sys
import time
from pathlib import Path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("workspace")
    parser.add_argument("--timeout", type=float, default=600)
    args = parser.parse_args()

    events = Path(args.workspace) / "events.jsonl"
    cursor = Path(args.workspace) / ".events.cursor"
    offset = int(cursor.read_text() or 0) if cursor.exists() else 0

    deadline = time.time() + args.timeout
    while time.time() < deadline:
        size = events.stat().st_size if events.exists() else 0
        if size < offset:  # file was truncated/reset
            offset = 0
        if size > offset:
            with events.open("rb") as f:
                f.seek(offset)
                new = f.read()
            cursor.write_text(str(size))
            sys.stdout.write(new.decode("utf-8", errors="replace"))
            return
        time.sleep(0.2)
    print(f"TIMEOUT: no user events after {int(args.timeout)}s")


if __name__ == "__main__":
    main()
