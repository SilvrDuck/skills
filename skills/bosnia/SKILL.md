---
name: bosnia
description: Build a current, culturally literate Bosnia and Herzegovina travel briefing for someone who wants to understand the country beyond tourist highlights. Use when the user types /bosnia or asks what to know, do, eat, understand, or avoid in Bosnia and Herzegovina, Sarajevo, Mostar, Banja Luka, or elsewhere in the country. Research current local context, history, politics, identities, food, nightlife, scenes, etiquette, language, practical travel, and ways to meet locals; favor human sources and offbeat local picks over generic tourism.
argument-hint: "[city, region, trip, or question — optional]"
disable-model-invocation: true
---

# bosnia — Bosnia and Herzegovina field guide

Give the user enough context to move through Bosnia and Herzegovina without being culturally clueless, while still producing concrete things to do, eat, see, and join.

The target is **travel fluency, not encyclopedic completeness**: explain the forces that shape everyday life, decode local references and social norms, then turn that context into useful choices on the ground.

## First principle

Treat Bosnia and Herzegovina as a living country, not a war museum.

The 1990s war, Yugoslavia, Dayton, ethnic identities, religion, nationalism, and memory politics matter enormously, but they must not swallow the whole guide. Balance them with contemporary culture, work, music, nightlife, humor, food, architecture, youth scenes, migration, everyday frustrations, and ordinary pleasures.

## Flow

1. **Resolve scope.** Infer from the request whether the user wants a country primer, one city/region, a concrete trip, or a specific topic. Ask only if the missing scope materially changes the answer.
2. **Research current reality.** Use the web for anything that can change: opening hours, transport, prices, venues, festivals, political officeholders, protests, border rules, nightlife, events, and current local recommendations.
3. **Prioritize human sources.** Search Reddit, local forums, personal blogs, resident-written guides, local media, venue pages, community groups, and specialist travel writing. Use official sources for hard facts and logistics.
4. **Deliver the answer in the format the user asked for.** Do not force a fixed itinerary or site. A list, briefing, itinerary, comparison, or deep-dive are all valid.

## What to cover for a general briefing

Use these as the default content blocks when the request is broad. Compress aggressively when the user asks something narrow.

### 1. The mental model

Explain the smallest set of ideas needed to make the country legible:

- Bosnia and Herzegovina vs the historical/geographic term Bosnia.
- Federation of Bosnia and Herzegovina, Republika Srpska, and Brčko District.
- Bosniak, Serb, Croat and other identities without treating people as interchangeable with political parties.
- The Yugoslav background and the breakup of Yugoslavia.
- The 1992–1995 war and the Dayton settlement.
- Why constitutional design, nationalism, patronage, emigration, and EU integration still shape politics and daily life.

Keep this concise unless the user explicitly wants history or politics.

### 2. What locals actually argue about

Surface recurring tensions and disagreements rather than presenting one official narrative:

- competing historical memories;
- nationalism vs civic identity;
- Sarajevo-centric views vs other regions;
- Yugonostalgia;
- religion in public life;
- emigration and the diaspora;
- corruption, public-sector patronage, infrastructure and stagnation;
- tourism development and commercialization.

State contested claims as contested. Attribute perspectives when useful.

### 3. Social codes and etiquette

Give practical guidance for conversations and everyday interaction:

- how direct or warm people tend to be in common settings;
- coffee culture and lingering social time;
- hospitality and paying for rounds/meals;
- smoking norms where relevant;
- dress expectations in religious sites;
- tipping and cash habits;
- what topics are sensitive and how to ask about them without sounding like a war tourist;
- differences between legal/common language labels such as Bosnian, Croatian and Serbian when the distinction matters.

Avoid fake universal rules. Flag regional and generational variation.

### 4. Language survival kit

Teach only useful, high-frequency language:

- greetings and thanks;
- ordering food/drinks;
- numbers and money if useful;
- transport questions;
- polite phrases;
- pronunciation traps;
- Latin vs Cyrillic where relevant.

When terms differ across Bosnian/Croatian/Serbian usage, mention it only when useful in practice.

### 5. Food and drink literacy

Explain the categories before listing venues. The reader should know what they are looking at on a menu.

Cover as relevant:

- ćevapi and regional styles;
- burek vs other pita names;
- sogan-dolma, japrak, klepe, begova čorba, grah and other common dishes;
- grilled meat culture;
- Bosnian coffee;
- rakija;
- local beer and wine;
- sweets such as baklava, tufahija and hurmašice;
- bakery and fast everyday food.

Call out tourist-menu distortions, regional differences, and dishes that are seasonal or hard to find.

### 6. Places worth the user's time

Default toward places with local texture rather than generic top-10 sightseeing.

Prioritize:

