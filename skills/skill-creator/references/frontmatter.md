# Agent Skills frontmatter — full reference

Every field defined by the [open Agent Skills specification](https://agentskills.io/specification) and by the [Claude Code skills extension](https://code.claude.com/docs/en/skills). Use this when authoring a SKILL.md and you need to know exactly what a field does, what its constraints are, and whether it's portable.

`SKILL.md` is a single file: YAML frontmatter (between `---` delimiters) followed by Markdown body. The frontmatter controls *whether and how* the skill activates; the body is what runs once it does.

The default mindset: write for any spec-compliant agent (Claude Code, OpenCode, Codex CLI, Pi, …). Portable fields go first. CC-only fields are additive enhancements — they degrade gracefully on other tools because unknown fields are ignored.

---

## Portable fields (open spec)

Part of agentskills.io. Work on every spec-compliant tool. Stick to these whenever possible.

### `name` — required

- **Type**: string (kebab-case identifier)
- **Length**: 1–64 characters
- **Format**: lowercase `a-z`, digits `0-9`, hyphens `-`. No leading or trailing hyphen. No consecutive hyphens.
- **Constraint**: MUST equal the parent directory name (e.g. `skills/<name>/SKILL.md`).
- **Behavior**: The skill's identifier. Becomes the slash trigger (`/<name>`) on tools that expose one. Codex and OpenCode reject SKILL.md files where `name` doesn't match the directory.

Example: `name: pdf-processing`

### `description` — required

- **Type**: string
- **Length**: 1–1024 characters (open spec). Claude Code caps the combined `description` + `when_to_use` block shown in the skill picker at ~1,536 chars.
- **Behavior**: The single most important field. On tools that auto-invoke skills, this is the only metadata always loaded into the agent's context — if it doesn't include the natural-language phrases the user would type, the skill never triggers. State *what* the skill does AND *when* to use it.
- **Note**: When `disable-model-invocation: true` is also set (Claude Code), the description is NOT loaded into context — only the directory listing shows it.

### `license` — optional

- **Type**: string (license name or filename reference)
- **Behavior**: Documentation of the skill's license. No runtime effect.

Example: `license: Apache-2.0`

### `compatibility` — optional

- **Type**: string
- **Length**: 1–500 characters if provided
- **Behavior**: Free-text description of environment requirements (intended product, required system packages, network access, etc.). Most skills don't need this.

Example: `compatibility: Requires Python 3.14+ and uv`

### `metadata` — optional

- **Type**: map of string keys to string values
- **Behavior**: Arbitrary metadata for clients. The spec recommends namespacing keys to avoid conflicts.

Example:
```yaml
metadata:
  author: example-org
  version: "1.0"
```

### `allowed-tools` — optional (experimental in the open spec)

- **Type**: space-separated string OR YAML list
- **Behavior**: Pre-approved tools the skill may use. Support varies across tools. In Claude Code, lets the skill call listed tools without per-use permission prompts while active. Permission settings still govern tools that are not listed.

Example: `allowed-tools: Bash(git:*) Read Grep`

---

## Claude Code-specific extensions

CC-only. Don't break portability — other tools ignore unknown fields. Treat as additive enhancements.

### `argument-hint` — optional

- **Type**: string
- **Behavior**: Shown in CC's autocomplete picker when the user types `/<name> `. Use `[brackets]` for optional args, `<angles>` for required.
- **Portability**: Other tools ignore it. Safe to use.

Example: `argument-hint: "[focus question — optional]"`

### `disable-model-invocation` — optional

- **Type**: boolean
- **Default**: `false`
- **Behavior**: Set to `true` to prevent the agent from auto-invoking the skill via description match. The user can still invoke `/<name>` manually. Description is not loaded into context until manual invocation. Also prevents the skill from being preloaded into subagents.
- **Portability**: CC-only. Other tools ignore the field and continue to auto-invoke based on the description — so a description with broad trigger phrases will still fire spuriously on other platforms. Either keep the description narrow, or accept the asymmetry.
- **Use for**: opt-in stance changes, deploy-style workflows with side effects, anything that should fire only on explicit request.

### `when_to_use` — optional

- **Type**: string
- **Behavior**: Extra natural-language triggers appended to `description` for invocation matching. Counts toward the ~1,536-character picker cap.
- **Portability**: CC-only. Not portable — other tools don't read it. Prefer putting triggers in `description` if you care about cross-tool behavior.

### `arguments` — optional

- **Type**: space-separated string OR YAML list
- **Behavior**: Named positional arguments that fill `$name` substitutions in the body. Maps to positions in order.
- **Portability**: CC-only. Not portable — substitutions don't expand on other tools, so the body becomes literal `$name` text elsewhere.

### `user-invocable` — optional

- **Type**: boolean
- **Default**: `true`
- **Behavior**: Set to `false` to hide the skill from the `/` menu. Use for background-knowledge skills that aren't meaningful as user commands. Note: this only controls menu visibility, not Skill-tool access — use `disable-model-invocation: true` to block programmatic invocation.
- **Portability**: CC-only.

### `disallowed-tools` — optional

- **Type**: space- or comma-separated string OR YAML list
- **Behavior**: Tools removed from the agent's pool while this skill is active. Restriction clears on the next user message.
- **Portability**: CC-only.

### `model` — optional

- **Type**: model identifier or `inherit`
- **Behavior**: Overrides the session model while the skill is active. Override applies for the rest of the current turn; session model resumes on the next prompt.
- **Portability**: CC-only.

### `effort` — optional

- **Type**: `low` | `medium` | `high` | `xhigh` | `max`
- **Behavior**: Overrides session effort level while the skill is active. Available levels depend on the model.
- **Portability**: CC-only.

### `context` — optional

- **Type**: `fork`
- **Behavior**: Set to `fork` to run the skill in a forked subagent context.
- **Portability**: CC-only.

### `agent` — optional

- **Type**: subagent type identifier
- **Behavior**: Which subagent type to use when `context: fork`.
- **Portability**: CC-only.

### `hooks` — optional

- **Type**: map (see CC's [hooks-in-skills docs](https://code.claude.com/docs/en/hooks#hooks-in-skills-and-agents))
- **Behavior**: Hooks scoped to this skill's lifecycle.
- **Portability**: CC-only.

### `paths` — optional

- **Type**: comma-separated string OR YAML list of glob patterns
- **Behavior**: Limits auto-invocation to sessions where files matching the patterns are in scope. Same format as path-specific rules in CC memory.
- **Portability**: CC-only.

### `shell` — optional

- **Type**: `bash` (default) | `powershell`
- **Behavior**: Shell to use for `` !`command` `` and ` ```! ` blocks. PowerShell requires `CLAUDE_CODE_USE_POWERSHELL_TOOL=1`.
- **Portability**: CC-only.

---

## Invocation control — visibility matrix

For CC. Combines `disable-model-invocation` and `user-invocable`:

| Frontmatter                       | Agent can invoke | User can invoke | Description in context |
|-----------------------------------|------------------|-----------------|------------------------|
| (default)                         | Yes              | Yes             | Yes — full skill loads when invoked |
| `disable-model-invocation: true`  | No               | Yes             | No — loads only when user invokes |
| `user-invocable: false`           | Yes              | No              | Yes — full skill loads when invoked |
| Both `true` / `false` set         | No               | No              | (Skill is effectively dead — avoid) |

---

## Example: portable skill with CC enhancements

```yaml
---
name: scorched-earth-mode
description: Manual-only opt-in stance for projects still iterating...
disable-model-invocation: true
argument-hint: "[on | off — defaults to on]"
---
```

Works in every spec-compliant tool. In Claude Code, `disable-model-invocation: true` enforces the manual gate and `argument-hint` polishes autocomplete. Other tools ignore those two fields and route the skill through their normal description-based auto-invocation.

---

## Validation

- Open spec: [`skills-ref validate`](https://github.com/agentskills/agentskills/tree/main/skills-ref).
- This repo: `./scripts/validate-skills` (enforces name format, name-matches-directory, description length, single SKILL.md per directory, mirror-symlink invariants).

---

## Sources

- [agentskills.io/specification](https://agentskills.io/specification) — the open spec.
- [code.claude.com/docs/en/skills](https://code.claude.com/docs/en/skills) — Claude Code extensions (Frontmatter reference, Control who invokes a skill).
