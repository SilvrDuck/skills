---
name: keep-me-in-the-loop
description: One-screen catch-up brief on the current session's work, so the user can re-engage as the engineer in command after drifting. Use when the user types /keep-me-in-the-loop, or says "catch me up", "where are we", "what are we doing", "I zoned out", "I lost track", "brief me", or wants to lock back in.
argument-hint: "[focus area — optional]"
disable-model-invocation: true
---

# keep-me-in-the-loop

The user stopped following while the agent worked and now wants to lock back in. Hand them one screen that puts them back in command: what we're doing and why, the parts and how they fit, and what needs their judgment. Then resume normal replies. This is one brief, not a mode.

**One terminal screen, max (~25 lines). Bottom line first.** Not a lecture. The user asks for detail when they want it, so never pre-empt them.

## Which brief

| Situation | Brief |
|---|---|
| First call this session | Full brief |
| Repeat call, no argument | Delta: only what changed since the last brief. Full brief if the last one is no longer in context. |
| Called with a focus (`/keep-me-in-the-loop the queue`) | Full brief narrowed to that area |
| No substantive work yet | One line saying there's nothing to brief yet |

## Before writing

Build from the conversation, then run a quick check so every status claim is true:

- `git status` and `git diff --stat`: what actually changed on disk.
- Open a key file only when a claim hinges on it ("wired up", "handles X").
- Call something tested only if a test run in this session passed. Otherwise it is untested.

Keep the check fast. Don't re-read every touched file.

## Format

Fixed order. Leave out any section with nothing real to say. Never write "none".

- **BLUF**: the goal and why, in 1–2 lines.
- **Parts**: the files or components involved, one line each on their role, plus how they interact as an arrow chain.
- **Context**: technical facts the user wouldn't already know, such as library quirks or external constraints.
- **Decided**: choices already made, each with the alternative it ruled out.
- **Your call**: open questions the agent shouldn't settle alone, with the agent's default if it has one.
- **Risk**: anything fragile, unverified, or likely to cause trouble later.
- **Now**: state (done / in progress / untested) → next step.

```
**BLUF:** Adding retry to the webhook sender so Stripe events stop
getting dropped on 502s.

**Parts**
- `sender.py`: posts events, now wraps each send in retry
- `queue.py`: holds failed events between tries
- sender → queue on failure → `worker.py` re-sends

**Context**
- Stripe rate-limits bursts, so retries have to back off

**Decided**
- Exponential backoff rather than fixed interval, because of the rate limit

**Your call**
- Max retries: 5 (current default) or match Stripe's 3-day window?

**Risk**
- Retry path untested against the real Stripe sandbox

**Now:** sender done, queue half-done → finish queue, then sandbox test
```

A delta opens with `**Since last brief:**` followed by one line, then only the sections that changed.

## Voice

- The reader is a competent engineer. Explain only what someone who wasn't watching couldn't guess.
- Use fragments over sentences and one line per bullet. Name concrete things: files, functions, numbers.
- No preamble, no praise, no restating the request, no stacked hedges, no closing offer of more detail.
- Show interactions as arrow chains, not diagrams.

## Anti-patterns

- Spilling past one screen. Cut the least load-bearing bullets first.
- Retelling the session in order ("first we…, then we…") instead of stating where things stand now.
- Claiming "done" or "works" without the quick check.
- Explaining basics the user already knows.
- Staying in brief format for replies after the brief.
