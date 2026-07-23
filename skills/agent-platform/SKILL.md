---
name: agent-platform
description: Operate the repository's lightweight self-regulating agent platform. Use only when the user invokes `/agent-platform`, asks to start, stop, resume, or inspect it, or when a scheduled prompt says `agent-platform heartbeat`.
argument-hint: "[start | stop | status | heartbeat — defaults to start]"
compatibility: Requires file access. Autonomous operation requires subagent and scheduler or wakeup support; otherwise run one heartbeat and report the limitation.
---

# agent-platform

Run **one bounded heartbeat at a time**. Never hold an LLM turn open with an infinite loop. Persist intent and state to disk, finish the turn, then let the scheduler wake the main agent again.

## Safety envelope — verify before starting

The platform should run autonomously **inside the current repository**, not with unrestricted machine access.

1. Resolve the current working directory and repository root.
2. Inspect the harness's effective permission, sandbox, and writable-directory settings. Confirm writes and shell commands are confined to this repository; do not add parent directories, sibling repositories, or broad home-directory access.
3. Use `auto` mode or the closest equivalent: non-interactive execution with the repository sandbox still enforced. On Claude Code, prefer `auto`; do not use `bypassPermissions` or `--dangerously-skip-permissions` as a substitute for sandboxed autonomy.
4. Confirm subagents inherit the same boundary and permission mode.
5. If the harness cannot provide both autonomous execution and a repository-local boundary, do not start. Tell the user the exact setting or restart command required.
6. Record the verified root, sandbox boundary, and permission mode in state and the first log entry.

## Repository authority

Once started, the platform owns the repository for the mission defined in `HEART.md`. It may autonomously:

- inspect, create, edit, move, and delete repository files;
- create notes, plans, research, state, and other working artifacts;
- write and run code, scripts, tests, builds, formatters, migrations, and experiments;
- install or update project-local dependencies;
- create local branches and commits;
- use available tools and delegate work to subagents.

Do not ask for permission for ordinary repository-local work. Follow the repository's own instructions and verify meaningful changes. `HEART.md` may narrow this authority at any time.

The repository boundary is real. Pushing or merging, deploying, contacting people, spending money, changing external services, exposing secrets, or destructive work outside the repository still requires explicit authorization in `HEART.md` or from the user.

## How the user uses it

On first start, briefly explain:

- `HEART.md` is the live control surface: the user may edit it at any time, including while the platform is running. Changes take effect on the next heartbeat.
- `LOG.md` is the readable operational history: what ran, what changed, blockers, and what happens next.
- `/agent-platform status` shows the current state and next wake without doing work.
- `/agent-platform stop` cancels future wakeups but preserves HEART and LOG.
- Work happens only inside the configured active window. Outside it, the platform schedules the next window start and spends no agent calls.

Do not bury this in setup output. The user should understand how to steer and stop the platform before autonomous work begins.

## Durable control plane

| File | Owner | Rule |
|---|---|---|
| `HEART.md` | User | The current mission, priorities, restrictions, external permissions, and stop conditions. Read it fully every heartbeat. Never edit it unless asked. |
| `LOG.md` | Platform | Append one compact summary per heartbeat. Read only the recent tail unless older history is needed. |
| `.agent-platform/state.json` | Platform | Local state: status, verified sandbox, permission mode, heartbeat interval, active window, timezone, agent limit, model map, last HEART hash, next wake, and scheduler task IDs. |

Do not add these files to git or `.gitignore` unless the user asks. `HEART.md` is authoritative immediately: a change on disk overrides the previous plan at the next heartbeat.

## Commands

### `start`

1. Verify the safety envelope above before doing autonomous work.
2. Inspect the harness before making assumptions:
   - Which scheduler or wakeup mechanism exists?
   - Which subagent, team, or workflow primitives exist?
   - Which models are actually exposed by the runtime, settings, or provider?
3. Build a model map without paid probe calls:
   - **fast** — status checks, searches, mechanical edits, log synthesis
   - **general** — normal implementation and investigation
   - **strong** — architecture, ambiguity, adversarial review, failed attempts
   - **inherit** — safe fallback when availability cannot be enumerated
   Use the cheapest sufficient model. Record identifiers and evidence in state and the first log entry.
