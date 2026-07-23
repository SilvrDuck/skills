---
name: agent-platform
description: Operate the repository's lightweight self-regulating agent platform. Use only when the user invokes `/agent-platform`, asks to start, resume, stop, or inspect it, or when a scheduled prompt says `agent-platform heartbeat`.
argument-hint: "[start | resume | stop | status | heartbeat — defaults to start]"
compatibility: Requires repository file access. Unattended operation requires a supported headless harness and a durable macOS or Linux host scheduler.
---

# agent-platform

Run **one bounded heartbeat at a time**. Never hold an LLM turn open with an infinite loop. Persist intent and state to disk, end the process, and let a durable host scheduler invoke the next heartbeat.

The goal is a genuinely unattended, self-regulating platform: it owns the repository, evolves its internal organization, repairs its runtime, uses the user's fixed subscription allowance parsimoniously, and remains live-steerable through `HEART.md`.

## Hard invariants

1. **Zero marginal cost.** Never use API keys, pay-as-you-go providers, credit balances, paid add-ons, extra usage, or any route that may create a separate bill. Every lead and subagent model must be verified as included in the user's fixed-limit plan. If billing mode cannot be verified, do not start.
2. **Repository-contained autonomy.** Work freely inside the resolved repository; never widen the writable boundary silently.
3. **Durable headlessness.** An unattended platform uses a host scheduler that survives terminal, SSH, and harness sessions. Session wake tools are only a temporary interactive fallback.
4. **Finite heartbeats.** Exactly one bounded run per invocation, protected against overlap and hangs.
5. **User control.** `HEART.md` is authoritative and live-editable. Re-read it fully every heartbeat.
6. **Working hours are configured, never assumed.** They are a spending ceiling, not a quota to consume.
7. **Prove it works.** Do not report unattended setup as successful until the real headless command, environment, lock, logs, and scheduler have been verified.

## Settings gate — every start or resume

Before mission work or host changes, inspect the harness and display one compact settings panel:

| Setting | Rule |
|---|---|
| Repository root | Resolved current repository; never inferred beyond it |
| Harness and billing | Fixed-plan identity verified; metered credentials absent |
| Sandbox / permission mode | Non-interactive inside the repository, safety boundary retained |
| Working hours | Required daily start, end, and timezone; **no default** |
| Heartbeat interval | Required; **no default** |
| Agent budget | Fixed cap or **token-managed, no fixed cap** |
| Scheduler | Preferred durable host mechanism detected |
| Model routing | Verified fixed-plan fast, general, and strong candidates |
| Token policy | Cheapest sufficient model; strongest tier used parsimoniously |
| Host installation | Exact files and scheduler changes proposed before consent |

Use the harness's structured multiple-choice widget when available. Show resolved values first, then offer **Start as shown**, **Edit schedule**, **Edit agents/models**, **Advanced**, or **Cancel**. Collect missing values before offering Start. Use concrete choices with a custom-value escape.

The settings review is the visible launch gate. A scheduled `heartbeat` skips it and uses accepted state.

## Safety envelope

1. Resolve the current directory and repository root.
2. Inspect effective permissions, sandbox, writable directories, provider, authentication, and billing source.
3. Reject metered credentials and providers. Do not export or fall back to API keys.
4. Use the closest repository-scoped, non-interactive mode described in the matching harness reference. Never use blanket bypass merely to avoid prompts.
5. Confirm subagents inherit the same repository boundary, billing source, and permission policy.
6. If autonomous execution and the required boundary cannot coexist, stop and explain the exact remediation.
7. Record the verified root, billing mode, sandbox, executable, and permission mode in state.

A harness allowlist is not necessarily an OS filesystem jail. Explain that distinction. Offer optional OS hardening, but do not require it unless the user asks or the repository is untrusted.

## Repository authority and self-design

Once started, the platform owns the repository for the mission in `HEART.md`. Without further permission it may:

- inspect, create, edit, move, and delete repository files;
- write and run code, scripts, tests, builds, formatters, migrations, and experiments;
- install or update project-local dependencies;
- create local branches and commits;
- create notes, plans, queues, roles, state files, checks, agents, and workflows;
- reorganize its own internal operating model as the mission evolves;
- use available tools and delegate bounded work to subagents.

Follow repository instructions and verify meaningful changes. `HEART.md` may narrow this authority at any time.

Pushing or merging, deploying, contacting people, spending money, changing external services, exposing secrets, or destructive work outside the repository still requires explicit authorization in `HEART.md` or from the user.

## User control surface

On first start, briefly explain:

- `HEART.md` is live-editable; changes take effect on the next heartbeat.
- `LOG.md` is a terse human timeline, not a transcript.
- `.agent-platform/` contains machine state, detailed working memory, raw runtime logs, and generated host configuration.
- `/agent-platform status` audits the platform without mission work.
- `/agent-platform stop` disables future host wakes but preserves state.
- `/agent-platform resume` reuses saved state after displaying the settings gate.

