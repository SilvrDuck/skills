---
name: defossil
description: Strip conversation-shaped fossils — text that only exists in the artifact because of how it was iteratively produced, not because the artifact needs it. Targets "# tight message" labels, README paragraphs announcing internal scaffolding the user asked for, defensive reassurances answering user worries, "now uses X instead of Y" comments, "Changes:" docstring sections, names like `test_validation_added`, and TODOs that point at "what we discussed". Use when the user types `/defossil`, asks to scrub/launder/depersonalize an artifact, or says "make this look like it wasn't iterated on". ALSO auto-invoke before reviewing your own recent work, before writing or editing a README / docstring / code comment / commit message / PR description, and before claiming a task complete — apply the litmus test in this skill before any of those, even if the user didn't ask. Be pushy: when in doubt about whether a comment or doc paragraph you're about to write is fossil-shaped, invoke this skill instead of guessing.
---

# Defossil

The conversation that produced an artifact leaves marks: labels naming transformations the user asked for, paragraphs announcing scaffolding the user requested, defensive reassurances answering the user's worries, "now uses X" framing that only makes sense if you remember the old X. These are **fossils** — preserved traces of a past event (the chat) that don't belong in the present artifact.

This skill is **not** generic over-commenting cleanup ("# loop through items"). That's a different problem. Defossil targets a sharper category: text whose presence is explained by the *prompt history*, not by the *product*.

---

## The litmus test

For every candidate, ask:

> **If a stranger had been handed the final spec and produced this artifact in one shot, would this text be here?**

- **No** → fossil, remove.
- **Yes** → keep.
- **Maybe** → borderline, flag for the user, don't auto-remove.

That single question replaces a hundred heuristics. Apply it line by line.

---

## Taxonomy of fossils

Each row is a pattern to scan for, with the diagnostic that distinguishes fossil from legitimate content.

| Pattern | Fossil tell | Example |
|---|---|---|
| **Transformation label** | Names the *operation the user asked for*, not the artifact | `# tight message` over a one-line commit message; `# Shortened version`; `# Renamed for clarity` |
| **Scaffolding announcement in docs** | README/docstring paragraph about *internal plumbing* (validators, checks, hooks) that the user only cares about as a black box | "The validator enforces that every X has a Y…" when the reader just wants to use X |
| **Defensive reassurance** | Note answering a *worry the user voiced*, not informing a fresh reader | "**Note:** this script is safe — it dry-runs by default…" added after "are you sure?" |
| **Before-state preservation** | "instead of <thing that no longer exists>" / "previously was sync" / "v2: now thread-safe" | `# Using a set instead of a list for O(1) lookups` when no list is in the diff |
| **Changelog-in-code** | `Changes:` / `What's new:` / `Updated:` blocks inside docstrings or code comments | A docstring listing recent edits rather than current behavior |
| **Chat-pointer TODOs** | TODOs that reference "we", "as discussed", "per the chat", "from earlier" | `# TODO: as we discussed, add retry logic later` |
| **Echoed wording as label** | Section heading or comment that quotes the user's own phrasing back | User called it "the tightening step"; code grows `# Tightening step:` |
| **Diff-encoded names** | Identifier describes the *change* rather than the *thing* | `test_validation_added`, `userIdClearer`, `processV2` |
| **Out-of-scope disclaimers** | Docs section saying what the artifact *doesn't* do because the user said it wasn't needed | "Note: this does not handle Unicode — that's out of scope for now" |
| **Session narration** | README section narrating what *the LLM did this session* | `## What I Added`, `## Changes in this version` (in a new artifact with no prior version) |
| **Acknowledgment trails** | "as requested", "per your feedback", "updated to", "now does X" framing | `# Updated to use async per your feedback` |

---

## What NOT to remove

A comment is **not** a fossil just because it was added during the conversation. Keep anything that:

- Documents a **non-obvious invariant** a future reader would want before editing the surrounding code (`# lock ordering: user_lock before org_lock`).
- Warns about **surprising external behavior** (`# Stripe sends 'livemode' as a string, not bool`).
- Explains **why a choice was made** when the choice would otherwise look wrong (`# off-by-one is intentional — the API treats end as exclusive`).
- Names a **legitimate fast path or invariant** the reader would want labeled (`# fast path: empty input` over an early return that genuinely is a perf optimization).

The fossil isn't the *information*, it's the *framing*. A comment can almost always be rewritten from "as we changed" to "what is true" — same content, no fossil.

---

## Workflow

### 1. Determine scope

Pick the smallest scope that contains "the recent work":

1. **Uncommitted changes** (`git diff` + `git diff --staged`) — preferred when present.
2. **Branch vs main** (`git diff main...HEAD`) — if the working tree is clean and a feature branch is checked out.
3. **Last commit** (`git show HEAD`) — if on main with nothing uncommitted.

Announce the scope you picked in one line before scanning. If the user passed a path or a commit range, use that instead.

### 2. Scan

Walk every added/modified line. For each:

- Match against the taxonomy.
- Apply the litmus test.
- Classify: **fossil**, **borderline**, or **keep**.

Scan **all artifact types** in the diff, not just code: Markdown (README, docs), commit messages, PR descriptions, test names, identifier names, code comments, docstrings.

### 3. Apply

- **Fossil**: remove or rewrite. If removing leaves an empty paragraph/section, collapse it too.
- **Borderline**: leave in place, surface in the report.
- **Keep**: silent.

Rewrite when removal would destroy real information — drop the fossil framing, preserve the fact:

```diff
- # Using a set instead of a list for O(1) lookups
- seen: set[str] = set()
+ seen: set[str] = set()  # O(1) membership check is hot in this loop
```

(Or just drop the comment if the perf rationale isn't load-bearing.)

### 4. Report

Output one block per scope. Tight.

---

## Output shape

```
🦴 Defossil — scope: <uncommitted | branch <name> vs main | HEAD>

Removed (<n>)
- <path>:<line> — <pattern>
  was: <quoted snippet>
- <path>:<line> — <pattern>
  was: <quoted snippet>

Borderline (<n>) — left in place, your call:
- <path>:<line> — <quoted snippet>
  fossil case: <why it might be one>
  keep case:   <why it might not>

Kept (<n>): <one line summarizing categories, or omit if zero>
```

If nothing was removed, say so in one line: `🦴 Defossil — scope: <…> — no fossils found.` Don't pad.

---

## Anti-patterns

- ❌ Removing every comment in the diff. This is not a comment-stripper. Comments that explain non-obvious *why* survive — only conversation-residue framing dies.
- ❌ Removing a comment because it was added in this session. Provenance isn't the test; the litmus test is.
- ❌ Inventing fossils. If the diff is clean, the report says so. Don't manufacture findings to look productive.
- ❌ Silently auto-applying borderline removals. Borderline goes in the report, not the diff.
- ❌ Rewriting "as we discussed" comments into "as previously discussed" comments. The whole framing has to go, not the pronoun.
- ❌ Touching files outside the scope you announced. If you said "uncommitted changes," don't reach into `git log`.
- ❌ Generalizing to over-commenting cleanup ("# increment counter", "# loop through items"). That's a different skill's job.
