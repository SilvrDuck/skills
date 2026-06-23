---
name: skill-creator
description: Author or revise a portable Agent Skill (SKILL.md) that works across Claude Code, OpenCode, Codex CLI, and Pi. Use when creating a new skill, scaffolding a SKILL.md, editing an existing skill's frontmatter or body, reviewing a skill for portability, or whenever the user asks to "make this a skill", "create a skill", "write a SKILL.md", or is about to add a directory under skills/ or plugins/<plugin>/skills/. Be pushy — call this skill any time skill creation is on the table, even if the user hasn't named it explicitly.
argument-hint: "[skill name — optional]"
---

# skill-creator

Author or revise a portable Agent Skill that works in Claude Code, OpenCode, Codex CLI, and Pi from a single source.

The open spec is at [agentskills.io/specification](https://agentskills.io/specification). This skill distills only the authoring parts — the rules that, if you get them right, make the skill work everywhere on the first try.

## Default audience: any agent, not just Claude

Write skills assuming the user is **not** on Claude. Use generic terms in the body — "the agent", "the LLM", "the harness" — not "Claude" or "Claude Code". Stick to the [open spec](https://agentskills.io/specification) for fields and conventions so the skill works on OpenCode, Codex CLI, Pi, and anything else that adopts the standard. Claude Code-only fields (`disable-model-invocation`, `argument-hint`, …) are fine as *additive enhancements* — they make the skill better in CC but degrade gracefully because other tools ignore unknown fields. Reach for them when CC users specifically benefit; don't make them load-bearing. The full field list (portable + CC-only) is in [`references/frontmatter.md`](references/frontmatter.md).

## Before scaffolding — ask for the name

For new skills, don't pick the name yourself. Ask the user for the kebab-case slug (= directory name = `/<name>` trigger) before running `new-skill` or drafting anything. Skip only if they already said it.

## Scaffold a new skill

From this repo's root:

```bash
./skills/skill-creator/scripts/new-skill <kebab-name>
```

Creates `skills/<kebab-name>/SKILL.md` with valid frontmatter and a placeholder body. Validates the name. Then edit the description (the most important field), fill the body, run the validator, done.

## Frontmatter — only two required fields

```yaml
---
name: <kebab-case, matches the parent directory>
description: <what + when + natural triggers, 10–1024 chars>
---
```

- `name`: lowercase `a-z 0-9 -`, 1–64 chars, no leading/trailing hyphen, no consecutive `--`. **MUST equal the parent directory name** — Codex and OpenCode reject mismatches; the repo's validator enforces it.
- `description`: 10–1024 chars. See the next section — this is the only field always in context, so it IS the trigger.

Optional fields (skip unless you have a reason): `license`, `compatibility`, `metadata`, `allowed-tools`. Behavior-changing CC-only fields (`when_to_use`, `arguments`, …) make the skill non-portable — avoid unless CC-only.

Exception worth using proactively: **`argument-hint`** — shows in Claude Code's autocomplete picker. Add whenever the skill takes an argument. Wrap each argument in square brackets; space-separate multiple (`[from] [to]`); show mutually-exclusive choices with `|` inside one bracket (`[on | off]`); append `— optional` to any argument the user can omit. Never angle brackets — the CC docs use square brackets for every argument. Example: `argument-hint: "[focus question — optional]"`. Other tools ignore it, so it's portability-safe.

Exception worth knowing: **`disable-model-invocation: true`** — the hard toggle that turns off auto-invocation. Claude can no longer trigger the skill from the description; only the user can invoke it via `/<name>`. The description isn't even loaded into context unless someone invokes it. Use for opt-in stance changes, high-stakes workflows, or anything that should sit behind an explicit gate so it doesn't fire on every loosely-related mention. Claude Code only — other tools ignore the field and fall back to normal auto-invocation, so the skill still works everywhere; only CC honors the gate. Source: [Claude Code skills docs](https://code.claude.com/docs/en/skills) ("Frontmatter reference" / "Control who invokes a skill").

## The description IS the trigger

The description is the only thing always loaded into the agent's context. If it doesn't contain the words a user would naturally say, the skill never activates. Vague descriptions are the #1 cause of dead skills.

**Anatomy:** `<one-line what>. Use when <triggers, contexts, natural phrases the user would say>.`

```yaml
# Vague — no triggers, no when
description: Helps with PDFs.

# Workflow summary — the agent may follow this and skip reading the body
description: Use when extracting text — first parse, then OCR, then merge.

# What + when + natural triggers
description: Extract text and tables from PDFs and fill PDF forms. Use when the user mentions PDFs, forms, document extraction, or asks to "read this PDF".
```

Rules:

1. **State what AND when.** What the skill does AND the conditions/keywords that should activate it. Not just one.
2. **Use natural keywords** the user would actually type, not internal jargon. ("tests are flaky", not "non-deterministic assertion timing").
3. **Be pushy.** Skills undertrigger by default. Add a phrase like *"call this skill any time the user mentions X, even if they don't ask for it"*. This measurably helps.
4. **Don't summarize the workflow.** Procedure belongs in the body. A description that lists steps becomes a shortcut the agent takes instead of reading the body.
5. **Front-load the important triggers.** Long descriptions can be truncated by some tools (Claude Code caps the combined description block at ~1,536 chars).
6. **Third person, "Use when…" opener.** Works across every target tool.

Iterate: too often → tighten triggers; too rarely → add more natural phrases.

## Body structure

The body loads on activation and stays in context for the rest of the session. Every line is a recurring token cost — and not just money. Past ~3K tokens or a few dozen distinct directives, agents follow instructions measurably *worse*, and an over-stuffed skill can leave the agent worse off than with no skill at all. Evidence + citations: [`references/context-budget.md`](references/context-budget.md).

Targets:

- ≤500 lines, ideally <300.
- ≤5,000 tokens when activated — fewer is better; degradation is measurable from ~3K.
- **Few distinct directives.** Every "always/never/must" competes for adherence; pile them on and each one is followed less. Cut rules the agent doesn't need.
- **Front-load the load-bearing rule.** Models attend to the start and end and lose the middle — put the one rule that must not be missed near the top, not buried.
- **High-signal, not shortest.** Don't compress into generic stubs (that propagates errors); aim for the smallest *sufficient* set, not the fewest words.
- Imperative voice. Standing instructions, not narration ("Always prefer X", not "I usually do X").

A reasonable shape:

```markdown
# <skill-name>

<2-sentence intro: what the skill is for.>

## Quick reference

<the smallest table or list a returning user needs>

## <the technique / rules / steps>

<smallest correct subset of content>

## Anti-patterns

- <one-liner>
```

What NOT to put in the body:

- Long reference material — split it to `references/`.
- A story about how you solved this once — skills are reusable techniques, not narratives.
- Trigger info — only the description is consulted for activation. Body triggers are dead weight.
- Five examples in five languages — one excellent example beats five mediocre ones.

## Editing an existing skill

Match the addition's weight to the rule's weight. A new field gets a sentence, not a section; a new heuristic gets a bullet, not a checklist. Prefer extending the nearest existing list to spawning a new H2. If your edit doubles the file size for one concept, it's wrong — cut it down.

## Splitting into references / scripts / assets

| Folder | Use for | Loaded |
|---|---|---|
| `references/` | Long-form docs the agent reads on demand | Only when SKILL.md points at them |
| `scripts/` | Deterministic operations: transforms, validation, scaffolds | Run as commands; **never loaded into context** |
| `assets/` | Static files emitted into output: templates, schemas, fonts | On demand |

Rules of thumb:

- **Deterministic? → script.** Math, parsing, file generation, validation. Effectively free token-wise.
- **Knowledge consulted occasionally? → reference.** Reference it explicitly from SKILL.md so the agent knows to open it.
- **Embedded in the output? → asset.**
- Keep references one level deep — don't chain `references/A.md → references/B.md → …`.
- For references >300 lines, include a table of contents at the top.

## Validate

This repo ships a validator:

```bash
./scripts/validate-skills
```

It enforces: required frontmatter, `name` matches directory, description 10–1024 chars, single SKILL.md per directory, and the multi-tool symlink invariants. CI runs the same script on every push.

Run it before committing.

## Cross-tool portability

To stay in the portable Claude Code / OpenCode / Codex / Pi subset:

- Avoid CC-only frontmatter whose effect depends on the *body* (`arguments` + `$name` substitution, `when_to_use` to carry triggers your `description` lacks). Additive CC-only fields whose absence only loses polish (`argument-hint`, `disable-model-invocation`) are fine — other tools ignore them, the rest of the skill still works.
- Don't use CC substitutions (`$ARGUMENTS`, `$N`, `${CLAUDE_PLUGIN_ROOT}`) in bodies — they don't expand elsewhere.
- Don't depend on plugin-only features (hooks, MCP servers, LSP servers) unless documented as CC-only.
- Use paths relative to `SKILL.md` when referencing bundled files.

If a skill genuinely needs CC-only features to function, say so in the description: *"Claude Code only — uses hooks."*

## Authoring checklist

- [ ] For new skills: asked the user what command/name they want before scaffolding.
- [ ] Directory name matches frontmatter `name` exactly.
- [ ] Description: states what AND when, includes natural trigger keywords, no workflow summary, pushy where useful.
- [ ] If the skill takes an argument, `argument-hint` is set: square brackets per arg, space-separated for multiple, `|` for choices, `— optional` on omittable args — never angle brackets.
- [ ] Body ≤500 lines, ≤5,000 tokens activated.
- [ ] Heavy reference content split to `references/` (and explicitly linked from SKILL.md).
- [ ] Deterministic operations split to `scripts/`.
- [ ] One excellent example, not five mediocre ones in different languages.
- [ ] Body uses generic agent terms ("the agent", "the LLM"), not Claude-specific names.
- [ ] No body-breaking CC-only features (`$ARGUMENTS`, hooks, MCP, `$N`) unless the skill is CC-only. Additive frontmatter fields (`argument-hint`, `disable-model-invocation`) are fine.
- [ ] `./scripts/validate-skills` passes.

## See also

- [`references/frontmatter.md`](references/frontmatter.md) — full frontmatter field reference (portable + CC-only).
- [`references/context-budget.md`](references/context-budget.md) — why skills must stay lean (the research, with citations).
- Open spec: <https://agentskills.io/specification>
- Anthropic's official `skill-creator` (gold-standard authoring reference): <https://github.com/anthropics/skills/tree/main/skills/skill-creator>
- Anthropic's official skill repo (exemplars): <https://github.com/anthropics/skills>
- Claude Code skills guide: <https://code.claude.com/docs/en/skills>
