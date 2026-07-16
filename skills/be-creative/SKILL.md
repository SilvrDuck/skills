---
name: be-creative
argument-hint: "[request | generate N] [Manual Wikipedia seed link(s) (if harness blocks fetch) — optional]"
description: Inject genuine, surprising originality into a response by anchoring it to an unrelated random Wikipedia article. Use this skill whenever the user asks the agent to be creative, original, surprising, weird, fun, playful, imaginative, "out of the box", "tiré par les cheveux", or asks for ideas/names/designs/stories/explanations/metaphors that need fresh angles. Also trigger when the user explicitly says "be creative", "/be-creative", or "creative skill", or whenever the request is open-ended enough that a stock answer would feel generic and a novel angle would clearly serve them better. Prefer triggering over not triggering when creativity is even loosely implied.
---

# Be Creative Skill

The goal of this skill is to make your answer feel like it came from a more imaginative version of you, not a generic "creative-sounding" one. The trick: ground each independent creative decision in its *own* real, unrelated artifact (a random Wikipedia article) so every angle you take is genuinely unexpected, not a recycled cliché. A single global seed only shifts the top-level framing — a distinct seed per decision stops your default priors from quietly steering everything downstream.

The user should not see the scaffolding. They simply get an unusually inspired answer.

## Generate mode (raw seed list)

If the request is `generate N` (or otherwise asks for a plain list of N random Wikipedia links), skip the entire creative workflow below. Fetch N random articles and output **only** the URLs — one per line, in a code block, nothing else: no intro, no rationale, no creative answer. This exists to hand a copy-pastable seed list to another sandboxed agent that can't reach Wikipedia itself.

```bash
curl -sL --max-time 8 "https://en.wikipedia.org/w/api.php?action=query&generator=random&grnnamespace=0&grnlimit=3&prop=info&inprop=url&format=json" \
  | python3 -c "import json,sys; [print(p['fullurl']) for p in json.load(sys.stdin)['query']['pages'].values()]"
```

Set `grnlimit` to N (one call handles a few hundred). No `extracts` are fetched — the links are the whole output. If the curl is blocked, the same rule as below applies: never hand-pick, ask the user to paste `Special:Random` URLs.

## How to use this skill

### 1. Fetch one random article per creative decision, in a single batch call

**First, decompose the request into its independent creative decisions.** A creative decision is a distinct choice the answer commits to — the naming, the structure, the tone, a core mechanic, a visual motif — *not* every item inside one decision. If a decision produces a list (eight candidate names), that whole list shares one seed so it stays a coherent set; a *different* decision (the tagline, the architecture) gets its own. A request with a single decision (just "name this tool") needs exactly one seed. Call the count N.

**Then check the user's request for Wikipedia URLs.** If they pasted N links (e.g. `https://en.wikipedia.org/wiki/...`), assume their harness can't reach Wikipedia and they fetched random pages for you. Skip the curl, treat their links as the seeds — one per decision — and go straight to step 2. User-supplied articles are just as valid; the only forbidden source is one *you* pick yourself.

Otherwise, run **exactly this command** with `grnlimit` set to N. It is built so that **only three short lines per article** (title, URL, ~700-char extract) ever reach your context. This matters: the Wikipedia action API returns several KB of metadata per page you don't need, and pulling that into context is wasteful and noisy. The pipe collapses everything to the minimum useful signal.

```bash
N=<number of independent creative decisions>
curl -sL --max-time 8 "https://en.wikipedia.org/w/api.php?action=query&generator=random&grnnamespace=0&grnlimit=$N&prop=extracts|info&exintro&explaintext&exchars=700&inprop=url&format=json" \
  | python3 -c "import json,sys; [print(p.get('title',''),p.get('fullurl',''),p.get('extract','').replace(chr(10),' ').strip()[:700],sep='\n',end='\n\n') for p in json.load(sys.stdin)['query']['pages'].values()]"
```

What the flags do, briefly, so you understand what to keep vs. tweak:
- `generator=random&grnnamespace=0`: random articles from the main namespace (skip talk/user/file pages).
- `grnlimit=$N`: one article per decision, fetched in a single network call — not N separate curls.
- `prop=extracts&exintro&explaintext&exchars=700`: return only the lead section, plain text, capped at ~700 chars **at the API level**. This is the most important filter.
- `prop=info&inprop=url`: include the canonical URL.
- The `python3` step prints just `title`, `fullurl`, `extract` per article, blank-line separated. Nothing else (no IDs, no revision metadata, no `pageprops`, no `continue` tokens) enters your context.

If the command fails, do **not** retry in a loop or fall back to a hard-coded list. Every seed must come from this curl or from the user — **never** from your own web-search, web-fetch, or hand-picked article/number. The instant *you* choose a seed you reintroduce the exact bias this skill exists to remove, so a self-picked seed is worse than not running the skill at all; "too cumbersome for a quick question" is not an exception. So if the host is blocked (sandboxed network), stop and ask the user to open `https://en.wikipedia.org/wiki/Special:Random` **N times** and paste back the N URLs it lands on, then use those as the seeds — one per decision. Let them know they can skip this round-trip next time by pasting `Special:Random` links directly, or by asking a Wikipedia-capable agent for `be-creative generate N`. Otherwise (network down, rate-limited), say why and hard fail.

### 2. Find an oblique connection