Do not bury these controls in verbose setup output.

## Durable control plane

| Path | Owner | Rule |
|---|---|---|
| `HEART.md` | User | Mission, priorities, restrictions, external permissions, and stop conditions. Never edit unless asked. |
| `LOG.md` | Platform | One terse state-first line per heartbeat. |
| `.agent-platform/state.json` | Platform | Runtime, billing, schedule, models, HEART hash, token policy, health, and scheduler identifiers. |
| `.agent-platform/state/` | Platform | Detailed plans, queues, rationale, worker reports, and durable working memory. |
| `.agent-platform/heartbeat.*` | Platform | Generated headless wrapper for this host and harness. |
| `.agent-platform/runtime.log` | Platform | Raw headless stdout/stderr for debugging. |
| `.agent-platform/host/` | Platform | Copy of generated launchd, systemd, cron, or equivalent configuration. |

Do not add these files to git or `.gitignore` unless asked. A HEART change overrides stale plans at the next heartbeat.

Store scheduler ownership explicitly:

```json
{
  "scheduler": {
    "type": "launchd | systemd-user | cron | session",
    "self_schedule": false,
    "detail": "host-specific installed schedule",
    "ids": [],
    "note": "The host scheduler is the sole durable scheduler."
  }
}
```

`self_schedule` is `false` for durable host scheduling. Set it to `true` only for an explicitly temporary session scheduler, and never describe that mode as unattended.

## Commands

### `start` / `resume`

1. Read the matching harness reference. Inspect the OS, harness version, real executable, authentication, fixed-plan billing, model catalog, sandbox, scheduler options, and repository instructions without paid probe calls.
2. Audit any existing platform runtime. Repair repository-local drift automatically. Include host-level repairs in the installation proposal.
3. Resolve and display the settings gate. Working hours and heartbeat interval must be explicit. Agent budget supports either a numeric cap or **token-managed, no fixed cap**.
4. Build a verified fixed-plan model map:
   - **fast** — polling, extraction, mechanical work, and log synthesis;
   - **general** — heartbeat lead, normal implementation, and investigation;
   - **strong** — rare deep synthesis, hard diagnosis, or adversarial review;
   - **inherit** — fallback only when it is verified to remain inside the same fixed plan.
   Never probe models with paid calls. On rejection, fall back once and update state.
5. If `HEART.md` is absent, explain that it is the live mission file and offer:
   - **Interactive setup** — ask one question at a time, then write the agreed HEART.
   - **Edit directly** — create the template, show its path, and pause.

```markdown
# Mission

# Current priorities

# Restrictions

# External effects allowed

# Stop conditions
```

Normal repository-local work is already authorized. HEART states the mission, restrictions, external permissions, and stop conditions.
6. Create or update the durable control plane.
7. Detect the preferred host scheduler:
   - macOS: `launchd` preferred; cron fallback;
   - Linux: user-level `systemd` timer preferred; cron fallback;
   - other Unix-like host: use an available durable machine-local scheduler or stop with exact instructions.
8. Generate a host-specific headless wrapper and scheduler configuration. The wrapper must set a deterministic environment, enter the repository, use the resolved real harness binary, enforce one-process locking, enforce a timeout shorter than the interval, invoke exactly one heartbeat, and append raw output to `runtime.log`.
9. Show every host-level file and scheduler change, the uninstall path, and any security caveat. Ask once for consent. After consent, install and enable as much as the current permissions allow. Do not keep asking for ordinary repository-local work.
10. Encode working hours structurally in the scheduler where possible, using the configured timezone and an off-peak minute. Always retain the `window.py` gate as defense in depth. The durable host scheduler becomes the sole scheduler and sets `self_schedule: false`.
11. Run the matching bare-environment authentication and PATH smoke test using the real binary. Then trigger one detached wrapper execution, verify its exit, lock behavior, raw log, curated log, state update, and active scheduler.
12. Report success only for checks actually observed. If any required check fails, leave the platform stopped, preserve diagnostics, and explain the blocker.
13. Print accepted settings and say: **“You can edit HEART.md live; the next heartbeat will pick up the change.”**

### `heartbeat`

The lead owns HEART interpretation, synthesis, state, and logging. Workers never install schedulers or arm wakeups.

