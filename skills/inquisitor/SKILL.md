---
name: inquisitor
description: Drive an adaptive interview — one question at a time — to pin down something the user wants to define, decide, or spec. Starts broad, lets each answer choose the next question (never a pre-written list), keeps going until everything is clear, then ends with a formatted summary the user approves or sends back. Uses the structured multiple-choice question widget when available. Use when the user types `/inquisitor`, or asks to "interview me", "ask me one question at a time", "help me figure out / flesh out / define / spec X", "pin down requirements", or says they have a vague idea they want made concrete. Be pushy — invoke whenever the user wants their own half-formed idea drawn out through questioning.
argument-hint: "[what you want to define — optional]"
---

# Inquisitor

Interrogate the user, gently, to turn a fuzzy idea into a crisp, agreed definition. You ask **one question at a time**, you **decide each question from the previous answer** rather than from a script, and you stop only when nothing is left vague, missing, or contradictory. You end with a clean summary the user approves or sends back.

The `[argument]` is the thing being defined (a feature, a concept, a plan, a policy, a name — anything). If it's missing, your first question is what they want to define.

## The loop

1. **Open broad.** One wide question that frames the whole thing.
2. **Ask one question.** Through the choice widget when you can (see below).
3. **Read the answer. Decide the _single_ next question from it.** Don't consult a pre-made list — there isn't one.
4. **Repeat** until the clarity test passes.
5. **Summarize** in a formatted block.
6. **Approval gate.** Approve → present + suggest a next step. Not yet → keep digging.

## One question at a time — non-negotiable

Exactly one question per turn. Never batch, never "a few quick questions", never a numbered list. One question, one answer, then think. Batching is the single most common way this skill gets ruined — it collapses the adaptivity that makes it worth doing.

A turn may carry a one-line bridge ("Got it — so it's web-only.") before the question, but only one actual question lands.

## Don't pre-plan. Let the answer choose the next question.

This is the whole point. **Don't draft a questionnaire in advance** — not even privately. Drafting ahead makes you ask generic questions that ignore what the user just told you. Instead, after each answer:

- Note what just got resolved, and what new ambiguity or branch the answer _opened_.
- Pick the **one question that removes the most uncertainty right now.** Usually that's the biggest open fork the last answer created.

Funnel from general to specific:

- **Early:** purpose, scope, the core of the thing, who it's for, what "done" looks like.
- **Middle:** the shape — structure, behavior, the main decisions and their alternatives.
- **Late:** edges, constraints, exceptions, format, naming, what's explicitly _out_.

Branch on answers. "It's for end users" and "it's an internal script" must lead to different next questions. If the next question is identical no matter the answer, it was too generic.

Skip anything you can reasonably infer, anything already answered, and anything that wouldn't change the outcome. Every question must earn its turn.

## Asking with the choice widget

Prefer the structured multiple-choice question widget (in Claude Code, the `AskUserQuestion` tool) — it's faster for the user than typing prose and forces you to commit to concrete options.

- **One question per call.** The widget can hold several; you use one. (The one-at-a-time rule again.)
- **2–4 concrete, mutually distinct options**, generated from the conversation so far — real candidate answers, not "Yes / No / Maybe". A short `header` chip names the dimension (e.g. "Scope", "Audience", "Format").
- The widget always offers an **"Other" free-text escape**, so it works even for semi-open questions — give your best concrete options and let the user override.
- Use **multi-select** when several options can genuinely co-apply.
- Drop to a **plain prose question** only when the answer space truly can't be enumerated (e.g. "what should it be called?"). Still one question.
- You may offer a sensible default, but don't railroad — this is elicitation, not persuasion.

If no widget exists in the current tool, ask in plain prose — same rules, still one at a time.

## When to stop

Stop when the **clarity test** passes: you could write the summary and every part is concrete, nothing important is undecided, and nothing the user said contradicts anything else.

- **Don't stop early** because you have "enough to start". Loose ends become wrong guesses.
- **Don't drag.** The moment it's clear, stop — padding with low-value questions is as bad as batching. If you catch yourself asking something whose answer wouldn't change the result, you're done.
- If two answers conflict, your next question resolves the conflict — don't summarize over it.

## The final summary

Present a formatted block. Group decisions under the themes that actually emerged — not a flat dump. Surface what was deliberately left open.

```
## ✓ <Thing> — definition

**In one line:** <the essence in a single sentence>

**<Theme that emerged, e.g. Scope>**
- <decision> — <the why or detail, if it matters>
- <decision>

**<Next theme, e.g. Behavior>**
- <decision>

**Left open / out of scope**
- <thing not decided, and why it's fine to leave it>

---
Approve this and I'll lock it in — or tell me what's off and I'll keep asking.
```

Keep it scannable: bold theme labels, tight bullets, no walls of prose. You may run the approval itself as a final choice-widget question (`Approve it` / `Not yet — here's what's off`) so corrections come back through "Other".

## After approval

1. Restate the locked definition cleanly — the approved summary is the deliverable.
2. **Suggest one concrete next step** that fits what was defined — e.g. "Want me to write this up as a spec file?", "Shall I start building it?", "Turn this into the README?".
3. **Stop and let the user react.** Don't act on the suggestion until they say so.

## Anti-patterns

- ❌ Asking several questions in one turn, or a numbered list "to save round-trips". Kills adaptivity.
- ❌ Privately drafting the full question set up front, then reading it out. The next question must come from the last answer.
- ❌ Generic questions whose follow-up is the same no matter the answer.
- ❌ Widget options like "Yes / No / It depends" — give real, specific candidates.
- ❌ Stopping at "good enough to start" with loose ends, or padding with questions after it's already clear.
- ❌ Summarizing over a contradiction instead of resolving it with the next question.
- ❌ On approval, charging ahead into building/saving without letting the user react to the suggestion.
