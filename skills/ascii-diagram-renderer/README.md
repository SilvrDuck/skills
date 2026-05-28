# ascii-diagram-renderer

Claude Skill for generating clean ASCII and Unicode box-art diagrams from D2, Graph::Easy, or PlantUML source.

This skill is intentionally broad: it should be used whenever Claude needs to draw a diagram, including diagrams shown directly in chat, not only README files.

## Install in Claude Code

```bash
mkdir -p ~/.claude/skills
cp -R ascii-diagram-renderer ~/.claude/skills/
```

Replace any older copy of this skill so Claude sees the broader activation description:

```bash
rm -rf ~/.claude/skills/ascii-diagram-renderer
cp -R ascii-diagram-renderer ~/.claude/skills/
```

## Use

Invoke directly:

```text
/ascii-diagram-renderer draw a terminal-friendly diagram of our auth gateway flow
```

Or ask naturally:

```text
Draw the flow in chat as an ASCII diagram.
```

```text
Show me a box-and-arrow diagram for this architecture.
```

```text
Add a monospace diagram to this PR comment.
```

## Render manually

```bash
cd ascii-diagram-renderer
scripts/render_d2_ascii.sh examples/agentcore-obo.d2 /tmp/agentcore-obo.txt extended
scripts/render_graph_easy.sh examples/agentcore-obo.ge /tmp/agentcore-obo-ge.txt boxart
```

## Principle

Do not hand-align final diagrams. Write source, render, inspect, then revise the source.
