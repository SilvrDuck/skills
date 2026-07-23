# Claude Code implementation notes

Use this reference only when the harness is Claude Code. Prefer runtime inspection over hard-coded model versions because aliases and plan entitlements change.

## Scheduling

- Schedule the plain prompt `agent-platform heartbeat`; the skill description is intentionally narrow but model-invocable so the scheduled prompt can load it.
- Keep scheduling in the main agent. Background subagents do not receive the wakeup tool.
- Prefer one-shot wakeups chained by each heartbeat over a broad recurring cron: the next fire can jump directly to the next active window and only one task remains armed.
- Session scheduling requires the Claude Code session to remain open or backgrounded and recurring tasks expire. For automation that must survive independently, use a Desktop scheduled task, a cloud routine, GitHub Actions, or an external supervisor instead of pretending the session scheduler is permanent.

## Models

Inspect the effective current model, model picker/configuration, provider, `availableModels`, and alias overrides when exposed. Do not probe every candidate with subagent calls.

Route by capability rather than brand name:

| Class | Claude Code default candidate | Use |
|---|---|---|
| fast | `haiku` | polling, inventory, simple extraction, mechanical checks |
| general | `sonnet` or `inherit` | normal coding and investigation |
| strong | `opus`, `best`, or `fable` when exposed | architecture, hard diagnosis, synthesis, adversarial review |

Treat these as candidates, not promises. An organization allowlist, provider, or subscription may exclude them. On rejection, fall back once and update the model map.

## Orchestration choice

- **Subagents:** default; focused work that reports back to the lead.
- **Agent teams:** only when peers need shared tasks or direct communication. They cost materially more and remain experimental.
- **Dynamic workflows:** many agents or repeatable scripted fan-out. Set a small size guideline and route cheap stages to a cheaper model.

The lead remains responsible for HEART interpretation, final synthesis, logging, and scheduling.
