---
name: are-we-there-yet
description: Final sweep for loose threads before the user closes the session, so they can walk away and never think about it again. Use when the user types /are-we-there-yet, or says "are we done", "can I close this", "anything left?", "did I miss anything", "wrapping up", "before I go", or otherwise signals they are about to end the session.
---

# are-we-there-yet

The user wants to close this session and never think about it again. Find whatever stands in the way, and stay on it until nothing does.

**The test: once this conversation is gone, is anything left half-done, or is there anything the user must do or remember that lives only in the chat?**

## Look

Go back over the whole conversation, not just the last few turns. What slips is what got buried: an instruction to the user in the middle of a long reply, a question nobody answered, a "we'll do that later" that never happened. Then check the real state of whatever the session touched rather than trusting memory: uncommitted work, something still running, anything left in a temporary state.

Those are examples, not a checklist. Think about what this particular session could have left behind.

## Report

Open with one of these verdict banners, copied verbatim in a code block:

```
    ___                       |> NOT YET
  _/_|_\_                     |
 '-O---O-' . . . . . . . . .  |
```

```
                        ___   |> WE'RE THERE
                      _/_|_\_ |  safe to close
 . . . . . . . . . . '-O---O-'|
```

After NOT YET, a numbered list, one item per thing to do, one line each, so the user can answer by number: the shortest context that makes it make sense, then the action. Nothing outside the list; if it isn't an action, drop it. Offer to handle what the agent can; don't do it unasked.

If nothing is open, the WE'RE THERE banner is the whole answer.

## Stay on until clear

NOT YET keeps this skill active. End every following reply with the banner and the list, re-checked against the real state: drop what got done, add anything the new work left open. Stop only after showing WE'RE THERE, or when the user calls it off.

## Anti-patterns

- Inventing loose ends to look thorough. Ideas and nice-to-haves nobody committed to aren't loose threads.
- Flagging deferred work that's already recorded somewhere (issue, TODO, notes). Flag it only if it would be lost with the chat.
- Recapping the session.
