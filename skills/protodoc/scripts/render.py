#!/usr/bin/env python3
"""Markdown-subset renderer for protodoc review pages.

Covers what design docs actually use: headings, paragraphs, lists, tables,
blockquotes, rules, fenced code (``mermaid`` fences pass through to the client
renderer) and raw HTML blocks, which is how screen mockups are embedded.

Every top-level block becomes an addressable ``<div class="blk">`` carrying its
index and enclosing heading slug, so the shell can mark what changed since the
last snapshot and anchor annotations to a stable location.
"""
import difflib
import hashlib
import html
import re

VOID_TAGS = {
    "area", "base", "br", "col", "embed", "hr", "img", "input",
    "link", "meta", "source", "track", "wbr",
}


def block_sig(block: str) -> str:
    """Stable handle for a whole block, so notes can anchor to a diagram or an image."""
    return hashlib.sha1(re.sub(r"\s+", " ", block).strip().encode()).hexdigest()[:10]


def slugify(text: str) -> str:
    s = re.sub(r"<[^>]+>", "", text).lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"[\s_]+", "-", s).strip("-") or "section"


def split_blocks(md: str) -> list[str]:
    """Split markdown into top-level blocks, keeping fences and HTML elements whole."""
    lines = md.replace("\r\n", "\n").split("\n")
    blocks: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        if not lines[i].strip():
            i += 1
            continue

        fence = re.match(r"^\s*(```|~~~)", lines[i])
        if fence:
            marker = fence.group(1)
            j = i + 1
            while j < n and not lines[j].strip().startswith(marker):
                j += 1
            blocks.append("\n".join(lines[i:min(j + 1, n)]))
            i = j + 1
            continue

        tag = re.match(r"^\s*<([a-zA-Z][\w-]*)", lines[i])
        if tag:
            name = tag.group(1).lower()
            if name in VOID_TAGS:
                blocks.append(lines[i])
                i += 1
                continue
            j, depth = i, 0
            while j < n:
                depth += len(re.findall(rf"<{name}\b", lines[j]))
                depth -= len(re.findall(rf"</{name}\s*>", lines[j]))
                depth -= len(re.findall(rf"<{name}\b[^>]*/>", lines[j]))
                if depth <= 0:
                    break
                j += 1
            blocks.append("\n".join(lines[i:min(j + 1, n)]))
            i = j + 1
            continue

        j = i
        while j < n and lines[j].strip():
            j += 1
        blocks.append("\n".join(lines[i:j]))
        i = j
    return blocks


def inline(text: str) -> str:
    out = html.escape(text, quote=False)
    out = re.sub(r"`([^`]+)`", lambda m: f"<code>{m.group(1)}</code>", out)
    out = re.sub(r"<code>(pinned|negotiable|constrained)</code>", r'<span class="rig \1">\1</span>', out)
    out = re.sub(r"!\[([^\]]*)\]\(([^)\s]+)\)", r'<img alt="\1" src="\2">', out)
    out = re.sub(r"\[([^\]]+)\]\(([^)\s]+)\)", r'<a href="\2">\1</a>', out)
    out = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", out)
    out = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", out)
    return out.replace("\n", " ")


def render_table(lines: list[str]) -> str:
    def cells(line: str) -> list[str]:
        return [c.strip() for c in line.strip().strip("|").split("|")]

    head = "".join(f"<th>{inline(c)}</th>" for c in cells(lines[0]))
    body = "".join(
        "<tr>" + "".join(f"<td>{inline(c)}</td>" for c in cells(line)) + "</tr>"
        for line in lines[2:]
        if line.strip()
    )
    return f"<table><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table>"


def render_list(lines: list[str]) -> str:
    tag = "ol" if re.match(r"^\s*\d+[.)]\s", lines[0]) else "ul"
    out = [f"<{tag}>"]
    nested = False
    for line in lines:
        item = re.match(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$", line)
        if not item:
            if out[-1].endswith("</li>"):
                out[-1] = out[-1][:-5] + " " + inline(line.strip()) + "</li>"
            continue
        indent, _, text = item.groups()
        deep = len(indent) >= 2
        if deep and not nested:
            out.append(f"<{tag}>")
            nested = True
        elif not deep and nested:
            out.append(f"</{tag}>")
            nested = False
        out.append(f"<li>{inline(text)}</li>")
    if nested:
        out.append(f"</{tag}>")
    out.append(f"</{tag}>")
    return "".join(out)


def render_block(block: str) -> tuple[str, str | None]:
    """Return (html, heading_slug_if_this_block_is_a_heading)."""
    stripped = block.strip()
    first = stripped.split("\n", 1)[0]
    lines = block.split("\n")

    if re.match(r"^(```|~~~)", first):
        lang = re.sub(r"^(```|~~~)", "", first).strip()
        body = re.sub(r"\n?\s*(```|~~~)\s*$", "", "\n".join(lines[1:]))
        if lang == "mermaid":
            return f'<pre class="mermaid">{html.escape(body)}</pre>', None
        cls = f' class="lang-{lang}"' if lang else ""
        return f"<pre><code{cls}>{html.escape(body)}</code></pre>", None

    if re.match(r"^<[a-zA-Z!]", first):
        return block, None

    heading = re.match(r"^(#{1,6})\s+(.*)$", stripped)
    if heading:
        level, text = len(heading.group(1)), heading.group(2).strip()
        anchor = slugify(text)
        return f'<h{level} id="{anchor}">{inline(text)}</h{level}>', anchor

    if re.match(r"^(-{3,}|\*{3,}|_{3,})$", stripped):
        return "<hr>", None

    body_lines = [line for line in lines if line.strip()]
    if all(line.strip().startswith(">") for line in body_lines):
        inner = "\n".join(re.sub(r"^\s*>\s?", "", line) for line in body_lines)
        return "<blockquote>" + render_block(inner)[0] + "</blockquote>", None

    if first.strip().startswith("|") and len(lines) > 1 and re.match(r"^\s*\|[\s:|-]+\|?\s*$", lines[1]):
        return render_table(lines), None

    if re.match(r"^\s*([-*+]|\d+[.)])\s", first):
        return render_list(lines), None

    return "<p>" + inline(stripped) + "</p>", None


def diff_blocks(old_md: str, new_md: str) -> tuple[set[int], set[int]]:
    """Indices of changed blocks in the new doc, and indices with deletions before them."""
    if not old_md.strip():
        return set(), set()
    matcher = difflib.SequenceMatcher(None, split_blocks(old_md), split_blocks(new_md), autojunk=False)
    changed: set[int] = set()
    removed: set[int] = set()
    for op, _, _, j1, j2 in matcher.get_opcodes():
        if op in ("replace", "insert"):
            changed.update(range(j1, j2))
        elif op == "delete":
            removed.add(j1)
    return changed, removed


def render_page(md: str, previous: str = "") -> str:
    changed, removed = diff_blocks(previous, md)
    blocks = split_blocks(md)
    cut = '<div class="cut">content removed here</div>'
    heading = ""
    out: list[str] = []
    for index, block in enumerate(blocks):
        body, anchor = render_block(block)
        if anchor:
            heading = anchor
        if index in removed:
            out.append(cut)
        marks = ' data-changed="1"' if index in changed else ""
        out.append(
            f'<div class="blk" data-blk="{index}" data-h="{heading}" '
            f'data-sig="{block_sig(block)}"{marks}>{body}</div>'
        )
    if any(index >= len(blocks) for index in removed):
        out.append(cut)
    return "\n".join(out)
