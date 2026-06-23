---
name: yolo
description: Throwaway spike to prove (or kill) a feature's riskiest unknown before committing to building it for real. Use when the user types /yolo, or says "spike this", "quick prototype to see if X is even possible", "just hack something to prove the critical path", or wants learnings now so the feature can be spec'd properly later. Not for shipping work.
disable-model-invocation: true
argument-hint: "[what you're trying to find out — optional]"
---

# yolo

`/yolo` proves or kills a feature's riskiest unknown with a throwaway prototype — fast, but trustworthy enough to believe the result — so the learnings make the *real* version easy to spec. The spike is never meant to merge; the only thing that survives is `YOLO-LEARNINGS.md`.

Manual-only, on purpose: you opt into cutting corners for one spike.

## Flow

1. **Frame the one question.** Name the thing that, if it doesn't work, kills the direction — the riskiest unknown. That's all the spike answers. Write it at the top of `YOLO-LEARNINGS.md`.
2. **Branch.** Cut a throwaway `spike/<short-kebab>` branch — the convention for research with no merge intent. Pick the base — `main` or current branch — by what the spike builds on; ask the user if unsure. No PR, no merge intent.
3. **Spike it.** Skip everything that isn't the thing under test. Keep the path under test real. Journal as you go.
4. **Finalize.** Write the verdict + what the real spec must address, then stop. No auto-handoff, no cleanup — the user decides what's next.

## Fast but trustworthy

- **Skip freely:** security/auth, error handling, edge cases, tests, clean code, abstractions, polish, anything for states the spike won't hit. One ugly file is fine.
- **Keep real:** the integrations *on the path under test* (real API/DB/library), and enough error visibility (let it crash loudly) to believe what you see. Never mock away the thing the spike exists to learn.
- **Stay on target:** if what you're building doesn't answer the framed question, stop. No config systems, no second features, no "while I'm here" cleanup.

## The journal — `YOLO-LEARNINGS.md`

Lives at repo root. **Untracked but not `.gitignore`d** — survives branch switches and deletion, stays visible in `git status`. Never `git add -A`; commit spike code with explicit paths so the journal never lands in a throwaway commit.

```markdown
# Spike: <the one question>

## Log
- <tried> → <happened> → <surprise / dead-end / confirmation>

## For the real spec
- <constraint, gotcha, hard-vs-easy, open question>

## Verdict
<go / no-go / go-with-caveats> — <why>
```
