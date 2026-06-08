---
name: be-creative
description: Inject genuine, surprising originality into a response by anchoring it to an unrelated random Wikipedia article. Use this skill whenever the user asks the agent to be creative, original, surprising, weird, fun, playful, imaginative, "out of the box", "tiré par les cheveux", or asks for ideas/names/designs/stories/explanations/metaphors that need fresh angles. Also trigger when the user explicitly says "be creative", "/be-creative", or "creative skill", or whenever the request is open-ended enough that a stock answer would feel generic and a novel angle would clearly serve them better. Prefer triggering over not triggering when creativity is even loosely implied.
---

# Be Creative Skill

The goal of this skill is to make your answer feel like it came from a more imaginative version of you, not a generic "creative-sounding" one. The trick: ground the creative leap in a *real, unrelated* artifact (a random Wikipedia article) so the angle you take is genuinely unexpected, not a recycled cliché.

The user should not see the scaffolding. They simply get an unusually inspired answer.

## How to use this skill

### 1. Fetch a random article, filtered at the command level

Run **exactly this command**. It is built so that **only three short lines** (title, URL, ~700-char extract) ever reach your context. This matters: the Wikipedia REST/action APIs return ~2-10 KB of metadata you don't need, and pulling that into context is wasteful and noisy. The pipe collapses everything to the minimum useful signal.

```bash
curl -sL --max-time 6 "https://en.wikipedia.org/w/api.php?action=query&generator=random&grnnamespace=0&grnlimit=1&prop=extracts|info&exintro&explaintext&exchars=700&inprop=url&format=json" \
  | python3 -c "import json,sys; p=next(iter(json.load(sys.stdin)['query']['pages'].values())); print(p.get('title','')); print(p.get('fullurl','')); print(p.get('extract','').replace(chr(10),' ').strip()[:700])"
```

What the flags do, briefly, so you understand what to keep vs. tweak:
- `generator=random&grnnamespace=0`: random article from the main namespace (skip talk/user/file pages).
- `prop=extracts&exintro&explaintext&exchars=700`: return only the lead section, plain text, capped at ~700 chars **at the API level**. This is the most important filter.
- `prop=info&inprop=url`: include the canonical URL.
- The `python3 -c` step extracts just `title`, `fullurl`, `extract` and prints them as three lines. Nothing else (no IDs, no revision metadata, no `pageprops`, no `continue` tokens) enters your context.

If the command fails, do **not** retry in a loop or fall back to a hard-coded list. The seed must come from this curl or from the user — **never** from your own web-search, web-fetch, or hand-picked article/number. The instant *you* choose the seed you reintroduce the exact bias this skill exists to remove, so a self-picked seed is worse than not running the skill at all; "too cumbersome for a quick question" is not an exception. So if the host is blocked (sandboxed network), stop and ask the user to open `https://en.wikipedia.org/wiki/Special:Random` and paste back the URL it lands on, then use that article as the seed. Otherwise (network down, rate-limited), say why and hard fail.

### 2. Find an oblique connection

Read the three-line output and look for a non-obvious link to the user's request. Don't pick the first connection you see. Look for:
- a **structural analogy** (the article describes a system whose shape you can borrow),
- a **vocabulary** you can repurpose (jargon, names, era-specific terms),
- a **constraint** the article suggests (one rep per constituency → "every failure has exactly one owner"),
- a **contrarian framing** (the article's domain values the *opposite* of what the user's domain values).

The further the article is from the user's domain, the better. That distance is the source of the originality.

### 3. Reason about the bridge before answering

Before composing the answer, work through these four blocks in your reasoning. The user never sees this step; producing it is what keeps the final answer coherent rather than a vague gesture toward the article.

- Wikipedia title and URL used as the seed
- 2-4 sentences on the bridge: what in the article inspired what in your answer
- One-line creative thesis for your response
- (Optional) one or two angles you considered and rejected, so the choice is deliberate not lazy

Then answer.

