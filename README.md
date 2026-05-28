# silvrduck-skills

A personal [Agent Skills](https://agentskills.io) collection. Feel free to use it :)

> **Skills live in `skills/`.** Every other dir in this repo is a symlink pointing there, for compatibility with various tools.

Personal repo, issues for bugs or out-of-date info are welcome, see [CONTRIBUTING.md](CONTRIBUTING.md).

## Skills

| Skill | TLDR |
|---|---|
| [doubt](skills/doubt/SKILL.md) | Re-examine work with fresh skepticism when I push back. Assumes I don't know either. My favorite one. |
| [be-creative](skills/be-creative/SKILL.md) | Experimental skill to try to make an LLM actually creative through random wikipedia pages. |
| [defossil](skills/defossil/SKILL.md) | Strip conversation fossils, the annoying way LLMs still reference your conversation in the way they document and comment. |
| [scorched-earth-mode](skills/scorched-earth-mode/SKILL.md) | Agents are always trying to keep compatibilty with the poorly speced stuff you added at the start of the project. Ask them to be more radical in refactors. |
| [handout](skills/handout/SKILL.md) | Dump the current conversation as a self-contained Markdown brief so a fresh LLM can pick up the work. Includes project context. |
| [handcraft](skills/handcraft/SKILL.md) | For when I am tired of vibe coding. Work function by function with the agent. |
| [conventional-git](skills/conventional-git/SKILL.md) | Conventional Commits + Conventional Branches cheat sheet. |
| [ascii-diagram-renderer](skills/ascii-diagram-renderer/SKILL.md) | Avoids typical LLM ASCII diagram mistakes by using [Graph Easy](https://github.com/ironcamel/Graph-Easy) |
| [skill-creator](skills/skill-creator/SKILL.md) | Just my own tuning on your typical skill creator skill. |
| [x](skills/x/SKILL.md) | Alias for `/doubt`, because that is what you press when you have one. |

## Install

### Claude Code

```jsonc
// ~/.claude/settings.json
{
  "extraKnownMarketplaces": {
    "silvrduck-skills": {
      "source": { "source": "github", "repo": "SilvrDuck/skills" }
    }
  }
}
```

Then in Claude Code:

```text
/plugin install silvrduck@silvrduck-skills
```

### Codex CLI

```bash
codex marketplace add SilvrDuck/skills
```

Codex reads the same `.claude-plugin/marketplace.json` this repo ships for Claude Code (officially supported as the legacy-compatible path).

### Pi

```bash
pi install https://github.com/SilvrDuck/skills
```

Pi auto-discovers the top-level `skills/` directory.

### OpenCode

OpenCode has no first-party GitHub install (its `plugin` array only takes npm packages or local paths). Clone, then symlink the canonical `skills/` dir into one of OpenCode's auto-scan paths:

```bash
git clone https://github.com/SilvrDuck/skills.git ~/code/silvrduck-skills
ln -s ~/code/silvrduck-skills/skills ~/.claude/skills
```

OpenCode then auto-discovers from `~/.claude/skills`.

## Repo layout

```text
skills/                                   ← canonical (real directory)
└── <skill>/SKILL.md
.claude-plugin/marketplace.json           Claude Code + Codex CLI marketplace manifest
plugins/silvrduck/
├── .claude-plugin/plugin.json            Claude Code plugin manifest
└── skills  →  ../../skills               symlink (plugin sees skills/)
.agents/skills  →  ../skills              symlink (OpenCode, Codex, Pi scan path)
.claude/skills  →  ../skills              symlink (OpenCode, CC project scope)
```

## Validate

```bash
./scripts/validate-skills
```

Checks: required frontmatter, name matches directory, description length, no nested `SKILL.md`, the `skills/` canonical + three-symlink layout, and that every skill on disk has a row in the README skills table. CI runs the same script on every push.

## License

MIT — see [LICENSE](LICENSE).
