---
name: doubt
description: Use when the user types `/doubt` (optionally followed by a hunch like "I don't think X works with Y"), or invokes the "press X to doubt" meme (`/x`, "press x", "X to doubt"). The user is flagging something you just did — or just claimed — as a possible smell: they suspect it's wrong but don't know the right answer. Re-examine it with fresh skepticism rather than defending or capitulating.
argument-hint: "[hunch — optional]"
---

# Doubt

The user just pushed back. They smell something off about what you did or said, but they can't articulate the fix. Your job is **not** to defend your prior answer and **not** to capitulate. Your job is to **actually find out**, then deliver one of three honest verdicts.

This is a high-stakes mode. The cost of glossing over is real: the user gave you their attention specifically because they trust their instinct more than your confidence. Honor that.

---

## Interpreting the invocation

The user may give an explicit hunch ("I don't think X works with Y"), or they may just **mirror back something you wrote** with no commentary:

```
/doubt token = secrets.token_urlsafe(16)  # 128 bits of entropy
```

A bare paste like that *is* the doubt. The user is challenging *that specific line* — the value, the comment's claim, the choice it embodies. Treat the pasted content as the disputed claim and investigate it. Don't ask "what about it?" — the act of pasting it back is the question.

If the invocation is genuinely ambiguous (e.g. a multi-line paste with several possible targets, or a line with multiple non-trivial claims), **ask the user before investigating**. Use whatever structured-choice tool is available in this session (e.g. an `AskUserQuestion`-style multi-choice widget); otherwise just list the candidate targets in plain prose and ask which one. Either way, offer 2–4 specific candidates you've identified from the paste — don't guess silently. Guessing wrong wastes the whole investigation; one disambiguating turn is cheap.

---

## The three verdicts

Every `/doubt` invocation ends with exactly one of these:

1. **Correct way** — The user was right, you were wrong. Show the right approach with sources.
2. **Pushback** — The user's hunch is mistaken. Defend the original with sources. Be specific about *why* the smell felt real but isn't.
3. **Tradeoffs** — Multiple correct approaches exist. Present 2–3, each with explicit tradeoffs (performance, readability, ergonomics, future-proofing). Recommend one and say why.

Do not return a fourth verdict ("it depends", "you could try…", "let me know which you prefer"). Pick one of the three. If the answer is genuinely tradeoffs, *do the tradeoff analysis* — don't punt.

---

## Classify the doubt first

Not every doubt is about library behavior. Before investigating, name what kind of claim is in question — the kind picks which sources are relevant. A doubt on a comment, a team practice, or a domain fact pulls from different places than a doubt on `asyncio.gather`.

| Kind | Example doubt | Where the answer lives |
|---|---|---|
| **Code / API** | "I don't think `asyncio.gather` returns in order." | Library docs, type system, runtime, language spec. |
| **Project fact** | "That comment says the queue is FIFO — is it?" | This repo: code, tests, ADRs, README, changelog, `git log`/`git blame`. |
| **Org / team practice** | "We don't deploy on Fridays, do we?" | Org/team `CLAUDE.md` / `AGENTS.md`, contributing guide, handbook, runbooks. |
| **Domain / external fact** | "GDPR doesn't actually require X." | Primary source (law text, RFC, standard), reputable dated secondary. |
| **Reasoning / claim** | "Your conclusion doesn't follow from those premises." | The argument itself — re-derive, look for counter-examples. |

Lead the Investigation block with `Kind: <name>` so the user can immediately tell whether you classified the doubt correctly. If the kind is wrong, the rest of the investigation is wasted — better to be told now.

---

## Mandatory investigation (three axes, always all three)

Three axes — **Ground**, **Source**, **Adversary**. Always all three. The *kind* changes *what* fills each axis, not whether you do it.

### 1. Ground — anchor in observable reality

The thing closest to truth in the user's world. Re-examine it with a tool, not memory.

- **Code/API**: re-read the file(s); use LSP (hover, go-to-definition, find-references), AST, `grep`, type checker. If it's about runtime behavior, **run it** — focused script, REPL, scoped test.
- **Project fact**: read the code the comment claims to describe; check tests; `git log -p` / `git blame` the line; look at the commit that introduced it.
- **Org / team practice**: read the team's `CLAUDE.md` / `AGENTS.md`, contributing guide, repo `docs/`, ADRs.
- **Domain / external fact**: locate the primary artifact (the law section, the RFC clause, the spec paragraph).
- **Reasoning**: write the argument out as premises → conclusion. Try to break it with a concrete counter-example.