4. Ask one compact setup question for anything missing: heartbeat interval, active window, timezone, and maximum concurrent subagents. Default the maximum to `2`; do not invent the time settings.
5. If `HEART.md` is absent, do **not** silently drop a blank file and leave. Explain that HEART is the live-editable mission file and offer two concrete paths:
   - **Interactive setup** — ask one question at a time to establish the mission, priorities, restrictions, external permissions, and stop conditions, then write the agreed HEART.
   - **Edit directly** — create the template below, show its path, and pause until the user edits it.

```markdown
# Mission

# Current priorities

# Restrictions

# External effects allowed

# Stop conditions
```

Normal repository-local work is already authorized by this skill; HEART only needs to state restrictions or authorize external effects. If the invocation already contains a clear mission, use it to draft HEART, show the draft, and ask only about missing restrictions or stop conditions before starting.
6. Create `.agent-platform/state.json` and `LOG.md` if absent.
7. Print a compact start summary containing the repository root, sandbox and permission mode, HEART path, LOG path, active window, heartbeat interval, model routing, concurrency cap, and the commands `status` and `stop`. Explicitly say: **“You can edit HEART.md live; the next heartbeat will pick up the change.”**
8. If currently inside the active window, run the first heartbeat. Otherwise schedule exactly one wake at the next window start and stop.

### `heartbeat`

The main agent owns the heartbeat. Subagents may do work but must never schedule the next wake.

1. **Gate on time first.** Run `scripts/window.py` from this skill with the configured window. If outside the window, schedule the returned `next_wake`, update state, and stop without spawning agents. The active window is a hard spending ceiling, not a target.
2. Reconfirm that the effective working root and sandbox have not widened. Stop and report if the safety envelope changed.
3. Read `HEART.md` fully, hash it, and read only the recent tail of `LOG.md`. If HEART changed, discard any stale plan that conflicts with it and note the change in the log.
4. Check stop conditions and blockers. Stop the platform when instructed; otherwise select the smallest useful bounded work for this heartbeat.
5. Delegate only when it helps:
   - subagents for focused independent tasks;
   - agent teams only when workers must communicate;
   - scripted workflows only for repeatable high-fan-out work.
   Cap concurrency from state. Disable nested spawning unless HEART explicitly allows it.
6. Route each task through the model map. Do not spend a strong model on polling or mechanical work. If a model is unavailable, fall back, update the map, and do not repeatedly probe it.
7. Verify completed work. Do not start work likely to cross the end of the active window; when less than one heartbeat interval remains, prefer synthesis, logging, or stopping early.
8. Append one log entry, update state, and schedule exactly one next wake:
   - `now + interval` when that remains inside the window;
   - otherwise the next window start.
9. End the turn. Never overlap heartbeats or leave multiple wakeups armed.

### `status`

Read state plus the latest log entry and report: running state, repository root, sandbox and permission mode, HEART path and latest hash/change status, model map, current workers, last result, and next wake. Remind the user that HEART is live-editable. Do not perform work.

### `stop`

Cancel only scheduler tasks recorded in state, mark the platform stopped, append a final log entry, and leave `HEART.md` and `LOG.md` intact. Tell the user that `/agent-platform start` resumes from those files later.

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

When running on Claude Code, read [`references/claude-code.md`](references/claude-code.md) before configuring permissions, scheduling, or choosing orchestration primitives.

## Anti-patterns

- `while true`, shell `sleep`, or a model turn kept alive indefinitely.
- Autonomous mode without first verifying the repository sandbox.
- Using blanket permission bypass when safe auto mode exists.
- Asking permission for ordinary work inside the owned repository.
- Creating an empty HEART without explaining how the user controls it.
- Hiding the live-edit and stop controls in verbose setup output.
- A recurring schedule that fires outside the approved window.
- Reading the entire growing `LOG.md` every heartbeat.
- Spending calls merely to discover whether a model exists.
- Spawning a team for sequential work or allowing recursive fan-out by default.
- Editing `HEART.md`, ignoring a changed hash, or continuing a stale plan.
- Starting new work near the window boundary and spilling into the user's daytime plan.
- Pushing, deploying, deleting outside the repository, spending money, or contacting people unless HEART explicitly authorizes that class of action.
