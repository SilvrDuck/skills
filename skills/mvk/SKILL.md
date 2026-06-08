---
name: mvk
description: Research any field to "level-1 enthusiast lurker" depth and deliver it as a self-contained, interactive HTML mini-site — the culture (history, key people, industry players, beloved brands, dramas, lingo, memes) plus, when the field has gear, how to read a spec sheet (which specs and criteria actually matter, and how much you need). Use when the user types /mvk or wants to quickly get into, understand, or sound like they follow a hobby, scene, or field — "give me the rundown on X", "I want to get into X", "minimal viable knowledge", "what should I know before buying X". Runs a short multiple-choice quiz to fix direction first, then community-tuned web research.
argument-hint: "[subject to learn — optional]"
disable-model-invocation: true
---

# mvk — Minimal Viable Knowledge

Take the user from zero to **level-1 enthusiast lurker** on any field — the person who's read the subreddit for a year. They know the rough history, the key people, the industry players, the beloved brands, and the dramas: superficially, but fluently. And if the field has gear, they can **read a spec sheet** — they know which specs and criteria actually matter, what each one means, and how much of each they need for their use, so they can size up *any* product instead of picking from someone's list.

**The bar:** the report succeeds only if the reader can (1) hold their own in a conversation with an aficionado, and (2) walk into a shop and confidently pick the right thing *for their goal that day* — both without looking anything up. Every section earns its place by serving one of those two.

The deliverable is a single self-contained, interactive **HTML mini-site** the user keeps and browses — not a chat answer, not a markdown doc.

## Flow

1. **QCM first — always, before any research.** Ask a few quick multiple-choice questions to fix two things: the user's **motive** (to buy gear / to hold a conversation / to start doing it / pure curiosity) and the exact **slice** of the field (narrow broad topics — "photography" → film vs digital vs phone). Use the harness's question widget if it has one. Don't ask their level or how deep — the level is fixed at "lurker."
2. **Research** the field, community-tuned (below).
3. **Build** the HTML site, save it to `/tmp` (fall back to the working dir if `/tmp` isn't writable), and tell the user the full path.

## Research

Search where lurkers actually learn — Reddit, dedicated forums, YouTube, enthusiast blogs, "best X of <year>" roundups. You're capturing **vibe, consensus, and drama** — who and what the community loves and mocks, the recurring arguments, the canon — not fact-checking.

- **Buying info must be current and dated** ("as of <year>"); best-pick lists and prices go stale fast. Culture (history, people, debates, memes) is evergreen — gather it without recency pressure.
- Collect **real URLs as you go** — communities, key videos, product pages, and **images**. For images: only keep a URL you have **opened and confirmed returns an actual image** — **never guess or construct one from memory** (invented paths 404, which is why images come back as empty alt-text boxes). For Wikipedia/Wikimedia photos use `https://commons.wikimedia.org/wiki/Special:FilePath/<exact filename>?width=800` — it resolves from the filename alone, with no guessable hash path. Expect some link rot.

## The report

A fixed, complete site — every section present at full lurker depth, organized as **tabs**. **Motive never cuts content**; it only sets the intro framing and suggests which tab to open first. The user self-navigates.

Baseline sections (add whatever a given field clearly needs; drop only the buying tab when there's nothing to buy):

- **History** — the minimal timeline that explains how the field got here.
- **Key people** — who matters and why, a sentence each.
- **Industry players** — the companies and orgs that shape it.
- **Beloved brands** — what the community swears by, and the reputations.
- **Dramas** — the controversies and scandals everyone references.
- **Buying guide** *(only if the field has gear)* — **teach how to read a spec sheet, not what to buy.** For each kind of thing one buys: what it is in plain terms, the few specs/criteria that actually matter and what each one means, and how to judge how much (or which) you need — including where paying more stops helping. **Map the common goals to priorities** — for objective X prioritize spec A and ignore B; for Y, flip it — so the reader turns *their* intent into a confident pick. Call out the specs that separate budget from premium, and the **common traps and marketing-fluff specs** that get oversold or pushed at the counter. **Still give the community's verdict on the popular brands and products** — what's trusted, loved, mocked, or overrated, and the consensus picks — so you know the reputations walking in. Weave that sentiment into the literacy as illustration; just don't let a curated "best picks" / tier table stand in for teaching the spec sheet.
- **Lingo / glossary** — the jargon and slang, decoded.
- **Where the scene lives** — the subs, forums, channels, podcasts to lurk next.
- **Eternal debates** — the recurring flame wars and tribal divides, plus the tells that out a tourist vs a regular: what not to ask, and which takes are safe to hold.
- **Memes & inside jokes** — the running gags and "iykyk" references.

**Voice: neutral explainer.** Teach clearly and even-handedly ("some swear by X, others by Y"). Slang lives in the glossary, humor in the memes tab — don't narrate in-character.

**Cite the checkable claims.** Hard facts — rules, dates, stats, named incidents, prices/specs — carry a small **inline source link** to the page they came from, so the reader can verify or dig deeper in one click. Vibe and opinion ("purists grumble…") stay uncited. This is *sourcing* — link what you actually drew from — not fact-checking; no verification rabbit holes.

## The site

One self-contained `.html` file — inline CSS/JS, no build step, opens by double-click. Make it **interactive, visual, and andragogical** — built to actually teach an adult, not just to be read:

- **Tabbed** navigation between sections.
- **Collapsible TL;DRs** — each section a one-liner that expands to the full detail (skim by default).
- A **spec-sheet decoder** for the buying guide — each key spec laid out with what it controls, what to look for, and how much is "enough" for casual vs serious use. A comparison table fits well, but its rows are *specs and criteria*, not curated products.
- A **point-of-sale checklist** for the buying guide — the few specs to verify and questions to ask at the counter, condensed to glance at on a phone in the shop.
- A **self-quiz / flashcards** over the lingo, people, and debates ("are you lurker-fluent yet?").
- **Real images throughout — not a text wall.** Embed photos with `<img>` (people, gear, logos, iconic moments) using only the **verified** URLs from research, plus galleries and clickable link cards. You can't download files and don't need to — hotlink the remote URL. Give every `<img>` an **`onerror` fallback** so any dead link degrades to a clean captioned placeholder, never a raw alt-text box.
- **Visual aids wherever they help** — timelines, a landscape map of the players, brand family trees, spec-vs-price curves. Invent the ones that fit the field; this list is a floor, not a ceiling.

Make it look like a real little website, not a worksheet. Be creative.

## Anti-patterns

- ❌ Skipping the QCM and researching on assumptions.
- ❌ Shipping a markdown report or a chat summary instead of the HTML file.
- ❌ Cutting sections based on motive — motive only reframes.
- ❌ A curated "what to buy / best builds" table as the buying guide — teach the spec sheet so the user can size up any product; popular picks are illustration, not the deliverable.
- ❌ Guessing or constructing image URLs (especially Wikimedia `.../thumb/<hash>/...` paths) — embed only URLs you've fetched and confirmed load, or you get boxes of alt text. A text-only site is just as much a failed run.
- ❌ Stating a checkable fact (a rule, stat, date, named incident, price) with no clickable source — the reader can't trust it or dig in. Cite the hard claims; leave vibe uncited.
- ❌ Narrating in heavy in-group slang — that's what the glossary and memes tabs are for.
- ❌ Stale, undated buying advice.
- ❌ Fact-check rabbit holes — this is lurker-level cultural fluency, not journalism.
