# Contributing

This is a personal collection, so the skills here are tuned to my workflow. I won't necessarily accept PR, but feel free to use what you find here.

Issues are always welcome: broken links, outdated install commands, a skill that fails validation, or a wrong claim about how Claude Code / OpenCode / Codex / Pi consumes these. Bug-fix PRs that match an existing issue are welcome too.

## Repo invariants

- Canonical skills live at `skills/<skill>/SKILL.md` (a real directory at the repo root).
- `.agents/skills`, `.claude/skills`, and `plugins/silvrduck/skills` are symlinks pointing at `skills/`. Don't change them — they are the install surface for the non-Claude-Code tools and for the Claude Code plugin.
- Each skill directory contains exactly one `SKILL.md`. Frontmatter `name` must match the directory name. `description` must be 10–1024 characters and include when-to-use trigger language.
- Auxiliary files live in `references/`, `scripts/`, or `assets/` inside the skill directory.

## Validate

```bash
./scripts/validate-skills
```

CI runs this on every push and pull request.

## Commit style

[Conventional Commits](https://www.conventionalcommits.org/). Common types: `feat`, `fix`, `docs`, `chore`, `refactor`.
