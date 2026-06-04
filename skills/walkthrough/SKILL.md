---
name: walkthrough
description: Guided, debugger-style tour of one concrete code path — a screen per step that carries one real value forward as it visibly transforms. Use when the user types /walkthrough or asks to be walked or driven through how a request, command, event, pipeline, feature, or flow works end to end, step by step, or function by function.
argument-hint: "[path, feature, or flow to walk — optional]"
disable-model-invocation: true
---

# walkthrough

Drive the user through one concrete code path the way a debugger does: stop on
each step, show its source, explain why it exists, draw where it sits in the
system, and carry one concrete value forward — visibly transformed at every
stop. The user steps; you narrate. Never race ahead.

## What counts as a path

A *path* is an ordered sequence of **steps** that one value (or thread of
control) moves through, from a **trigger** to an **outcome**. Most programs have
them — a request through handlers, a record through pipeline stages, arguments
through a CLI, source through compiler passes, an event through reducers, a job
from trigger to side effect.

Only three things change with the program type; the format below is identical
for all of them. Name them for the project at hand, then walk:

- **The step unit** — usually a function, but a pipeline stage, a middleware, an
  event handler, a compiler pass, or a state transition all qualify.
- **The value that flows** — what the data panel tracks (a request, a record,
  parsed arguments, an AST, accumulating state, a message…).
- **The trigger** — the one concrete instance you trace (one call, one input
  row, one command, one event), not the abstract feature.

## Quick reference

| Control | Meaning |
|---------|---------|
| `n` / next | Step **over** — advance to the next step in the runtime flow. |
| `s` / step into | Go **deeper** — unfold the current step's machinery or a callee. |
| `b` / back | Return to the previous stop. |
| (a bare question) | Answer in place. **Do not advance.** Questions are not `next`. |

Offer these at the end of every stop. Wait for the user. The user drives.

## Phase 0 — absorb before you walk

1. **Read the relevant code yourself**, into your own context — enough to cite
   `file:line` and field follow-up questions without re-reading. Do not delegate
   the reading to a sub-agent that returns only a summary; you need the code in
   hand for the interactive Q&A.
2. **Pick ONE concrete happy path** tied to a real trigger (one API call, one
   CLI invocation, one input record, one published event). A named, specific
   journey beats "the whole module" — it gives the data panel something real to
   carry.
3. **Map the whole path first**, end to end, as a one-line pipeline. This becomes
   the reusable minimap. Find the entry-point step.
4. **Announce readiness**, propose the path + entry point, and start at Stop 1.

## The stop format

Every stop is **one step**, rendered as a framed screen with these sections in
this exact order. Consistency is the point — the user learns the layout once.

1. **Screen-border header** — stop number / total, step name, `file:line`.
2. **🗺️ minimap** — the same ASCII pipeline every stop, with the current node
   marked. Only the marker moves between stops.
3. **🧠 what it does** — its *role in the broader flow* and the non-obvious WHY.
   Do **not** restate the code in prose; the code is right there.
4. **Code excerpt** — paste the *actual* step's source. Trim noise with `...`.
   Annotate the load-bearing lines with inline `# ← …` arrows. Show enough to be
   real, not the whole module.
5. **🧳 data panel** — the value the path carries *at this point*. This is the
   spine of the whole technique: it must **visibly change** each stop (a parsed
   argument, a derived field, a transformed record, an accumulated total, a new
   state). Carry it forward so the user watches the value take shape.
6. **🎛️ controls** — the table above, phrased for *this* stop (name what `n`,
   `s`, `b` lead to), plus "ask anything inline".

Close each stop with a thin `end stop N` rule so screens are visually separate.

## Rules that make it work

- **One step per stop.** Resist dumping a whole file. Depth comes from `s`.
- **Cite `file:line` every time** — they are clickable; they anchor trust.
- **Reuse one minimap.** Redrawing a different diagram each stop destroys the
  sense of place. Keep it simple and hand-written — do **not** invoke a
  diagram-rendering skill; plain ASCII is the whole aesthetic.
- **The data panel earns its keep only if it transforms.** If a stop doesn't
  change the value, say so explicitly ("nothing added yet — the change is next
  stop") rather than showing an identical panel.
- **Honesty flag** when a step lives in framework/library code, not the
  project's own source: show the project's touch-point, then describe what the
  external code does. Don't fake a `file:line` you can't point at.
- **Questions are not `next`.** Answer a mid-stop question in place, in a small
  framed side-trip, then return the user to the same controls. Only `n`/`s`/`b`
  move the cursor.
- **Finish with a full-journey recap** — the whole path compressed to one
  annotated block, ending in the single sentence the user should remember.

## Visual kit

Copy these. Keep widths consistent across a session.

Screen-border header + footer:

```
╔══════════════════════════════════════════════════════════════════════════════╗
║   ▶  STOP 3 / 8   ·   <step_name>   ·   <what happens here in 4-6 words>        ║
║      📄 path/to/file.ext:120                                                   ║
╚══════════════════════════════════════════════════════════════════════════════╝
   ...sections...
╚══════════════════════════════ end stop 3 ═══════════════════════════════════╝
```

Thin section rule (one per section, with its emoji label):

```
──────────────────────────────────  🧠 what it does  ──────────────────────────────────
```

Minimap (mark the current node with `^^^` or `[brackets]`):

```
entry ─→ step ─→ [current step] ─→ step ─→ result
                  ^^^^^^^^^^^^^^
                  3–5 words on what it does
```

Data panel (two columns when an input becomes an output):

```
INPUT (what arrives)                     →   OUTPUT (what leaves this step)
─────────────────────────────────           ─────────────────────────────────
<value as it enters>                         <value as it leaves>   ◀── what changed
```

## Example

See [`references/example.md`](references/example.md) for one fully-formed stop
that assembles every section above. Read it before your first stop so your
rendering matches.
