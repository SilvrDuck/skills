---
name: rp
description: Roleplay a blind end user to QA a product through its real control surface (UI, CLI, or API), surfacing where actual users get confused, make mistakes, or give up. Use when the user types `/rp`, or asks you to playtest or roleplay as an end user, act as a first-time or non-technical user, run blind or persona-based QA, do guerrilla usability testing, or "pretend you don't know this project". Be pushy — trigger whenever simulating a real user's blind, first-time experience would surface usability, onboarding, or robustness problems.
argument-hint: "[what to test / persona hint — optional]"
---

# rp

Roleplay QA: you cast a believable end-user persona, dispatch a **context-free subagent** to play that user against the *real* product, and keep a think-aloud `RP-LOG.md` of the whole journey. Then you debrief — where they got stuck, what broke, what delighted them. The point is to find the friction your own familiarity hides.

## The core move — read this first

**You cannot un-know this project.** You built it, or you've read it this session. Pretending to be a naïve user *in your own context* is theater: you'll glide past the exact spots where real users fall. So you do not roleplay inline.

The actual blind user is a **fresh subagent** with none of this conversation's context. You *cast* it and *dispatch* it; its blindness is real, not performed. Its job is to flounder convincingly. Yours is to watch and learn.

Two hard walls make the run honest — the actor must never cross them:

1. **Only the real end-user control surface.** The actor drives the live UI (browser automation), the HTTP API (`curl`/`httpie`), or the actual CLI binary — whatever a user is handed. If a user couldn't see it or do it, neither can the actor.
2. **Never read the repo's internals.** No opening, grepping, or listing source, configs, or developer docs to figure things out. A user doesn't have the code. The actor reads only what's *on screen* plus what a user is explicitly given (the entry URL/command, public README, `--help`). The bugs you want live exactly where the actor would be tempted to peek.

(If a run wants a looser wall — actor may "google", i.e. read public user-facing docs when truly stuck — decide that during casting. Default is the hard wall above.)

## Phase 1 — Cast the persona (you interview the user)

Interview the user to build a **Casting Sheet**. Ask a *handful* of focused questions, adaptively — prefer the choice widget, branch on each answer, don't read out a fixed list. Any persona hint in the `[argument]` seeds the first question. Pin down:

- **Surface & entry point** — what's under test, and the *real* way a user reaches it (a URL, a command to run, an API base + the public contract). How is it launched?
- **Persona** — who they are, technical skill, domain knowledge, what they know and *don't*, device/constraints, and **disposition** (patient vs. bails fast; cautious vs. clicks everything; reads vs. skims).
- **Mission** — the goal in the user's words, as a *charter, not steps* ("sign up and create your first project", never "click Settings then New"). Let the actor find the steps, badly if that's realistic.
- **Done & bounds** — what counts as success, what's out of scope, and a rough time box.
- **Seeds** *(optional)* — a known-rough area or a real support-ticket pattern worth reproducing.

Show the Casting Sheet and get a nod before dispatching. Keep it tight — one persona, one mission per run is the default.

## Phase 2 — Run the blind play (dispatch the actor)

1. **Pick the control surface** (table below) and make sure the product is actually reachable — launched, server up, binary built.
2. **Smoke-test the surface first.** Before dispatching, confirm the actor's control path actually elicits a response — load the URL, hit the endpoint, run `--help`, send one relay turn. If it's a silent no-op or the path is wrong, fix it *now*. A dead surface wastes a whole blind run and masquerades as a product bug.
3. **Prep the log.** `RP-LOG.md` lives at repo root and is **gitignored, never committed** — append `RP-LOG.md` to `.gitignore` if it's not already there.
4. **Dispatch ONE subagent** (general-purpose) seeded with *only*: the Casting Sheet, the contents of [`references/actor-brief.md`](references/actor-brief.md), the entry point, which tool family to drive the surface with, and the absolute path to `RP-LOG.md`. Pass **nothing else** from this conversation — that's what keeps it blind.
5. **Don't coach it.** A real user has no one to ask. If the actor surfaces a question, it gets no answer — that *is* the finding.

**Scaling up (only on request):** dispatch a small **panel** of 2–3 distinct personas as parallel subagents (e.g. rushed novice, cautious expert, mobile user), each appending to its own `## <persona>` section of the log.

### Control surface — how a real user drives it

| Product is a… | Actor drives it via… | A user reads only… |
|---|---|---|
| Web app / SPA | browser-automation tools (navigate, click, type, read the rendered page) | what's rendered on screen |
| HTTP / REST / GraphQL API | `curl` or `httpie` against the public endpoint | the documented/public contract |
| CLI tool | the actual command | `--help` / `man`, at most |
| TUI / desktop / Electron | launch and drive the real app | the visible interface |
| Chatbot / agent skill / prompt / conversational product | a **turn-relay loop** (see below), not a fire-and-forget subagent | only the assistant's replies |
| Nothing runnable | walk the **user-facing docs** as the surface — and flag the run as lower-confidence in the log | the docs as written |

If the surface needs tools that aren't loaded (e.g. browser automation), tell the actor to search its available tools for them.

**Conversational products (a skill, a system prompt, a chatbot).** A dispatched subagent *cannot* be the blind user here — it can't reliably trigger the thing or see what a real user sees (a sub-agent often can't even invoke a project skill). So split the roles: **you (top-level) play the product; the subagent plays only the user.** Relay turns between them — the user-subagent sends one plain message and stops, you produce the product's *real* response and relay it back, it reacts and logs, repeat until it completes or bails. To play a skill faithfully, follow its own instructions yourself; if it's user-gated (`disable-model-invocation`), read its SKILL.md and execute it — never hand those instructions to the user-subagent, that would break its blindness.

## Phase 3 — Debrief (you synthesize)

Read `RP-LOG.md` plus the actor's report. **Lead with the single worst moment.** Then group findings:

- 🧱 **Friction** — every hesitation, misread, wrong turn, and "where is it?". Tie each to the persona trait that caused it. This is the gold; happy-path testing never finds it.
- 🐛 **Bugs / dead-ends** — real defects, each with exact reproduction (the actions/commands/requests, not guesses about the code).
- 😀 **Delights** — what was genuinely smooth.

Give each finding a severity and point to the log step where it happened, plus a concrete fix. Close by asking the user: **keep `RP-LOG.md`, or delete it?**

## Anti-patterns

- ❌ Roleplaying inline in your own context. You know too much — it's theater, and it finds nothing.
- ❌ Letting the actor read source/internal files to "figure it out". That's the bug hiding from you.
- ❌ A step-by-step charter. Hand a mission; let the actor flounder realistically.
- ❌ Coaching the actor or answering its mid-run questions. Real users are alone — their being stuck is the data.
- ❌ Optimal play. Real users satisfice, skim, mistype, and quit. An actor that breezes through learned nothing.
- ❌ Reporting only what crashed. Confusion, hesitation, and near-misses are the point.
- ❌ Committing `RP-LOG.md`. It's gitignored and disposable; the user decides keep-or-delete at the end.

## See also

- [`references/actor-brief.md`](references/actor-brief.md) — the full briefing handed to the blind actor: staying in character, simulating realistic mistakes, the think-aloud RP-LOG format, and the return report.
