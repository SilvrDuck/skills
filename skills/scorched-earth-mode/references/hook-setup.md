# Hook channel (Claude Code and other SessionStart-hook harnesses)

When the harness supports a session-start hook, this is the channel for persisting the
mode. The hook **guarantees** the declaration reaches every future session — the harness
injects it, so it never depends on the agent choosing to read a file — and `CLAUDE.md`
stays clean. Two pieces: a marker file (the state) and a hook (the delivery).

## Marker file = the state

`.claude/scorched-earth.md` holds the canonical declaration (the block shown in
`SKILL.md`). Its **presence** is the on/off switch; its **contents** are what gets
injected. Enabling writes it; disabling (`/scorched-earth-mode off`) deletes it. It's
git-tracked, so the mode stays reviewable in diffs.

## Hook = the delivery

Add this `SessionStart` hook to the project's `.claude/settings.json`. On every session
start it injects the marker's contents when the file exists, and does nothing when it
doesn't (so the hook is harmless to leave installed while the mode is off):

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "test -f \"$CLAUDE_PROJECT_DIR/.claude/scorched-earth.md\" && jq -Rs '{hookSpecificOutput:{hookEventName:\"SessionStart\",additionalContext:.}}' \"$CLAUDE_PROJECT_DIR/.claude/scorched-earth.md\" || true"
          }
        ]
      }
    ]
  }
}
```

Verified against the Claude Code hooks reference (<https://code.claude.com/docs/en/hooks>):

- The nesting is real — `SessionStart` is an array of groups, each with its own `hooks` array. Don't flatten it.
- A command hook injects context only by printing `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "…"}}` to stdout on exit 0. Plain stdout text is **not** added. `jq -Rs` slurps the marker file into the `additionalContext` string.
- `$CLAUDE_PROJECT_DIR` is exported to the command; use it rather than a relative path, since the hook's working directory isn't guaranteed to be the project root.
- Requires `jq` on PATH.
- No `matcher` → fires on all sources (startup, resume, clear, compact), which is what we want.

## Idempotency — when turning the mode on

1. Read `.claude/settings.json` (create `{}` if absent).
2. If a `SessionStart` hook already references `scorched-earth.md`, **don't add a second one** — just (re)write the marker file.
3. Otherwise merge the group above into the existing `hooks.SessionStart` array — append, don't overwrite other hooks.
4. Write the marker file with the canonical declaration.

## Turning the mode off

Delete `.claude/scorched-earth.md`. Leave the hook in place — with the marker gone it
injects nothing. (Only strip the hook from `settings.json` if the user asks to remove the
machinery entirely.)
