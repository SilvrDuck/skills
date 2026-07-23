# Codex implementation notes

Use this reference only when the harness is Codex. Inspect the installed version and effective configuration rather than assuming every client exposes the same UI.

## Skills and launch

Codex can load this repository's Agent Skill normally. Interactive `/agent-platform start` or `/agent-platform resume` should display the settings gate before doing work.

For unattended heartbeats, use a finite non-interactive Codex invocation rooted explicitly in the repository, for example:

```bash
codex exec \
  --cd "$REPO_ROOT" \
  --sandbox workspace-write \
  --ask-for-approval never \
  "agent-platform heartbeat"
```

Use `codex exec`, not a permanently open TUI turn. Do not use `--yolo`, `--dangerously-bypass-approvals-and-sandbox`, `danger-full-access`, `--add-dir`, or extra writable roots.

Before accepting this setup, inspect the effective config and verify:

```toml
sandbox_mode = "workspace-write"
approval_policy = "never"
```

Project-scoped Codex configuration is loaded only for trusted projects. Confirm the project is trusted, and check user, profile, project, and managed config layers for overrides. Network access is separate from filesystem access; leave it disabled unless the mission genuinely requires it.

## Settings interaction

Use Codex's structured user-input or multiple-choice UI when the current client exposes it. Otherwise render the same settings as a compact table and ask the user to select numbered options. Never skip the settings review merely because the client lacks a widget.

A scheduled `heartbeat` is non-interactive and reads the already accepted values from `.agent-platform/state.json`.

## Models and subagents

Inspect the current model catalog and effective configuration. Route by capability rather than hard-coding model generations.

Codex supports multi-agent roles and exposes controls such as:

- `agents.enabled`
- `agents.default_subagent_model`
- `agents.default_subagent_reasoning_effort`
- `agents.max_concurrent_threads_per_session`
- custom `agents.<name>` role declarations

Map those settings to the skill's fast, general, and strong classes. Keep the platform's concurrency cap at or below Codex's configured maximum. The lead remains responsible for HEART interpretation, final synthesis, logging, and scheduling.

## Scheduling

Codex CLI and interactive Codex sessions are execution harnesses, not durable clocks. Arrange each wake through an external scheduler such as systemd, launchd, cron, a container supervisor, or another machine-local task runner that invokes `codex exec` from the repository.

Do not assume ChatGPT Scheduled Tasks can reopen a local Codex repository: Scheduled Tasks are a separate ChatGPT surface and are not available inside Codex. The external scheduler must preserve the repository path and invoke exactly one heartbeat at a time.

Store only the scheduler identifiers created for this platform in state. Each heartbeat should replace or chain a single next wake; prevent overlapping processes with the scheduler or a repository-local lock.