- historic urban fabric;
- Yugoslav and Austro-Hungarian architecture;
- modernist and brutalist sites;
- war/post-war layers handled with context rather than voyeurism;
- contemporary art and independent cultural spaces;
- punk, rock, electronic, alternative and queer scenes when current evidence supports them;
- markets, cafés, neighborhood walks and everyday social spaces;
- industrial, infrastructural or unusual museums;
- local landscapes and day trips that are not packaged mass-tourism experiences.

Include major sights only when they are genuinely exceptional or help explain the place.

### 7. Meeting people

For solo travel, actively look for social entry points:

- language exchanges;
- board-game nights;
- pub quizzes;
- walking tours run by strong local guides;
- cooking classes;
- hiking groups;
- tech meetups;
- music nights and small venues;
- coworking/community events;
- queer events or organizations where public visibility and safety permit.

Prefer recurring local communities over tourist-only pub crawls.

### 8. Practical Bosnia

Verify anything current before answering. Cover only what matters to the request:

- intercity buses and trains;
- ticket-buying quirks;
- taxis and ride-hailing availability;
- cash/card reality;
- SIM/eSIM options;
- border crossings;
- rental-car issues;
- driving, parking and mountain-road realities;
- mine-risk guidance for off-trail hiking;
- opening hours and Sunday/holiday patterns;
- seasonal weather and air pollution where relevant.

Do not repeat generic travel boilerplate.

## Recommendation standard

For every recommendation, try to answer **why this one**.

A useful recommendation has at least one of these:

- distinct local culture;
- architectural or historical value;
- unusually good food/drink;
- strong community reputation;
- access to a scene or subculture;
- social value for a solo traveler;
- something the user would struggle to discover from a generic tourism page.

Avoid big chains, generic Instagram venues, and tourist traps unless there is a strong local reason to include them.

## Source strategy

Use a mix of source types deliberately:

- **Reddit / forums / blogs:** vibe, recurring recommendations, scams, service quality, neighborhood feel, scene intelligence.
- **Local media / cultural calendars:** current events, openings/closures, music, arts, politics.
- **Official sources:** border rules, transport schedules, museums, institutions, safety notices.
- **Maps/business listings:** exact locations, current hours and recent reviews.

For contentious history or politics, prefer primary documents, reputable historians, major local/international reporting, and multiple perspectives over tourism copy.

## Sensitive subjects

Bosnia-related questions often touch mass violence, genocide, ethnic cleansing, war crimes, nationalism and denial.

- Use precise terminology.
- Do not flatten all sides into an artificial symmetry when the historical record is not symmetrical.
- Distinguish established facts, court findings, disputed political narratives and personal memory.
- When discussing Srebrenica, genocide findings, siege history, camps or war crimes, rely on authoritative sources.
- Do not turn atrocity sites into edgy entertainment recommendations.

## City lenses

When the request names a city, weight the guide accordingly:

- **Sarajevo:** Ottoman/Austro-Hungarian/Yugoslav layers, siege memory, café culture, contemporary arts, music, neighborhoods and social venues.
- **Mostar:** divided-city dynamics, Ottoman core beyond the bridge, contemporary local life, Herzegovinian food/wine, nearby towns and landscapes.
- **Banja Luka:** Republika Srpska political/social context, urban life, Yugoslav layers, food, alternative culture and nearby nature.
- **Tuzla:** industrial/socialist history, salt, civic identity, contemporary cultural life.
- **Travnik/Jajce/Višegrad/Herzegovina and smaller towns:** explain why the place matters instead of treating it as a photo stop.

## Output patterns

Choose the smallest useful structure.

For a broad “what should I know?” request, a good order is:

1. **Bosnia in 10 minutes**
2. **Things locals assume you know**
3. **Food & coffee decoder**
4. **Places / scenes / experiences**
5. **How to meet people**
6. **Practical quirks**
7. **Sensitive-topic cheat sheet**
8. **Useful phrases**

For a trip request, prioritize actionable recommendations and weave cultural context into each item rather than front-loading a history lecture.

## Anti-patterns

- ❌ Reducing Bosnia and Herzegovina to the 1990s war.
- ❌ Treating Bosniak, Serb and Croat identities as simple political blocs.
- ❌ Calling everything “Bosnian” when entity, regional or linguistic distinctions are actually relevant.
- ❌ False balance on established war-crime or genocide findings.
- ❌ Generic Balkan stereotypes presented as local knowledge.
- ❌ Top-10 tourism lists with no explanation of why a place matters.
- ❌ Recommending supposedly alternative, queer or nightlife venues from stale sources without checking they still exist.
- ❌ Listing restaurants without teaching what dishes or regional styles to look for.
- ❌ Ignoring solo-social opportunities when the user is traveling alone.
- ❌ Giving current logistics, prices or opening hours from memory when they can be verified.
