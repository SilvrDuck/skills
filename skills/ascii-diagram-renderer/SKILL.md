---
name: ascii-diagram-renderer
description: Use when the user explicitly asks to create, draw, or render a diagram, or when producing a substantial diagram for documentation — architecture diagrams, system flows, network maps, service maps, dependency graphs, sequence-like flows in READMEs, docs, or specs. Reserve for deliberate, documentation-grade diagrams and explicit requests; do not auto-trigger on every passing mention of a diagram.
compatibility: Requires d2 >= 0.7.1; graph-easy and plantuml optional
---

# ASCII Diagram Renderer

Use this skill whenever a response would benefit from a diagram, not only for README files. This includes diagrams shown directly in chat, diagrams embedded in Markdown, diagrams for docs/specs/issues/PRs, and diagrams intended for terminal-friendly output.

## Activation policy

Use this skill for:

- Any request to draw, sketch, visualize, map, diagram, explain with boxes, or show a flow.
- Any architecture, auth flow, service flow, data flow, deployment, network, dependency, or system interaction diagram.
- Any ASCII, Unicode box-art, terminal, monospace, Markdown, README, PR, issue, doc, or code-comment diagram.
- Any model-generated diagram that would otherwise require manual spacing or aligned arrows.

Do not limit this skill to README-ready output. If the final answer is a normal chat message and it contains a diagram, use this skill.

If the user explicitly asks for Mermaid, DOT, PlantUML, D2, or another source format, respect that format. Still apply this skill's style rules: short labels, simple layout, no broken geometry, and no hand-aligned final ASCII unless a renderer is unavailable.

## Core rule

Never hand-align final ASCII or Unicode box-art diagrams directly. Always create a small diagram source first, render it with a layout tool, inspect the rendered output, and revise the source when needed.

A correct small diagram is better than a dense broken one.

## Preferred workflow

1. Infer the simplest useful diagram from the user's request. Clarify only when the missing detail changes the structure.
2. Choose the output:
   - If the user asked for ASCII or terminal-friendly output, render text output.
   - If the user asked for a source diagram format, provide that source.
   - If the user did not specify, prefer a compact text diagram for chat and Markdown.
3. Choose the renderer:
   - Use D2 first for architecture diagrams, service flows, containers, arrows, and nested groups.
   - Use Graph::Easy when D2 ASCII output is poor or when the requested diagram is a simple directed graph.
   - Use PlantUML for sequence diagrams if PlantUML is available.
4. Keep labels short. Prefer 1-4 words per node and edge label.
5. Create a source file, usually `diagram.d2`.
6. Render to text using one of the scripts in `scripts/` or the direct commands below.
7. Inspect the output before presenting it. Fix broken lines by simplifying labels, reducing nesting, or splitting the diagram.
8. Return the rendered diagram directly in the chat or target document. Include the source block when the user may want to maintain it.

## Rendering commands

D2, Unicode box drawing:

```bash
scripts/render_d2_ascii.sh diagram.d2 diagram.txt extended
```

D2, portable plain ASCII:

```bash
scripts/render_d2_ascii.sh diagram.d2 diagram.txt standard
```

Graph::Easy, Unicode box drawing:

```bash
scripts/render_graph_easy.sh diagram.ge diagram.txt boxart
```

Graph::Easy, portable plain ASCII:

```bash
scripts/render_graph_easy.sh diagram.ge diagram.txt ascii
```

PlantUML, ASCII text:

```bash
plantuml -txt sequence.puml
```

PlantUML, Unicode text:

```bash
plantuml -utxt sequence.puml
```

## D2 authoring rules

- Add `direction: down` or `direction: right` explicitly.
- Use stable IDs and short display labels.
- Prefer simple arrows over clever edge routing.
- Avoid long paragraphs inside nodes.
- Put details as edge labels or notes outside the main path.
- For complex systems, split into multiple diagrams instead of forcing one large ASCII block.

### D2 ASCII rendering pitfalls

- **No `$` in labels.** D2 parses `$` as variable substitution; `"$HOME"` fails to compile with `substitutions must begin on {`. Strip the `$` or use a `vars:` block.
- **No `\n` in node labels.** The ASCII backend does not reflow box borders around multi-line text — the label overruns the box. Keep each node label on one line; split into two nodes if needed.
- **Edge labels at the same junction will fuse** (e.g. `sourced` + `writes` → `sourcedrites`). Drop one, shorten to a single character, or route one edge around.
- **Nested containers blow up width fast.** Each container adds ~6 columns per level. Before presenting, run `wc -L <output>` — if wider than ~120, split into two diagrams rather than shrinking labels.

Minimal D2 pattern:

```d2
direction: down

client: Client
gw: Gateway
svc: Service
db: Database

client -> gw: request
gw -> svc: call
svc -> db: query
```

## Graph::Easy authoring rules

Use Graph::Easy for compact directed flows where source readability matters more than D2 features.

```text
[ Client ] -> [ Gateway ] { label: request; }
[ Gateway ] -> [ Service ] { label: call; }
[ Service ] -> [ Database ] { label: query; }
```

## Chat response rules

When the diagram appears directly in chat:

- Put the rendered diagram inside a fenced code block.
- Use the shortest diagram that answers the question.
- Avoid explanatory prose inside boxes.
- Do not say the diagram is approximate unless it actually omits important details.
- Include source only when useful; otherwise keep the response focused on the rendered diagram.

## Quality checklist

Before responding, verify:

- Every box border is closed.
- Arrows touch the intended node or edge.
- Labels are readable in a monospaced font.
- The diagram survives copy-paste in Markdown code fences.
- The diagram fits the answer context: chat, docs, README, PR, issue, spec, or terminal.
- The source is included when the user may edit the diagram later.
- `wc -L` on the rendered text is under ~120 columns for chat / Markdown targets. If wider, split or simplify.
- Read the rendered file back — don't trust the last few `tail` lines of the render command. Border breaks usually appear mid-file.

## Failure handling

If a renderer is unavailable, do not fake a rendered result. Say which command is missing and provide the source plus the exact install or render command the user should run.

If the rendered result has broken geometry, simplify the source and render again. Prefer a smaller correct diagram over a dense broken one.
