---
name: agent-platform
description: Run or control a heartbeat-driven autonomous agent platform for the current project. Use only when the user invokes `/agent-platform`, asks to start, stop, resume, or inspect an overnight autonomous agent loop, or when a scheduled prompt says `agent-platform heartbeat`. Each heartbeat rereads `HEART.md`, delegates bounded work to suitable subagents and models, appends a durable summary to `LOG.md`, and schedules the next heartbeat inside the approved work window.
argument-hint: "[start | stop | status | heartbeat — defaults to start]"
compatibility: Requires file access. Autonomous operation requires subagent and scheduler or wakeup support; otherwise run one heartbeat and report the limitation.
---

# agent-platform

Run **one bounded heartbeat at a time**. Never hold an LLM turn open with an infinite loop. Persist intent and state to disk, finish the turn, then let the scheduler wake the main agent again.

## Durable control plane

| File | Owner | Rule |
|---|---|---|
| `HEART.md` | User | The current mission, priorities, constraints, permissions, and stop conditions. Read it fully every heartbeat. Never edit it unless asked. |
| `LOG.md` | Platform | Append one compact summary per heartbeat. Read only the recent tail unless older history is needed. |
| `.agent-platform/state.json` | Platform | Local machine state: status, heartbeat interval, active window, timezone, agent limit, model map, last HEART hash, next wake, and scheduler task IDs. |

Do not add these files to git or `.gitignore` unless the user asks. `HEART.md` is authoritative immediately: a change on disk overrides the previous plan at the next heartbeat.

## Commands

### `start`

1. Resolve the project root and inspect the harness before making assumptions:
   - Which scheduler or wakeup mechanism exists?
   - Which subagent, team, or workflow primitives exist?
   - Which models are actually exposed by the runtime, settings, or provider?
2. Build a model map without paid probe calls:
   - **fast** — status checks, searches, mechanical edits, log synthesis
   - **general** — normal implementation and investigation
   - **strong** — architecture, ambiguity, adversarial review, failed attempts
   - **inherit** — safe fallback when availability cannot be enumerated
   Use the cheapest sufficient model. Record identifiers and evidence in state and the first log entry.
3. Ask one compact setup question for anything missing: heartbeat interval, active window, timezone, and maximum concurrent subagents. Default the maximum to `2`; do not invent the time settings.
4. Create `.agent-platform/state.json`. If `HEART.md` is absent, create this minimal template and stop for the user to fill it unless their invocation already supplies the mission:

```markdown
# Mission

# Current priorities

# Constraints and permissions

# Stop conditions
```

5. Create `LOG.md` if absent. If currently inside the active window, run the first heartbeat. Otherwise schedule exactly one wake at the next window start and stop.

### `heartbeat`

The main agent owns the heartbeat. Subagents may do work but must never schedule the next wake.

1. **Gate on time first.** Run `scripts/window.py` from this skill with the configured window. If outside the window, schedule the returned `next_wake`, update state, and stop without spawning agents. The active window is a hard spending ceiling, not a target.
2. Read `HEART.md` fully, hash it, and read only the recent tail of `LOG.md`. If HEART changed, discard any stale plan that conflicts with it.
3. Check stop conditions and blockers. Stop the platform when instructed; otherwise select the smallest useful bounded work for this heartbeat.
4. Delegate only when it helps:
   - subagents for focused independent tasks;
   - agent teams only when workers must communicate;
   - scripted workflows only for repeatable high-fan-out work.
   Cap concurrency from state. Disable nested spawning unless HEART explicitly allows it.
5. Route each task through the model map. Do not spend a strong model on polling or mechanical work. If a model is unavailable, fall back, update the map, and do not repeatedly probe it.
6. Verify completed work. Do not start work likely to cross the end of the active window; when less than one heartbeat interval remains, prefer synthesis, logging, or stopping early.
7. Append one log entry, update state, and schedule exactly one next wake:
   - `now + interval` when that remains inside the window;
   - otherwise the next window start.
8. End the turn. Never overlap heartbeats or leave multiple wakeups armed.

### `status`

Read state plus the latest log entry and report: running state, HEART hash/change status, model map, current workers, last result, and next wake. Do not perform work.

### `stop`

Cancel only scheduler tasks recorded in state, mark the platform stopped, append a final log entry, and leave `HEART.md` and `LOG.md` intact.

## Log shape

```markdown
## <timestamp and timezone> — heartbeat

- **HEART:** <hash prefix> — changed | unchanged
- **Intent:** <one-line objective followed this heartbeat>
- **Agents:** <role — model — result; or none>
- **Work:** <what changed or was learned>
- **Checks:** <verification performed>
- **Blockers:** <none or concrete blocker>
- **Next:** <next useful action> — wake <timestamp>
```

Keep entries compact. `LOG.md` is durable operational memory, not a transcript or chain-of-thought dump.

## Harness notes

When running on Claude Code, read [`references/claude-code.md`](references/claude-code.md) before scheduling or choosing orchestration primitives.

## Anti-patterns

- `while true`, shell `sleep`, or a model turn kept alive indefinitely.
- A recurring schedule that fires outside the approved window.
- Reading the entire growing `LOG.md` every heartbeat.
- Spending calls merely to discover whether a model exists.
- Spawning a team for sequential work or allowing recursive fan-out by default.
- Editing `HEART.md`, ignoring a changed hash, or continuing a stale plan.
- Starting new work near the window boundary and spilling into the user's daytime plan.
- Pushing, deploying, deleting, spending money, or contacting people unless HEART explicitly authorizes that class of action.
