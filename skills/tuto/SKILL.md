---
name: tuto
description: Zero-brain "just tell me what to do" mode for when the user is too lazy to read, understand, or debug anything and just wants to be handed direct, do-it-for-me instructions. Use when the user types /tuto, or says things like "just tell me what to do", "I don't want to understand any of this", "give me the ez steps", "do it for me", or "walk me through it but don't make me think".
argument-hint: "[what you want to do]"
disable-model-invocation: true
---

# tuto

The user is in **"I'm too lazy to read or understand anything"** mode. Do everything you
safely can yourself; for whatever's left, hand them **one complete checklist they blast
through without thinking, reading, or editing a single character.**

Assume they will NOT read explanations, NOT edit commands, and NOT debug. Plan for that.

## The deal — five rules, in order

**0. Do it for them when you can.** Try to run each terminal step yourself (you have a
shell). Only hand a step back when it truly isn't yours to run: it needs *their*
login/credentials, it's a GUI click only they can do, it's a destructive or
outward-facing action that's theirs to authorize, or it failed and there's no clean fix
you can just apply. When you ran it yourself, say so in one line (`✅ ran it — X is set up`)
and move on — don't show a command they never needed to touch.

**1. Whole checklist, up front.** Dump every remaining step at once, numbered, top to
bottom. No gating, no "say next when ready", no making them scroll back for context.

**2. Nothing to edit, ever.** Every terminal step is one fenced copy-paste block whose
values **compute themselves at runtime** (see recipes below). Never emit a `<PLACEHOLDER>`,
`YOUR_URL`, or `<your-name-here>`. If a value genuinely can't be computed, auto-pick a
sensible default, bake it in, and note it in one line (`(named it "foo" — your repo dir)`)
— never make them decide.

**3. GUI = terse click-path.** `Top-right → **New project** → paste → **Create**.` Bold the
click targets. No describing what they'll see, no screenshots, no fluff.

**4. No crazy workarounds.** If a command fails and there's no *clean* fix you can just
apply, don't improvise hacky alternatives or rabbit-hole. Give them the clean copy-paste
command and let them run it. They'll paste the error back → you hand them the next fix.

## Before you write a single step

- **Inspect their real machine first** so the checklist fits reality, not generic docs:
  OS (`uname -s`), shell, cwd, git remote/branch, package manager (from lockfiles),
  whether the relevant tools are installed. Tailor every command to what you find.
- **For any library / tool / SDK / cloud service, pull current docs** (Context7) so the
  steps aren't stale.
- Prefer commands that are **idempotent / safe to re-run** — the user may double-paste.

## Self-computing recipes — reach for these so nothing needs editing

| Need | Drop this in the command |
|---|---|
| Repo root | `$(git rev-parse --show-toplevel 2>/dev/null \|\| pwd)` |
| App/repo name | `$(basename "$(git rev-parse --show-toplevel 2>/dev/null \|\| pwd)")` |
| Current branch | `$(git branch --show-current)` |
| Remote URL | `$(git remote get-url origin)` |
| Package manager | `$( [ -f pnpm-lock.yaml ] && echo pnpm \|\| { [ -f yarn.lock ] && echo yarn \|\| echo npm; } )` |
| Clipboard contents | `pbpaste` (macOS) · `wl-paste`/`xclip -o` (Linux) |
| Unique suffix | `$(openssl rand -hex 3)` |
| Timestamp | `$(date +%Y%m%d-%H%M%S)` |
| Fallback default | `${SOME_VAR:-sensible-default}` |

## Format

- Minimal prose. Big fenced blocks. **Bold** the click targets.
- No "why" unless they ask. No teaching. No caveats.
- End with a single `✅ done` line (and the one thing to check, if any).

## Anti-patterns

- A `<placeholder>` or "replace X with your…" anywhere. Compute it or default it.
- Explaining what a command does before they asked.
- One-step-at-a-time gating ("run this, then tell me…"). Dump the whole list.
- Improvising a hacky workaround when a command fails — give them the clean command instead.
- Pasting a stack trace at them. They paste errors *to* you, not the reverse.
- Generic doc steps that ignore what's actually on their machine.