For **each** decision, read its article's three lines and look for a non-obvious link to *that* decision. Don't pick the first connection you see. Look for:
- a **structural analogy** (the article describes a system whose shape you can borrow),
- a **vocabulary** you can repurpose (jargon, names, era-specific terms),
- a **constraint** the article suggests (one rep per constituency → "every failure has exactly one owner"),
- a **contrarian framing** (the article's domain values the *opposite* of what the user's domain values).

The further each article sits from the user's domain, the better — that distance is the source of the originality. Keep the pairings separate: decision A's article shapes only decision A, so the seeds don't quietly average back into one.

### 3. Reason about the bridge before answering

Before composing the answer, work through — for **each** decision — a compact block in your reasoning. The user never sees this step; producing it is what keeps each bridge coherent rather than a vague gesture toward the article.

For each decision:
- the decision, plus the Wikipedia title and URL seeding it
- 1-3 sentences on the bridge: what in that article inspired that decision
- (Optional) one angle you considered and rejected, so the choice is deliberate not lazy

Then write a one-line thesis that ties the decisions into a single coherent answer, and answer.

**Optional `--log` flag**: if the user includes `--log` in their request (or asks something equivalent like "save the seeds" or "log it"), also write the per-decision blocks to a temp file at `/tmp/be-creative/<short-slug>.md` on Unix-like systems, or `%TEMP%/be-creative/<short-slug>.md` on Windows. Mention the path in your response so they can read it before the system clears temp on next reboot. Without the flag, no file is written.

### 4. Answer the user's actual request, precisely

This is the part that matters most. **Creativity is not an excuse to miss the brief.** The answer must do exactly what the user asked, just via a more "tiré par les cheveux" route than a default response would have taken. The Wikipedia seed is a lens, not a topic to drag in. If the user asked for a function name, give them a function name. One that happens to be unusually good *because* you let an unrelated article rearrange your priors.

### 5. Stay transparent in tone

Do not announce the skill. Do not name-drop the Wikipedia article. Do not explain the process to the user unless they ask. They get a clean, original-feeling answer. If they later ask "wait, where did that come from?", *then* explain: name the article and walk them through the bridge.

## Why the random seeds matter

Asking an LLM to "be creative" without a stimulus tends to produce the *average* of creative-sounding outputs: the same metaphors, the same whimsical tone, the same three structural moves. An unrelated real-world artifact breaks that average. It forces a specific, particular constraint that no template would have suggested. That specificity is what makes the result feel genuinely original instead of generically "creative".

The article does not need to be a *good* match. A bad match is often better. The further the leap, the more the result looks like a thought a human would have, rather than a thought a model would have. Do this per decision and no single branch of the answer is left on autopilot — the places a one-seed version would quietly fill with defaults each get their own jolt.

## What to avoid

- **Don't shoehorn the article in.** If the only way to use it is to literally mention it, you have failed the brief. The article is a *prior shifter*, not a topic. The names/ideas/phrasing in your final answer should not point back at the seed. A reader looking only at the answer should have no way to guess what the seed was.
- **Don't let the seeds blur or fragment.** One seed per decision, kept separate — but the decisions must still add up to one coherent answer. If each choice reads like it came from a different universe, you fetched seeds without bridging them into a whole. And don't over-split: items inside a single decision share one seed, or you'll drown in curls and lose the set's coherence.
- **Don't sacrifice precision for whimsy.** A creative answer that doesn't solve the user's problem is worse than a boring one that does.
- **Don't skip the structured reasoning.** Generating a block per decision is what forces you to commit to each bridge between article and answer. That's what makes the output coherent rather than scattered.
- **Don't widen the curl filter.** If you find yourself wanting more context from Wikipedia, you're probably trying to make the article fit too literally. Step back and re-read the three lines you have.
- **Don't explain the trick in the answer.** Transparency about *process* belongs in the reasoning, not the response. The answer itself should just feel sharp.

## Example flow

User: *"Give me a name **and** a one-line tagline for an internal tool that watches CI pipelines and pings the right person when something breaks."*

Two independent decisions (naming, tagline) → N=2. One batch curl returns two articles.

**Decision 1 — the name.** Seed:
```
10th Kwara State House of Assembly
https://en.wikipedia.org/wiki/10th_Kwara_State_House_of_Assembly
The 10th Kwara State House of Assembly is the legislative branch of the Kwara State Government... unicameral, with 24 representatives elected from constituencies across the state...
```
Bridge: the useful structure isn't "legislature", it's *constituency-based representation* — 24 territories, each with exactly one member responsible for it. Failures don't get *assigned*, they *belong* to a district, and the tool's real job is maintaining the map. Rejected `Speaker`/`Gavel` (calling-to-order is the wrong half of parliament). → names `Riding`, `Precinct`, `Ward`, `Bailiwick`, each rationalized by *territorial ownership of failure*.

**Decision 2 — the tagline.** Seed:
```
Epistolary novel
https://en.wikipedia.org/wiki/Epistolary_novel
An epistolary novel is a novel written as a series of documents — usually letters, though diary entries and news clippings also appear. The form lends immediacy and a sense of a named, personal correspondent...
```
Bridge: an epistolary story is told through letters, each addressed to one named recipient. Reframe an outage the same way — not a broadcast alert but a letter to the single person who can answer it. → tagline: *"Every outage, told as a letter to the one person who can answer it."*

Thesis tying them together: the tool is a *map of jurisdictions that writes each failure a personal letter to its owner* — one seed shaped the naming vocabulary, a different seed shaped the voice, and neither branch rode on the other's priors. The user gets exactly what they asked for; none of it points back at Kwara or epistolary novels, and if asked you can walk them through both bridges.
