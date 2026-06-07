---
name: mvk
description: Research any field to "level-1 enthusiast lurker" depth and deliver it as a self-contained, interactive HTML mini-site — the culture (history, key people, industry players, beloved brands, dramas, lingo, memes) plus, when the field has gear, how to buy in (what to check, differentiating criteria, price tiers). Use when the user types /mvk or wants to quickly get into, understand, or sound like they follow a hobby, scene, or field — "give me the rundown on X", "I want to get into X", "minimal viable knowledge", "what should I know before buying X". Runs a short multiple-choice quiz to fix direction first, then community-tuned web research.
argument-hint: "[subject to learn — optional]"
disable-model-invocation: true
---

# mvk — Minimal Viable Knowledge

Take the user from zero to **level-1 enthusiast lurker** on any field — the person who's read the subreddit for a year. They know the rough history, the key people, the industry players, the beloved brands, and the dramas: superficially, but fluently. And if the field has gear, they know how to **choose what to buy** — what to check on a spec sheet, the differentiating criteria, and which tier (cheap / bang-for-buck / semi-pro / luxury) fits them.

The deliverable is a single self-contained, interactive **HTML mini-site** the user keeps and browses — not a chat answer, not a markdown doc.

## Flow

1. **QCM first — always, before any research.** Ask a few quick multiple-choice questions to fix two things: the user's **motive** (to buy gear / to hold a conversation / to start doing it / pure curiosity) and the exact **slice** of the field (narrow broad topics — "photography" → film vs digital vs phone). Use the harness's question widget if it has one. Don't ask their level or how deep — the level is fixed at "lurker."
2. **Research** the field, community-tuned (below).
3. **Build** the HTML site, save it in the working dir, and tell the user the path.

## Research

Search where lurkers actually learn — Reddit, dedicated forums, YouTube, enthusiast blogs, "best X of <year>" roundups. You're capturing **vibe, consensus, and drama** — who and what the community loves and mocks, the recurring arguments, the canon — not fact-checking.

- **Buying info must be current and dated** ("as of <year>"); best-pick lists and prices go stale fast. Culture (history, people, debates, memes) is evergreen — gather it without recency pressure.
- Collect **real URLs** (communities, key videos, product pages) and **image URLs** as you go — the site links to and shows them. Expect some link rot.

## The report

A fixed, complete site — every section present at full lurker depth, organized as **tabs**. **Motive never cuts content**; it only sets the intro framing and suggests which tab to open first. The user self-navigates.

Baseline sections (add whatever a given field clearly needs; drop only the buying tab when there's nothing to buy):

- **History** — the minimal timeline that explains how the field got here.
- **Key people** — who matters and why, a sentence each.
- **Industry players** — the companies and orgs that shape it.
- **Beloved brands** — what the community swears by, and the reputations.
- **Dramas** — the controversies and scandals everyone references.
- **Buying guide** *(only if the field has gear)* — what to check, the differentiating criteria, spec-sheet literacy, and the cheap / bang-for-buck / semi-pro / luxury tiers.
- **Lingo / glossary** — the jargon and slang, decoded.
- **Where the scene lives** — the subs, forums, channels, podcasts to lurk next.
- **Eternal debates** — the recurring flame wars and tribal divides.
- **Memes & inside jokes** — the running gags and "iykyk" references.

**Voice: neutral explainer.** Teach clearly and even-handedly ("some swear by X, others by Y"). Slang lives in the glossary, humor in the memes tab — don't narrate in-character.

## The site

One self-contained `.html` file — inline CSS/JS, no build step, opens by double-click. Make it **interactive, visual, and andragogical** — built to actually teach an adult, not just to be read:

- **Tabbed** navigation between sections.
- **Collapsible TL;DRs** — each section a one-liner that expands to the full detail (skim by default).
- A **sortable / filterable comparison table** for the buying guide (filter by tier, sort by price, flag the spec that matters).
- A **self-quiz / flashcards** over the lingo, people, and debates ("are you lurker-fluent yet?").
- **Image galleries** and **clickable link cards** for communities and sources.
- **Visual aids wherever they help** — timelines, a landscape map of the players, brand family trees, price-vs-tier charts. Invent the ones that fit the field; this list is a floor, not a ceiling.

Make it look like a real little website, not a worksheet. Be creative.

## Anti-patterns

- ❌ Skipping the QCM and researching on assumptions.
- ❌ Shipping a markdown report or a chat summary instead of the HTML file.
- ❌ Cutting sections based on motive — motive only reframes.
- ❌ Narrating in heavy in-group slang — that's what the glossary and memes tabs are for.
- ❌ Stale, undated buying advice.
- ❌ Fact-check rabbit holes — this is lurker-level cultural fluency, not journalism.
