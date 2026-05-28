---
name: handout
description: Package the current conversation into a self-contained Markdown file at the repo root so the user can paste it into a fresh LLM (ChatGPT, another Claude window, a coworker) and get useful help without any prior context. Use whenever the user types `/handout`, says "write a handoff", "I want to continue this with another LLM", "give me a brief for ChatGPT", "summarize this whole thread for someone else", or asks for a session brief / handover doc. ALSO accepts an optional argument that focuses the handout on a specific question, e.g. `/handout explain this last bug` or `/handout why isn't the auth middleware firing` — when an argument is present, structure the document around answering that for the recipient. Mention the argument form in chat when the user runs it without one. Be pushy: if the user signals they're about to leave the session or hand off, suggest `/handout` proactively.
argument-hint: "[focus question — optional]"
---

# handout

Package this conversation into a single Markdown file that a stranger — a fresh ChatGPT window, another Claude session, a coworker — can read once and immediately help with. Assume the reader has **zero** prior context: no idea what the project is, what we tried, what failed, or what the user wants next.

The output is a *handover*, not a transcript. The reader does not want to relive the chat. They want the minimum they need to be useful.

## Quick reference

| Situation | What to do |
|---|---|
| `/handout` with no argument | Write a general handover covering project + session state + open thread, save to `HANDOUT.md` at repo root |
| `/handout <question>` | Same primer, but structure the body around answering or unblocking that specific question; save to `HANDOUT-<slug>.md` |
| User wants a different path/name | Honour it. The default is just a default. |
| Repo root not obvious (no git, multiple roots) | Save next to the file most relevant to the discussion; tell the user where |
| Conversation has been compressed / very long | Read `git log`, `git diff`, and recently-touched files to reconstruct missing facts before writing |

After writing, print the absolute path and a one-line hint reminding the user that `/handout <topic>` focuses the doc on a question.

## What goes in the document

A good handout has five sections, in this order. Cut any that are genuinely empty — don't pad.

### 1. Project primer (what is this thing?)

Two to four sentences. What the project does, what stack/language, anything load-bearing the reader needs before reading any code. Pull from `README.md`, `CLAUDE.md`/`AGENTS.md`, `package.json` / `pyproject.toml` / `Cargo.toml` / etc. — don't invent.

If the conversation revealed non-obvious project context (e.g. "this is an internal fork", "we only support Python 3.11", "the prod DB is on Neon"), include it here.

### 2. What the user is trying to do

The session goal, in the user's words where possible. Not "we discussed X" — state the actual objective. If the goal evolved during the session, give the *final* version, not the original.

### 3. What's been done so far

A tight chronological-ish list of the substantive moves: files created/edited, commands run with meaningful output, decisions made, dead ends hit. Skip the chatter ("then I asked clarifying questions"). Include enough that the reader doesn't redo work that's already done.

Use file paths with line numbers when pointing at code: `src/auth/middleware.ts:42`.

### 4. Current state / the specific ask

This is the most important section.

- **With no argument:** describe where we are now and what the open thread is — "tests pass locally but CI is still red on the lint job; user is debugging".
- **With an argument:** restate the user's question/blocker as the headline, then give everything a fresh LLM needs to answer it: the failing code, the error, what was already tried, the user's hypothesis if they voiced one.

Quote real error messages, real diffs, real log output. Paraphrased errors are useless to the next model.

### 5. What would actually help

One or two sentences pointing at what the recipient should produce: "Suggest a fix for the lint rule", "Explain why this race condition happens", "Write the missing migration". If the user gave an argument, this section is basically a restatement of it as a prompt the recipient can act on.

## Style rules

- **Write for a stranger.** No "as we discussed", no "the bug you saw earlier", no "remember when…". The reader was not here.
- **Quote, don't summarize, code and errors.** Use fenced code blocks with the language tag. Truncate huge outputs with `…` and a note about what was cut.
- **One self-contained file.** Don't link to other docs unless the reader can also see them (public URLs, files committed to the repo). A link to `notes/private.md` that the reader doesn't have is worthless.
- **Be honest about uncertainty.** If something is unclear or unverified, say so: "User hasn't confirmed whether X is reproducible on main." Inventing certainty wastes the recipient's time.
- **Keep it scannable.** Headings, short paragraphs, lists. The reader will skim first, read second.

## Filename and path

- Default location: repo root (where `.git/` lives, or the working directory if no repo).
- Default filename: `HANDOUT.md`. With an argument, slugify the first ~6 words: `HANDOUT-explain-this-last-bug.md`.
- If `HANDOUT.md` already exists, **don't clobber silently** — append a numeric suffix (`HANDOUT-2.md`) or ask.
- The file is not meant to be committed by default. Don't add it to git unless asked.

## After writing

End your turn with:

1. The absolute path of the file you wrote.
2. **If the user invoked the skill with no argument**, a short hint that `/handout` accepts one — phrase it lightly:
   > Tip: `/handout <question>` focuses the doc on a specific ask, like `/handout why does this build fail on CI`.
   The frontmatter `argument-hint` already advertises this in the tool's autocomplete (e.g., Claude Code's), so the chat tip is for users who skipped autocomplete or are on a tool that doesn't show it. Once per session is enough — don't repeat it on subsequent invocations.
3. Nothing else. Don't paste the contents back into chat — the file is the artifact.

## Anti-patterns

- **Dumping the transcript.** A handout is not a chat log. Synthesize.
- **Vague primer.** "This is a web project" is worthless. Name the framework, the entry point, the thing being built.
- **Skipping the ask.** A handout with no clear "what should the next model do?" is just a status report.
- **Leaving conversation fossils** (see also: [[defossil]]). Don't write "we then realized…" — write what is true now.
- **Inventing project facts.** If you're not sure what the project does, read the README, ask, or write "unknown — see <file>" rather than guess.
- **Writing into a deep subdirectory** the user didn't ask for. Repo root is the default for a reason — it's findable.
- **Forgetting the argument hint.** When the user runs `/handout` bare, always mention the `<question>` form once. This is how they learn the feature exists.