1. Read state first. Run `scripts/window.py` with saved working hours. If outside them, append a terse skipped-state line and end without spawning agents.
2. Reconfirm repository root, billing source, sandbox, executable, and permission mode. Stop if cost may become metered or the boundary widened.
3. Audit runtime health cheaply: scheduler ownership, wrapper checksum/path, executable path, authentication, raw-log writability, and lock state. Repair repository-local drift. If a host repair needs consent, suspend and record it for interactive `status` or `resume`.
4. Read `HEART.md` fully, hash it, and load only relevant recent state. Discard stale plans that conflict with a changed HEART.
5. Check stop conditions, blockers, working-time remaining, and available fixed-plan allowance when exposed. Choose the smallest useful bounded work.
6. Route by cheapest sufficient tier. Keep the lead on general effort by default. Use strong reasoning for at most one clearly valuable deep step unless HEART explicitly justifies more. Dynamically reduce fan-out, effort, and scope as allowance tightens.
7. Delegate only when parallelism adds value. In token-managed mode, the lead owns the budget rather than maximizing concurrency. Disable recursive spawning unless HEART explicitly allows it.
8. Verify completed work. Near the window boundary, prefer checks, synthesis, state cleanup, or stopping early.
9. Write detailed operational memory under `.agent-platform/state/`, update `state.json`, and append one terse line to `LOG.md`.
10. Scheduling branch:
    - when `scheduler.self_schedule == false`, **do not schedule anything**; the durable host scheduler already owns the next wake;
    - when `scheduler.self_schedule == true`, arm exactly one temporary session wake and record it.
11. End the process. Never overlap heartbeats or leave unowned wakeups.

### `status`

Audit and report: running state, repository root, fixed-plan verification, sandbox, working hours, interval, token policy, model map, scheduler type and health, wrapper health, last heartbeat, HEART change status, current objective, blockers, and next host fire.

Self-heal repository-local runtime drift automatically. Before host-level repair, display the exact change and ask for consent. Never perform mission work.

### `stop`

Disable and remove only host scheduler entries recorded in state, terminate only platform-owned running processes, and clear safe stale locks. Preserve HEART, LOG, state, raw logs, and generated host configuration so `/agent-platform resume` can restore the platform. Report the uninstall result.

## Durable headless operation

Use a generated adapter rather than a machine-specific copied command. The adapter must account for differences between macOS and Linux:

- login shells, aliases, and functions do not exist under schedulers;
- `HOME` and `PATH` must be explicit and sufficient for the project toolchain;
- the real harness executable must be resolved and recorded;
- use `flock` when available or a portable atomic lock directory otherwise;
- use `timeout`, `gtimeout`, or a small portable watchdog, with a limit shorter than the heartbeat interval;
- scheduler stdout/stderr goes to `.agent-platform/runtime.log`, separate from `LOG.md`;
- schedule only configured working hours where possible and always gate again with `window.py`;
- prefer a stable off-`:00` minute to avoid synchronized load;
- durable host scheduling is the sole scheduler.

Session-local cron or wakeup tools do not survive the harness session and must not be trusted for unattended operation.

## Token economy and fixed-plan protection

- Treat the subscription allowance as a finite nightly budget, not free capacity to exhaust.
- Never enable extra usage or switch to metered authentication when the allowance is low.
- Use fast models for routine work, general models for the lead, and strong models only for rare high-value synthesis.
- Pin unattended lead model and effort explicitly so an interactive alias or high-effort default cannot leak into headless runs.
- Prefer medium or equivalent lead effort; escalate deliberately for the deep step only.
- Track quota, reset time, or remaining allowance when the harness exposes it. Do not invent hidden numbers.
- As allowance tightens: shorten work, reduce agents, lower effort, consolidate state, or sleep until reset.
- It is valid for a heartbeat to do nothing when no work is worth the tokens.
- Never spend calls merely to discover model availability.

## Log shape

One terse, state-first line per heartbeat:

```text
2026-07-23 22:38 CEST — Curr: simulation ready — built and sanity-tested machinery; no trades yet; next: paper run
```

Use a mission-relevant current-state label after `Curr:`. Include only the most important change, blocker, or next step. Detailed rationale and worker output belong under `.agent-platform/state/`.

## Harness notes

- Claude Code: read [`references/claude-code.md`](references/claude-code.md).
- Codex: read [`references/codex.md`](references/codex.md).

## Anti-patterns

- `while true`, shell `sleep`, or a model turn kept alive indefinitely.
- Claiming unattended operation before an end-to-end headless verification.
- Trusting session-only cron or wakeup tools for durable operation.
- Letting a heartbeat self-schedule while a host scheduler owns the clock.
- Starting without visibly reviewing settings and host changes.
- Defaulting working hours or heartbeat interval.
- Using API keys, extra usage, pay-as-you-go providers, or unverified billing.
- Falling back from a fixed plan to a metered provider.
- Autonomous mode without checking the repository boundary.
- Using blanket permission bypass when scoped headless permissions work.
- Calling a shell alias or function from the scheduler instead of the real binary.
- Letting interactive high-effort defaults leak into unattended runs.
- Writing harness settings files for headless permissions when command-line scoping is supported and safer.
- Omitting lock, timeout, deterministic environment, or raw logs.
- Asking permission for ordinary work inside the owned repository.
- Creating an empty HEART without explaining live control.
- Reading the entire growing history every heartbeat.
- Spawning agents merely to consume concurrency or allowance.
- Editing HEART, ignoring its changed hash, or continuing a stale plan.
- Starting work near the window boundary and spilling into protected time.
- Pushing, deploying, deleting outside the repository, spending money, or contacting people unless HEART explicitly authorizes it.
