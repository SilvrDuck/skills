---
name: protodoc
description: Doc-driven design for a product that does not exist yet — a local doc site the user marks up like a shared document, exported as a build spec an implementing agent works from. Use when the user types /protodoc, or wants to design, spec, or think through a product, feature, or system before building it — "let's design X", "spec this out", "docs first", "doc-driven development", "prototype this idea on paper", "what should we actually build". Be pushy — offer it whenever someone is about to start coding something substantial with no written design.
argument-hint: "[what you want to design — optional]"
disable-model-invocation: true
---

# protodoc

Write a product's documentation before the product, then argue about the documentation until it is right. Two phases — **what it does**, then **how it's built** — each reviewed in a local doc site, each ending at a gate. The deliverable is `BUILD.md`, which an implementing agent reads before writing any code.

**Answer every annotation, explicitly.** Never silently apply a note, never silently drop one. Each gets a reply carrying one of four states, and the user sees all of them in the margin. A round where notes vanish into a rewrite is a failed round.

## Commands

`P=<this-skill-dir>/scripts/pd.py`, `D=protodoc/<slug>`.

| Command | Use |
|---|---|
| `python3 $P init <slug> [--addition]` | scaffold `protodoc/<slug>/`, git-exclude its `.state/` |
| `python3 $P serve $D` | review site — **run in background**, read the port from `$D/.state/server.json` |
| `python3 $P watch $D` | blocks until the user sends notes, then prints what needs answering |
| `python3 $P show $D [--all]` | current annotation state without waiting |
| `python3 $P reply $D --id N --state S --text "…"` | answer one note, which resolves it; `S` ∈ applied, applied-differently, pushed-back, needs-you |
| `python3 $P ask $D "<question>"` | show the page you're blocked on an answer in chat |
| `python3 $P phase $D <user-doc\|tech-doc\|export>` | advance the phase |

## Flow

**0 — Frame.** Read what already exists first — briefs, specs, READMEs, prior design docs in the working directory. That material is the richest input you will get, and it answers most of what you would otherwise ask. Then interview for what is genuinely missing, one question at a time, until you can describe the finished product; stop there rather than chasing every detail, because a draft surfaces the rest faster than questions do. If the directory holds a real codebase, ask once whether this is a new product or an addition to that one; for an addition, `init --addition` and read the existing architecture before phase 3.

**1 — User doc.** The manual you'd ship for the product **finished** — every feature, every surface, written as though all of it exists today. This is not an MVP and not a first iteration: carving increments out of it is someone else's job afterwards, and they can only do that if the whole shape is on paper. Never cut scope to make a round easier to review — sequence the writing instead: lay down the full page set first, then fill the pages in, letting the user review each as it lands. Start the server, hand over the URL, and say what the three verbs do.

**2 — Gate 1.** Reality check, then ask. See *Gates*.

**3 — Tech doc.** `phase $D tech-doc`. Architecture, data model, interfaces, and the alternatives you rejected with the reason. Every claim must trace to something in the user doc; if it doesn't, either the tech doc is inventing scope or the user doc is missing a promise.

**4 — Gate 2.** Same ritual.

**5 — Export.** `phase $D export`. Write `BUILD.md`, extract each mockup to `mockups/<page>-<screen>.html`, and make one final pass over `DECISIONS.md`.

## The review round

1. Write or revise docs. Only the blocks you touch get marked as changed, so **patch surgically** — a wholesale rewrite marks the entire page and destroys the user's ability to see what moved.
2. `watch` blocks until they send notes. While it blocks, do nothing else.
3. **Discuss the batch in chat before touching a file.** Argue with what deserves arguing, propose alternatives, group notes that are really one disagreement. A round that silently applies fourteen notes taught nobody anything.
4. `reply` to **every** note. That resolves it, which is not deletion — the user can reopen anything they are not finished with. **A round ends with zero open notes.**
5. Revise the docs. Do not stop at the annotated sentences: a note about one screen usually invalidates a rule three pages away, and the conversation itself decides things nobody annotated. **The docs must read as the current shared understanding of the product, not as the first draft plus patches.**
6. Redistil `DECISIONS.md`, then say in chat what changed, what you pushed back on, and what you changed that nobody asked about.
7. `watch` again.

Keep exactly one `watch` running — a dead watcher means Send does nothing and the page says so. Blocked on an answer mid-round? `pd.py ask $D "<question>"` puts it in the page so they know to come back. On `TIMEOUT`, ask whether they're still reading rather than looping.

## The three verbs

| Verb | They mean | You do |
|---|---|---|
| **comment** | discuss this | reply, revise if they're right |
| **suggest** | replace it with *this* | apply verbatim, or reply why not |
| **doubt** | this smells wrong, I can't say why | investigate, then a sourced verdict |

**doubt** is the heavy one. The user is flagging something you wrote as a possible smell — they suspect it's wrong but don't know the right answer. Do not defend, do not capitulate. Re-examine it with fresh skepticism, find out, and come back with exactly one verdict: *they were right* (say what you missed), *it holds* (cite what proves it, and grant why the smell felt real), or *genuine tradeoffs* (two or three options, each with its cost, and a recommendation). Never "it depends".

Raise the same thing unprompted when a note would break something you know about — reply `pushed-back` and let them overrule.

## Rigidity

Tag every real decision, in the doc where it's made and again in `BUILD.md`:

- **pinned** — the product dies without it
- **negotiable** — a guess that happened to need a value; deviate if reality disagrees
- **constrained** — existing code already decided this (addition mode only)

Mockups are `negotiable` by default. A drawn screen reads as decided, and it isn't — pin one only when the user says so.

## Gates

Before asking, run a **reality check**: attack your own doc and report what you find. What's expensive, what's hand-waved, what assumes a thing that may not exist, what did you draw because it looked good rather than because it's right. Findings become notes you answer, or open questions carried into `BUILD.md`.

Then ask in chat using the harness's multiple-choice tool: lock and move on / keep refining / reopen a specific decision. Never assume a gate. Locking freezes that doc — later changes to it are fine but must be logged in `DECISIONS.md` with the reason, so a reopened decision leaves a trace.

## Writing the docs

Structure, mockup markup, `BUILD.md` and `DECISIONS.md` skeletons: [`references/templates.md`](references/templates.md). Read it before drafting the first page.

Pages are `NN-name.md` in `user-doc/` or `tech-doc/`, ordered by prefix, titled by their `#` heading. Markdown supports headings, lists, tables, quotes, fenced code, `mermaid` fences, and raw HTML blocks.

## Anti-patterns

- **Shipping an MVP.** Descoping to a first slice, a phase 1, a "core loop". The deliverable is the finished product; someone else extracts the increments.
- **Inventing over asking.** When a gap would change the product, ask. Only fill it in yourself when told to, and tag what you filled `negotiable`.
- **Rewriting a page to address one note.** It nukes the change marks the user reads by.
- **Silent obedience.** Applying a note you believe is wrong, without saying so.
- **A doc that only describes.** If nothing in it could turn out false, it isn't a spec.
- **Answering an open question by picking one.** Unresolved questions belong in `BUILD.md`, not quietly decided.
- **Leaving the server running** once `BUILD.md` is written. Stop it; the docs stay.
