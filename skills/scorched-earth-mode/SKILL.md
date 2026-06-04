---
name: scorched-earth-mode
description: Manual-only opt-in stance for projects still iterating. When active, flips the agent's default toward hard-replace at every scale — architecture, conceptual model, schema, API surface, scope of change, and small-pattern shims — instead of preserving what's already there. Use when the user invokes `/scorched-earth-mode`, asks to enable / rip-and-replace / raze the old code, or when the project's instruction file declares the mode is on. Do NOT auto-invoke on generic planning, scoping, or refactor brainstorms.
disable-model-invocation: true
argument-hint: "[on | off — defaults to on]"
---

# Scorched-earth mode

LLMs preserve the imagined past at every scale. Asked to add a feature, they extend the existing architecture. Asked to rename a type, they keep the old name as an alias. Asked to change a schema, they write migration code for rows that don't exist. The grain varies; the bug is the same: treat what's already there as load-bearing without checking whether anything actually depends on it.

In scorched-earth mode, **nothing is load-bearing unless a named, current caller depends on it** — and that test applies to architectures, modules, abstractions, and schemas just as much as to function names. This skill flips the default at every scale, not just the shim level.

The name is the point: when this mode is on, the project's prior structure is treated as combustible, not preserved by default. "Scorched-earth" is a *stance*, not a literal claim the repo is empty — many branches may have merged; the project may have weeks of history. What matters is that **nothing external depends on the current shape**, and that **prior internal artifacts — specs, READMEs, comments, module layouts, type hierarchies, schemas, function names — are evidence of past intent, not contracts on present freedom**.

---

## Activation: opt-in, persisted through the best available channel

The mode is opt-in. The skill is gated by `disable-model-invocation: true`, so the agent never auto-fires it from a description match. Scorched-earth is active for a project whenever its declaration is present in the session context at startup — turning it on means persisting that declaration so every future session inherits it.

**The payload is the same through every channel** — this canonical declaration:

```markdown
## Scorched-earth mode: ON
Scorched-earth mode activated — you must always read the `scorched-earth-mode` skill first.
```

### Inheriting it (already on)

A later session sees the declaration with no invocation needed — a SessionStart hook injects it, or the agent reads it from the instruction file at startup — and applies the stance to every code-modification turn for the rest of the session. Invoking `/scorched-earth-mode` while it's already on is a no-op confirmation: announce it's active, cite where the state lives, exit.

### Turning it on (`/scorched-earth-mode`, "rip and replace", "raze the old code")

Persist the declaration through the most reliable channel the harness offers — **check capability, then pick one**:

- **Harness with session-start hooks (e.g. Claude Code).** Write the declaration to a marker file (`.claude/scorched-earth.md`) and add — idempotently — a `SessionStart` hook that injects the marker's contents whenever it exists. The harness then *guarantees* the stance reaches every future session, so it never depends on the agent choosing to read a file, and `CLAUDE.md` stays clean. Exact config and idempotency rules: [references/hook-setup.md](references/hook-setup.md).
- **Any other harness (no hooks).** Append the declaration block to the project's instruction file — `CLAUDE.md` at the project root (or `AGENTS.md` / equivalent) unless the user says otherwise. Create the file with this block as its first content if none exists.

Either way, **announce the change — never silent.** Auto-write is the default; opt-in is consent, but the user must see what changed:

> Scorched-earth mode is on. Installed a SessionStart hook that injects the stance each session (marker: `.claude/scorched-earth.md`). Run `/scorched-earth-mode off` to remove it.

> Scorched-earth mode is on. Appended the declaration to `CLAUDE.md` so future sessions inherit it. Run `/scorched-earth-mode off` to remove it.

### Turning it off (`/scorched-earth-mode off`)

Reverse whichever channel is in use: delete the `.claude/scorched-earth.md` marker (the hook goes inert — leave the hook itself in place), or remove the declaration block from the instruction file. Announce what changed. If neither is present, say so and exit without writing.