**Optional `--log` flag**: if the user includes `--log` in their request (or asks something equivalent like "save the seed" or "log it"), also write the four blocks to a temp file at `/tmp/be-creative/<short-slug>.md` on Unix-like systems, or `%TEMP%/be-creative/<short-slug>.md` on Windows. Mention the path in your response so they can read it before the system clears temp on next reboot. Without the flag, no file is written.

### 4. Answer the user's actual request, precisely

This is the part that matters most. **Creativity is not an excuse to miss the brief.** The answer must do exactly what the user asked, just via a more "tiré par les cheveux" route than a default response would have taken. The Wikipedia seed is a lens, not a topic to drag in. If the user asked for a function name, give them a function name. One that happens to be unusually good *because* you let an unrelated article rearrange your priors.

### 5. Stay transparent in tone

Do not announce the skill. Do not name-drop the Wikipedia article. Do not explain the process to the user unless they ask. They get a clean, original-feeling answer. If they later ask "wait, where did that come from?", *then* explain: name the article and walk them through the bridge.

## Why the random seed matters

Asking an LLM to "be creative" without a stimulus tends to produce the *average* of creative-sounding outputs: the same metaphors, the same whimsical tone, the same three structural moves. An unrelated real-world artifact breaks that average. It forces a specific, particular constraint that no template would have suggested. That specificity is what makes the result feel genuinely original instead of generically "creative".

The article does not need to be a *good* match. A bad match is often better. The further the leap, the more the result looks like a thought a human would have, rather than a thought a model would have.

## What to avoid

- **Don't shoehorn the article in.** If the only way to use it is to literally mention it, you have failed the brief. The article is a *prior shifter*, not a topic. The names/ideas/phrasing in your final answer should not point back at the seed. A reader looking only at the answer should have no way to guess what the seed was.
- **Don't sacrifice precision for whimsy.** A creative answer that doesn't solve the user's problem is worse than a boring one that does.
- **Don't skip the structured reasoning.** Generating those four blocks is what forces you to commit to the bridge between article and answer. That's what makes the output coherent rather than scattered.
- **Don't widen the curl filter.** If you find yourself wanting more context from Wikipedia, you're probably trying to make the article fit too literally. Step back and re-read the three lines you have.
- **Don't explain the trick in the answer.** Transparency about *process* belongs in the reasoning, not the response. The answer itself should just feel sharp.

## Example flow

User: *"Give me a name for an internal tool that watches CI pipelines and pings the right person when something breaks."*

- Run the curl. Output (3 lines):
  ```
  10th Kwara State House of Assembly
  https://en.wikipedia.org/wiki/10th_Kwara_State_House_of_Assembly
  The 10th Kwara State House of Assembly is the legislative branch of the Kwara State Government, inaugurated on June 13, 2023. The assembly is unicameral with 24 representatives elected from constituencies across the state. The incumbent Speaker is Rt. Hon Salihu Yakubu-Danladi... Bills must be endorsed by a two-thirds majority of the house before being presented to the Governor for assent...
  ```
- Reasoning: the useful structure here isn't "legislature", it's *constituency-based representation*. 24 territories, each with exactly one member responsible for it. That's a sharper mental model for "ping the right person" than on-call rotation: failures don't get *assigned*, they *belong* to a district by birth, and the tool's real job is maintaining the map. Considered and rejected: `Speaker`, `Gavel`, they evoke calling-to-order and turn-taking, which is the wrong half of parliament for this problem. Thesis: the name should imply a map of jurisdictions, not a notifier or a siren.
- Answer to user: a tight list, `Riding`, `Precinct`, `Ward`, `Bailiwick`, plus 2-3 more in the same vein, each with a one-line rationale tied to *territorial ownership of failure*, not to parliament.

The user gets exactly what they asked for (names with rationales) but the candidate set sits in a vocabulary (territorial jurisdictions with a single responsible figure) that a default response would not have surfaced. None of the names point back at the seed; if asked, you can explain the bridge, but unprompted the answer just lands as unexpectedly sharp.
