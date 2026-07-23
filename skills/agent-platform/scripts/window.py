#!/usr/bin/env python3
"""Calculate an overnight work window and the next safe heartbeat time."""

from __future__ import annotations

import argparse
import json
from dataclasses import asdict, dataclass
from datetime import datetime, time, timedelta
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


@dataclass(frozen=True)
class WindowResult:
    now: str
    in_window: bool
    window_start: str
    window_end: str
    remaining_minutes: int
    next_wake: str


def parse_hhmm(value: str) -> time:
    try:
        parsed = datetime.strptime(value, "%H:%M")
    except ValueError as exc:
        raise argparse.ArgumentTypeError("expected HH:MM in 24-hour time") from exc
    return parsed.time()


def localize(day: datetime, clock: time, tz: ZoneInfo) -> datetime:
    return datetime.combine(day.date(), clock, tzinfo=tz)


def bounds(now: datetime, start: time, end: time) -> tuple[datetime, datetime, bool]:
    if start == end:
        raise ValueError("start and end must differ; a 24-hour window is not allowed")

    crosses_midnight = start > end
    today_start = localize(now, start, now.tzinfo)  # type: ignore[arg-type]
    today_end = localize(now, end, now.tzinfo)  # type: ignore[arg-type]

    if not crosses_midnight:
        if today_start <= now < today_end:
            return today_start, today_end, True
        if now < today_start:
            return today_start, today_end, False
        tomorrow = now + timedelta(days=1)
        return localize(tomorrow, start, now.tzinfo), localize(tomorrow, end, now.tzinfo), False  # type: ignore[arg-type]

    if now >= today_start:
        return today_start, localize(now + timedelta(days=1), end, now.tzinfo), True  # type: ignore[arg-type]
    if now < today_end:
        return localize(now - timedelta(days=1), start, now.tzinfo), today_end, True  # type: ignore[arg-type]
    return today_start, localize(now + timedelta(days=1), end, now.tzinfo), False  # type: ignore[arg-type]


def calculate(now: datetime, start: time, end: time, interval_minutes: int) -> WindowResult:
    window_start, window_end, in_window = bounds(now, start, end)
    if in_window:
        candidate = now + timedelta(minutes=interval_minutes)
        next_wake = candidate if candidate < window_end else bounds(window_end, start, end)[0]
        remaining = max(0, int((window_end - now).total_seconds() // 60))
    else:
        next_wake = window_start
        remaining = 0

    return WindowResult(
        now=now.isoformat(timespec="seconds"),
        in_window=in_window,
        window_start=window_start.isoformat(timespec="seconds"),
        window_end=window_end.isoformat(timespec="seconds"),
        remaining_minutes=remaining,
        next_wake=next_wake.isoformat(timespec="seconds"),
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--start", required=True, type=parse_hhmm)
    parser.add_argument("--end", required=True, type=parse_hhmm)
    parser.add_argument("--timezone", required=True)
    parser.add_argument("--interval-minutes", required=True, type=int)
    parser.add_argument("--now", help="ISO datetime for testing; defaults to current time")
    args = parser.parse_args()

    if args.interval_minutes < 1:
        parser.error("--interval-minutes must be at least 1")

    try:
        tz = ZoneInfo(args.timezone)
    except ZoneInfoNotFoundError as exc:
        parser.error(f"unknown timezone: {args.timezone}")
        raise AssertionError from exc

    if args.now:
        try:
            now = datetime.fromisoformat(args.now)
        except ValueError as exc:
            parser.error("--now must be an ISO datetime")
            raise AssertionError from exc
        now = now.replace(tzinfo=tz) if now.tzinfo is None else now.astimezone(tz)
    else:
        now = datetime.now(tz)

    try:
        result = calculate(now, args.start, args.end, args.interval_minutes)
    except ValueError as exc:
        parser.error(str(exc))

    print(json.dumps(asdict(result), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
