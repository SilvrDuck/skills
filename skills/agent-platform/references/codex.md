# Codex implementation notes

Use this reference only when the harness is Codex. Inspect the installed version, effective configuration, model catalog, authentication, and billing source rather than assuming every client exposes the same capabilities.

## Fixed-plan requirement

Unattended operation must remain inside the user's fixed Codex or ChatGPT subscription allowance.

- Verify the active authentication and plan before starting.
- Reject API keys, pay-as-you-go projects, credit balances, extra usage, or provider fallbacks that can create a separate bill.
- If fixed-plan billing cannot be established for the lead and every subagent model, stop.
- Never solve quota exhaustion by switching to metered credentials.

## Skills and headless launch

Codex can load this repository's Agent Skill normally. Interactive `/agent-platform start` or `/agent-platform resume` displays the settings gate first.

For each unattended heartbeat, use a finite non-interactive invocation rooted explicitly in the repository, for example:

```bash
codex exec \
  --cd "$REPO_ROOT" \
  --sandbox workspace-write \
  --ask-for-approval never \
  "agent-platform heartbeat"
```

Use `codex exec`, not a permanently open TUI turn. Do not use `--yolo`, `--dangerously-bypass-approvals-and-sandbox`, `danger-full-access`, `--add-dir`, or extra writable roots.

Before accepting this setup, inspect effective config and verify the equivalent of:

```toml
sandbox_mode = "workspace-write"
approval_policy = "never"
```

Project-scoped configuration loads only for trusted projects. Confirm trust and inspect user, profile, project, and managed layers for overrides. Network access is separate from filesystem access; leave it disabled unless HEART requires it.

## Settings interaction

Use Codex's structured user-input or multiple-choice UI when exposed. Otherwise render the same compact settings table and ask for numbered selections. Never skip settings review because a widget is unavailable.

A scheduled `heartbeat` is non-interactive and reads accepted values from `.agent-platform/state.json`.

## Durable scheduling

Codex CLI and interactive sessions are execution harnesses, not durable clocks. Install the same host-level architecture used by the generic skill:

- macOS: LaunchAgent preferred, cron fallback;
- Linux: systemd user timer preferred, cron fallback;
- generated repository-local wrapper with deterministic `HOME` and `PATH`;
- resolved real `codex` binary, never an alias or function;
- non-overlapping lock and watchdog shorter than the interval;
- raw stdout/stderr in `.agent-platform/runtime.log`;
- working hours encoded structurally where possible and rechecked by `window.py`.

Show exact host changes and ask once for consent before installation. Store installed identifiers in state and a copy of configuration under `.agent-platform/host/`. The host scheduler is the sole scheduler, so set `scheduler.self_schedule` to `false`.

Do not assume ChatGPT Scheduled Tasks can reopen a local Codex repository. They are a separate surface. Do not trust a live Codex session to survive terminal or SSH closure.

## Bare-environment verification

Before reporting success:

1. Run the resolved `codex` binary under `env -i` with explicit `HOME` and minimal sufficient `PATH`.
2. Execute a tiny fixed-plan headless prompt and require the expected exact output and exit code `0`.
3. Confirm no API key or metered project supplied authentication.
4. Run the generated wrapper detached.
5. Verify runtime logs, state update, curated log, lock behavior, and active host scheduler.

Do not declare unattended operation working based only on generated files.

## Models, allowance, and subagents

Inspect the fixed-plan model catalog and effective configuration. Route by capability rather than hard-coding generations:

- **fast:** cheap polling, extraction, mechanical work, and log synthesis;
- **general:** heartbeat lead, normal implementation, and investigation;
- **strong:** rare deep synthesis, difficult diagnosis, or adversarial review.

Codex multi-agent controls may include:

- `agents.enabled`
- `agents.default_subagent_model`
- `agents.default_subagent_reasoning_effort`
- `agents.max_concurrent_threads_per_session`
- custom `agents.<name>` role declarations

Map available fixed-plan models to the platform classes. A numeric cap must remain within Codex's configured maximum. In `token-managed, no fixed cap` mode, the lead still manages the subscription allowance parsimoniously; it does not maximize threads.

Pin the unattended lead model and moderate reasoning effort explicitly when the installed CLI supports it. Do not inherit an interactive high-effort profile accidentally. When allowance information is exposed, reduce fan-out, effort, and scope as the reset approaches. It is valid to do no work when progress is not worth the remaining allowance.

The lead remains responsible for HEART interpretation, final synthesis, state, logging, and scheduler ownership. Workers must not install schedulers, widen the workspace, change billing, or recursively fan out unless HEART explicitly permits it.

## Runtime self-healing

On `start`, `resume`, and `status`, detect stale executable paths, wrapper drift, stopped timers, bad environment, broken fixed-plan authentication, and abandoned locks. Repair repository-local state automatically. Present host-level changes and ask for consent before applying them. Never self-heal by widening the sandbox or enabling metered billing.