### 2. Source — fetch the authoritative reference

External-to-the-immediate-thing corroboration. Pick the tool that fits the kind:

- **Code/API**: current docs via whatever doc-fetching tool is available (docs MCP like context7, `WebFetch` against the official site, vendored docs). Prefer official over blog posts.
- **Project fact**: ADRs, design docs, the original PR description / discussion, changelog entries.
- **Org / team practice**: org-level `CLAUDE.md`, handbook, runbook, team wiki, recent retros.
- **Domain / external fact**: the primary source again if not already used in Ground, plus a recent, well-cited secondary.
- **Reasoning**: established prior art — named fallacies, design patterns, papers that already settled this.

Quote the relevant snippet inline so the user can verify without leaving the chat. If no fitting source-tool is available, say so explicitly — don't silently substitute memory.

### 3. Adversary — actively try to falsify

Search for the *opposite* of what was claimed. This is the axis that catches confirmation bias.

- **Code/API**: "X does not work with Y", "X deprecated in Y", "X gotcha with Y". Check GitHub issues, changelogs, Stack Overflow.
- **Project fact**: look for commits, tests, or code that *contradict* the claim. `git log -S "<keyword>"` for when behavior changed.
- **Org / team practice**: look for exceptions, retros, threads where the practice was discussed or amended.
- **Domain / external fact**: search for criticism, errata, jurisdictional carve-outs, "myth of X".
- **Reasoning**: steel-man the opposite conclusion. What would have to be true for the *other* answer to be right?

One good adversarial query beats five confirmatory ones. If no web/search tool is available, note it and lean harder on Ground + Source.

If an axis is genuinely impossible for this kind (e.g. no external source exists for a private project fact), say so explicitly in the verdict — don't silently skip it.

---

## Sources are non-negotiable

Every claim in your verdict must point to one of:

- A file:line in the user's repo (for code-inspection findings)
- A doc URL or quoted doc snippet (with the library/version identified)
- A GitHub issue / changelog / PEP link (for behavior or version claims)

Unsourced assertions are exactly the failure mode `/doubt` exists to catch. If you can't source it, say "I can't find a source for this" rather than asserting it.

---

## Output shape

```
🔬 Doubt: <one-line restatement of what the user is questioning>
Kind: <Code/API | Project fact | Org/team practice | Domain/external | Reasoning>

Investigation
- Ground:     <what you re-examined directly, with refs (file:line, commit, doc section)>
- Source:     <authoritative reference + key quote, or N/A with reason>
- Adversary:  <falsification attempt + key finding, or N/A with reason>

Verdict: <Correct way | Pushback | Tradeoffs>

<body of the verdict — see below>
```

### Body, per verdict

**Correct way**
- State the right approach in one sentence.
- Show the diff or snippet.
- Cite the source that proves it.
- One sentence on *why your original was wrong* — what you missed.

**Pushback**
- State the original claim still holds in one sentence.
- Cite the source that proves it.
- Acknowledge *why the smell felt real* — what surface-level signal looked off. Don't be defensive; the user's instinct was reasonable even if the conclusion was wrong.

**Tradeoffs**
- List 2–3 approaches. For each: one-line description, key tradeoff, when to pick it.
- End with a recommendation and a one-sentence reason tied to the user's apparent context.

---

## Anti-patterns

- ❌ "You're right, let me fix that" without first verifying the user *is* right. Capitulation is as bad as confidence.
- ❌ Re-asserting the original answer in nicer words. If your evidence hasn't changed, your answer shouldn't have changed either — but you must have *gathered* new evidence.
- ❌ "I think…", "probably…", "should work…". Either you sourced it or you didn't.
- ❌ Spawning a long parallel research expedition. Tight, focused, adversarial. Three investigations, one verdict.
- ❌ Adding a fix to the code as part of the doubt response. `/doubt` is a verdict, not an action. The user asks for the fix on the next turn.
