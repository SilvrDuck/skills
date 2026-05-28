---
name: conventional-git
description: Use when writing a commit message or naming a new git branch in a project that follows Conventional Commits or Conventional Branches. Triggers on phrases like "commit this", "make a PR", "new branch", "what should I call this branch", or when about to run `git commit` / `git checkout -b` / `git switch -c` and the project's convention is unclear. Distills conventionalcommits.org and conventional-branch.github.io into the minimum a competent dev needs, plus the local `spike/` convention for throwaway research branches with no merge intent.
---

# Conventional Git

Cheat sheet for [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/) and [Conventional Branch](https://conventional-branch.github.io/). You already know the spirit; this is the minimum to be clean.

Before applying, confirm the project actually uses these conventions — check recent `git log` and the contributing guide. If the repo uses a different style (e.g. plain `<scope>: <description>` without type prefix), follow that instead.

## Commits

Format: `<type>(<optional-scope>): <description>`

Types — pick the most specific that fits:
- `feat` — new feature (user-visible)
- `fix` — bug fix
- `docs` — docs-only change
- `style` — formatting, whitespace, semicolons — no code-behavior change
- `refactor` — restructure without changing behavior
- `perf` — performance improvement
- `test` — add or fix tests
- `build` — build system, dependencies, packaging
- `ci` — CI config and scripts
- `chore` — anything else that doesn't ship to users
- `revert` — reverts a prior commit (body: `Refs: <sha>`)

Rules that matter:
- Description: imperative mood, lowercase, no trailing period — `add X`, not `Added X.`.
- Breaking change: append `!` after the type/scope (`feat(api)!: drop /v1`) **and/or** add a `BREAKING CHANGE: <what broke>` footer. Either signals breakage; using both is fine and common.
- Body and footers: blank line between subject, body, and the footer block. Footers use `Token: value` or `Token #ref` (e.g. `Refs: #123`, `Reviewed-by: Alice`). `BREAKING CHANGE` is the only footer token allowed to contain a space.
- Scope is optional but cheap — name the area touched (`feat(auth):`, `fix(parser):`).

## Branches

Format: `<type>/<short-kebab-description>`

Types:
- `feature/` — new user-visible feature
- `bugfix/` — non-urgent bug fix
- `hotfix/` — urgent prod fix, usually branched off `main`/`release`
- `release/` — release prep (`release/1.4.0`)
- `chore/` — non-user-facing maintenance
- `spike/` — **local addition, not in the upstream spec**: research, exploration, or proof-of-concept with **no intent to merge**. Throwaway by default. Use this when you're answering a question, not shipping the answer — keeps the PR list honest about what's actually going to ship.

Rules:
- Description: lowercase, kebab-case, no spaces or special characters. Optional trailing `-<issue>` (e.g. `feature/login-flow-123`).
- Keep it short. The branch name is a handle, not a changelog.

## Picking the right thing fast

- Touches user-visible behavior? → `feat` / `feature/`
- Closes a ticket marked as a bug? → `fix` / `bugfix/`
- Production is on fire right now? → `hotfix/`
- Just trying something to learn? → `spike/` (and don't open a PR)
- None of the above, not user-facing? → `chore`
