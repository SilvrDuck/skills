---
name: align-check
description: Use whenever the agent is about to emit any ASCII or Unicode block where characters must line up — boxes, tables, trees, columns, banners, aligned comments, terminal diagrams. Be pushy: auto-invoke proactively any time vertical alignment could matter, even if the user never asked.
---

# align-check

You count tokens, not terminal columns, so hand-aligned layout drifts, especially
once a glyph is wider than one cell. Never trust visual inspection. After producing
any aligned block, verify it before presenting it.

## Use

1. Pipe the block into the checker, naming the marker that must line up (the wall
   char, a gutter, a separator). Paths are relative to this skill's directory:

       python3 scripts/align-check.py '│' < block.txt

   On Windows use `python` or the `py` launcher in place of `python3`.

2. Read the result:
   - `OK` (exit 0): the symbol is at identical display columns on every line. Present it.
   - `DRIFT` (exit 1): the report lists each column signature and the lines that
     produced it. Fix padding on the outlier lines only, then re-run until `OK`.

3. Present only after `OK`. Check each wall separately (`║`, then `│`, etc.).

## What it measures

Per line it records the display column of every occurrence of the symbol, in order,
as one signature (e.g. `1,40`), then groups lines by signature; more than one group
is drift. Widths follow Unicode: Wide/Fullwidth and emoji count as 2, the FE0F
selector widens its base (`▶️`), combining marks and ZWJ count as 0. To check only
one occurrence (e.g. the right wall), change the `key = ",".join(...)` line to
`key = str(sig[-1])`.

## The one rule that prevents most drift

A right wall is the only thing that must be padded to match content width, so it is
where drift shows. The simplest fix is to not draw one: use an open frame with a
left gutter only. Then a variable-width column has nothing downstream to push, and
it renders the same whether a glyph is scored 1 cell or 2.

If you do want a closed box, keep terminal-decided glyphs out of walled columns:
`✔ ✘ ⚠` and similar dingbats are spec-width-1 but some terminals render them as
2-cell emoji, so they pass the checker yet still look off. Use unambiguous emoji
(`✅ ⚠️ ❌`, `🟢 🟡 🔴`) or plain ASCII (`+ - x`) for status instead; both the
checker and the terminal agree on those. Avoid ZWJ clusters (`👨‍👩‍👧`, flags,
skin tones) in aligned regions entirely.