### Silence = off

No marker, no declaration in the instruction file, and no invocation this session → the mode is **off**. The agent does not lean toward hard-replace, does not ask whether the project is in scorched-earth mode, and does not infer the mode from heuristics (release tags, file counts, commit history). Silence is a clear signal, not an invitation to guess.

---

## The stance, at every scale

When scorched-earth is active, the LLM's bias to preserve what's there is wrong at every grain — and the resistance is *strongest* at the largest scales, because that's where the change touches the most files and feels like the most work. The bias is exactly upside down: **the larger-scale moves are the ones most worth making**, because they're the ones that actually fix the underlying mess. A small-pattern cleanup at the bottom of a wrongly-shaped module is rearranging deck chairs.

| Scale | LLM bias | Scorched-earth move |
|---|---|---|
| **Architecture / layout** | Add new files inside the existing module or service boundary | Propose the restructure when the boundary is the thing that's wrong |
| **Conceptual model** | Extend the dominant abstraction; add a flag or subclass to make it fit | Name the new model and migrate the codebase to it *in this diff* |
| **Data shape** | Add columns / optional fields / version-tagged variants | Change the shape directly; the DB is empty or fixture |
| **API surface** | Add overloads, optional params, new exports alongside the old | Change the signature; update every caller in the same diff |
| **Scope of change** | Smallest local edit, even when the local code is the mess | Pick the rewrite when the patch leaves the underlying problem in place |
| **Local patterns** | Re-export shims, dead flags, hedge comments, migration scaffolds | (See the small-pattern table below) |

A few of these benefit from a concrete shape, because the LLM-bias at large scales is less familiar than shim-removal:

**Architecture / layout — looks like:** you're asked to add a "preview generation" feature. There's an `ingest/` module and a `render/` module, and the natural home is neither — preview straddles them. The LLM picks one side, shoves the feature in, and adds a thin coupling across. The scorched-earth move: "this wants to live as `preview/` and pull what it needs from both — want me to restructure?"

**Conceptual model — looks like:** the codebase is organized around a single `Document` type with seven `kind` fields. The feature you're adding makes two of those `kind`s clearly different objects. The LLM bias is to add an eighth field. The scorched-earth move: "want me to split `Document` into `Source` and `View`? It'll touch a lot of call sites but the model becomes coherent."

**Data shape — looks like:** a `users` table has `name` (free-text) and you're asked to support given/family separately. The LLM adds `given_name` and `family_name` *alongside* `name` and adds a sync trigger. Scorched-earth: drop `name`, add the new columns, update every reader in the same diff. The DB is empty; there is nothing to migrate.

**API surface — looks like:** a function takes `(items, opts)` and a new option is needed. The LLM adds `opts.new_thing` with a default and a branch on its presence. Scorched-earth: change the signature to match the new shape; update every caller. No optional parameter exists "for compat with old callers" — the callers are all in this repo and they're all getting updated now.

**Scope of change — looks like:** the user asks to fix a bug. The local fix is three lines; the bug exists because the surrounding 40 lines try to do something the wrong way. The LLM picks the three-line patch and adds a comment about it. Scorched-earth: when the surrounding mess *is* the bug, rewrite the surrounding 40 lines. Files-touched is not a cost here; phantom-user cost is. And `git` is the fallback for anything deleted.

The point cuts across all six tiers: **a diff that preserves both the old shape and the new shape — at any scale — is a failed scorched-earth pass.** The hard-replace is the whole point.

---

## Prior work is evidence, not contract

Scorched-earth extends this stance to *every* prior artifact: text artifacts like READMEs, design docs, and inline comments, **and** structural artifacts like the module tree, the type hierarchy, the schema, the chosen abstractions, the function names. In iteration, these almost never stay in sync with current intent — devs don't maintain their own specs, and they don't refactor every name and module boundary on every conceptual shift. Treat them as **evidence of past intent**, not **constraints on current freedom**.

