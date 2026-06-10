# Hook channel (Claude Code and other harnesses with session-start hooks + local settings)

When the harness supports a session-start hook **and** a per-developer local settings file,
this is the channel for persisting the mode. The hook **guarantees** the declaration reaches
every future session — the harness injects it, so it never depends on the agent choosing to
read a file — and because it lives in local settings, nothing leaks into git or teammates'
sessions.

## Where the state lives

`.claude/settings.local.json` is personal and git-ignored (Claude Code adds it to
`.gitignore` automatically). The hook entry's **presence** is the on/off switch; the
declaration is inlined in the hook command, so there's no separate marker file and no `jq`
dependency. Enabling adds the entry; disabling (`/scorched-earth-mode off`) removes it.

## The hook

Add this `SessionStart` hook group to `.claude/settings.local.json`. On every session start
it prints the declaration as `additionalContext`:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "printf '%s\\n' '{\"hookSpecificOutput\":{\"hookEventName\":\"SessionStart\",\"additionalContext\":\"## Scorched-earth mode: ON\\nScorched-earth mode activated — you must always read the `scorched-earth-mode` skill first.\"}}'"
          }
        ]
      }
    ]
  }
}
```

Verified against the Claude Code hooks reference (<https://code.claude.com/docs/en/hooks>):

- The nesting is real — `SessionStart` is an array of groups, each with its own `hooks` array. Don't flatten it.
- A command hook injects context only by printing `{"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": "…"}}` to stdout on exit 0. Plain stdout text is **not** added.
- `printf '%s\n'` (not `echo`) emits the literal `\n` inside the JSON string as an escaped newline; the JSON parser then turns it into a real newline in `additionalContext`. Using `echo` with an unescaped newline produces a raw control character and the payload fails to parse.
- No `matcher` → fires on all sources (startup, resume, clear, compact), which is what we want.
- No external dependency — `printf` is a shell builtin.

## Idempotency — when turning the mode on

1. Read `.claude/settings.local.json` (create `{}` if absent).
2. If a `SessionStart` hook already prints the scorched-earth declaration, **don't add a second one** — announce it's already on and exit.
3. Otherwise merge the group above into the existing `hooks.SessionStart` array — append, don't overwrite other hooks.

## Turning the mode off

Remove the scorched-earth hook group from `.claude/settings.local.json`, leaving every other
hook in place. If the resulting `hooks.SessionStart` array is empty, drop it. The declaration
stops being injected from the next session on.
