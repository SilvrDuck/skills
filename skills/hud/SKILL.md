---
name: hud
description: Spin up a shared live web HUD on localhost for the current discussion — a small HTML control panel where every user click and keystroke is instantly appended to an events file the agent watches, and the agent reshapes the UI live by editing files (the page hot-swaps without reload). Proposes a few UI modalities as a multiple-choice question first, then builds and serves from /tmp. Use when the user types /hud or asks for a quick UI, control panel, dashboard, or a visual way to work together on the discussion.
argument-hint: "[what the UI should help with — optional]"
disable-model-invocation: true
---

# hud

Build a live, two-way visual workspace for the current conversation: the user steers through a local web page, the agent steers through files. The plumbing is fixed and shipped with this skill — **never rewrite it**. The agent's job is only to design `ui.html` and `state.json` for this discussion.

## How the pieces talk

| File (in workspace dir) | Owner | Purpose |
|---|---|---|
| `ui.html` | agent | UI fragment, hot-swapped into the page within ~250ms of any edit — no reload |
| `state.json` | agent | data the UI renders; cheaper to update than rewriting `ui.html` |
| `events.jsonl` | server | append-only log of every user action, written the instant it happens |

`assets/server.py` serves the page and logs events; `assets/index.html` is the browser shell that polls for changes. Run them as-is.

## Flow

1. **Frame the problem.** From the conversation, decide what visual surface would actually help. Then propose 2–4 concrete modalities via the harness's multiple-choice question tool (with small preview mockups if supported). Examples: triage/checklist board, parameter panel (sliders/toggles), ranking or voting on options, editable table, A/B compare with pick buttons, annotatable document, status dashboard.
2. **Set up the workspace** at `/tmp/claude/hud/<slug>` (fall back to a dir inside the project if not writable). Write an initial `ui.html` and `state.json`.
3. **Start the server in the background**: `python3 <this-skill-dir>/assets/server.py --dir <workspace>`. It picks a free port and writes `<workspace>/server.json`; read it and give the user the URL (`http://localhost:<port>`).
4. **Start the watcher in the background**: `python3 <this-skill-dir>/scripts/watch-events.py <workspace>`. It blocks until the user does something, prints the new event lines, and exits — that's the ping to react.
5. **React loop.** When the watcher returns events: read them, respond in chat and/or mutate `ui.html` / `state.json` (the page updates live), then **restart the watcher**. Keep exactly one watcher running. Keep the server running for the whole session.

## Writing ui.html fragments

`ui.html` is a body fragment (no `<html>`/`<head>`), injected into the shell's mount; its `<script>` tags re-run on every swap. The shell provides a dark theme with styled buttons/inputs/tables/`.card`, plus:

- **Auto-captured actions** — no wiring needed: any element with `data-action="name"` logs a click event (extra `data-*` attributes are included); any input/select/textarea with a `name` logs its value as it changes. Use `hud.send(type, {...})` for anything custom.
- **`hud.state`** — the parsed `state.json`. Re-render on `window.addEventListener('hud:state', e => ...)`. The swap itself re-runs scripts, so render from `hud.state` at script top level too.
- Form values and focus survive swaps, matched by `name` (opt out with `data-no-restore`).
- `state.title` sets the page header.

One fragment sketch:

```html
<div class="card">
  <h2>Pick the winner</h2>
  <div id="opts"></div>
  <textarea name="notes" placeholder="why?"></textarea>
</div>
<script>
  function render() {
    document.getElementById('opts').innerHTML = (hud.state.options || [])
      .map(o => `<button data-action="pick" data-id="${o.id}">${o.label}</button>`).join(' ');
  }
  window.addEventListener('hud:state', render);
  render();
</script>
```

## Rules

- Prefer `state.json` edits for data-only changes; edit `ui.html` only for structural changes.
- Never write to `events.jsonl` or `.events.cursor` — read only.
- Narrate meaningful reactions in chat ("saw you rejected #3 — removed it"), so the conversation and the HUD stay one discussion.
- On `TIMEOUT` from the watcher, ask the user whether to keep the HUD open; restart the watcher if yes.
- If the sandbox blocks binding a port, rerun the server command with sandbox disabled or ask the user to allow it.