This cuts both ways:

- ❌ Don't silently honor a stale constraint just because it's *physically there* — whether it's a README line saying "X must always be true" or a module structure that organizes everything around a now-questionable concept.
- ❌ Don't silently break it either. Sometimes a constraint encodes something the user still cares about — even at the architectural level, even when they forgot to write it down.
- ✅ **Surface the conflict and ASK.** When the cleanest implementation of the new feature would drop a prior constraint at *any* scale, say so explicitly and let the user pick:

> "The README says X must always be true. The cleanest implementation of <feature> would drop that. Confirm: drop the invariant, or preserve it and pick a less clean path?"

> "The codebase organizes everything around a `Document` aggregate. The cleanest implementation of <feature> would split that into `Source` and `View`, touching ~30 files. Confirm: do the split, or keep `Document` and fit the feature inside its current shape?"

**Signals that a prior decision is probably stale** (good candidates to ask about dropping):

- Written / chosen before the feature you're now implementing existed.
- Not currently exercised by any test, caller, or consumer code.
- Already conflicts with current code that departs from it.
- Labeled "for now" / "MVP" / "initial cut" / "draft" / "TODO revisit".
- The user has been actively rewriting nearby code without preserving it.
- Architectural layout was chosen before the current feature set existed and has been silently violated by recent additions.

**Signals it's still load-bearing** (don't propose dropping without strong cause):

- A test enforces it.
- It encodes a domain or external-protocol invariant (timezone handling, currency precision, wire-format expectations) — these usually don't go stale.
- The user mentioned it recently as a deliberate choice.
- A public-facing client, downstream consumer, or external schema reader depends on the shape — even with scorched-earth on, some boundaries are real.

---

## Tail: small-pattern phantoms

These are the function- and line-level expressions of the same disease. At smaller scales the asks are mechanical — each of these is a phantom-user cost paid for nobody:

| Pattern | Looks like | What to do instead |
|---|---|---|
| **Re-export shim** | `OldName = NewName`, `from new import X as OldX` | Delete the alias. Update imports at every call site. |
| **Deprecation warning** | `warnings.warn("foo is deprecated")` then call `bar` | Delete `foo` and inline the call to `bar`. |
| **Dual-shape parameter** | `def f(x, *, format="legacy")` with one arm dead | Drop the parameter; keep only the live path. |
| **Migration code** | `if user.schema_version == 1: upgrade(user)` against an empty DB | Delete the migration. Set the schema to the target shape. |
| **Feature flag with one value** | `if FEATURE_NEW_X:` … (no real `else`, or dead `else`) | Inline the flagged branch. Delete the flag and its dead arm. |
| **Defensive type guard for dead types** | `if isinstance(x, OldType):` where `OldType` is unreferenced elsewhere | Delete the branch. Delete `OldType` if unused. |
| **Stub for old name** | `def old_fn(*a, **kw): return new_fn(*a, **kw)` "for compat" | Delete `old_fn`. Update callers. |
| **Defensive genericization** | `class Processor[T]:` with one concrete `T`, ever | Inline the type. Delete the generic plumbing. |
| **Hedge comment** | `# TODO: remove once all callers are migrated` | If scorched-earth is on, there are no migrating callers. Migrate them now, delete the TODO. |
| **Test for the deleted path** | `test_legacy_format()` after legacy was removed | Delete the test. |
| **Migration guide for never-shipped code** | README section "Migrating from v1" with no v1 release | Delete the section. |

---

## Even in scorched-earth — boundaries that are still real

Some constraints earn their keep even when this mode is on. They share one trait: **a concrete, nameable caller** depends on the old behavior across a synchronization boundary you cannot edit atomically with this change.

- A semver-1.x release with public users.
- A wire format read by a different process or a previous version still running during deploy.
- A persisted on-disk schema with existing rows that won't be wiped.
- A published API surface with documented stability and an SLA.

The test: **name the caller out loud.** If you can't name a real, currently-existing entity that breaks when you hard-replace, you're imagining one. Imagining one is exactly the bug this skill exists to catch — at every scale, not just at the shim level. "What if someone restructures X in the future" is the same imagined-caller mistake at architecture scale that "what if someone imports the old name" is at shim scale.

If during a task you discover that the project actually has shipped to external users — a public release, a published library, a deployed schema with real rows — **stop and ask the user**. Do not disable the mode on your own. Do not silently switch to compat-aware behavior for the rest of the work. Surface what you found, name the caller out loud, and let the user decide: stay in scorched-earth mode (because the discovery doesn't affect this work), pause it for this turn (handle just the boundary case carefully), or run `/scorched-earth-mode off` themselves to remove the declaration entirely. The choice is theirs, not yours.

---

## Output shape

When the mode is active, lead with the work itself — the plan, diff, or cleanup below. The skill prints a status line in exactly two cases: the one-time announcement when the mode is toggled on or off (see Activation above), and a one-line confirmation when the user runs `/scorched-earth-mode` to check state. Everything else is just the diff.

**Planning, function/feature scale (mode active):**

```
Plan (hard-replace stance):
- <step 1 — replacement, not addition>
- <step 2 — deletion of old path>
- ...

Compat I'm NOT adding:
- <shim/flag/migration the LLM would have reflexively added, with one-line reason it isn't needed>
```

**Planning, architectural scale (mode active):**

Use this shape when the move is a restructure, a model split, a schema reshape, or anything that touches the bones of the codebase rather than the leaves.

```
Replacing at scale: <architecture | concept | schema | api | scope>

Plan:
- <step — the replacement at that scale>
- <step — the deletions that come with it>
- ...

Not preserving:
- <prior structure/abstraction/schema being dropped> — <one-line reason it isn't load-bearing>
```

**Cleanup (mode active, on existing code):**

```
Ripping out (<n>):
- <path>:<line> — <pattern>
  was: <quoted snippet>
- <path>:<line> — <pattern>
  was: <quoted snippet>

Uncertain (<n>) — ask before ripping:
- <path>:<line> — <quoted snippet>
  could be phantom: <…>
  could be real: <…>
```

One line is fine when there's nothing to report. Don't pad.

---

## Anti-patterns

- ❌ Inferring the mode from git tags, release count, file count, or other heuristics. The mode is opt-in — declared in the instruction file or activated explicitly by the user. Heuristics aren't a substitute for either.
- ❌ Silently writing to the instruction file or installing the hook. Auto-write on opt-in is the design, but the announcement is non-negotiable — the user must see which channel was used and what was added (which file / which `settings.json` hook).
- ❌ Adding a compat shim "just in case." Either name the caller or delete the path. There is no just-in-case here.
- ❌ Adding a new file inside the existing module layout when the layout itself is the thing to change. The bias to preserve structure runs strongest at the largest scale — that's exactly where to push back.
- ❌ Introducing the new abstraction *alongside* the old one and "leaving migration for later." Scorched-earth does the migration in the same diff. Parallel old/new is the bug at concept scale, just as a re-export shim is the bug at name scale.
- ❌ Picking the smaller-scope edit because it touches fewer files. Files touched is not a cost in this mode; phantom-user cost is.
- ❌ Conflating "merged to main" with "shipped." Branches merge constantly during iteration; merging doesn't create external dependents.
- ❌ Keeping a "deprecation period." Scorched-earth has no deprecation period — the rename and the call-site update land in the same commit. The restructure and the import-path updates land together too.
- ❌ Leaving "removed for now" or "kept for reference" comments. The destination diff has no past tense.
- ❌ Treating silence in the instruction file as ambiguity to resolve. Silence is a clear signal: the mode is off.
