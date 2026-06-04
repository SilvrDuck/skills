# Why skills must stay lean — the evidence

Bloat in a skill isn't just a token bill. Recent work shows it measurably *degrades* the
agent's behavior, and an over-stuffed instruction file can leave the agent worse off than
with no skill at all. Keep this in mind when deciding what earns a place in a SKILL.md body.

## Length degrades quality — and it starts early

- Reasoning accuracy drops as inputs grow, **even at ~3,000 tokens — far below any
  context-window limit** ("Same Task, More Tokens", arXiv:2402.14848). That is the size of a
  single mid-weight skill body.
- Degradation is **continuous, not a cliff**: a 200K-window model can wobble by ~50K, and
  agents with 1–2M windows can lose **>50% by 100K** ("Context Rot", Chroma 2025; "When
  Refusals Fail", arXiv:2512.02445). Capacity is the wrong metric.
- Length hurts **even when retrieval is perfect** — it is not only about whether the info is
  findable (arXiv:2510.05381). Semantic retrieval also collapses: at 32K many models fall
  below 50% of their short-context baseline (NoLiMa, arXiv:2502.05167).
- Models attend most to the **start and end and lose the middle** (the U-curve in "Lost in
  the Middle", TACL 2024). → Put the load-bearing rule near the top.

## Instruction *count* is its own cost

- Adherence falls as you pile on rules: even frontier models reach only **~68% at 500
  simultaneous instructions**, and they are **biased toward earlier instructions**
  ("How Many Instructions Can LLMs Follow at Once?" / IFScale, arXiv:2507.11538).
- The effect is regular enough that a logistic regression on **instruction count alone**
  predicts success within ~10% ("When Instructions Multiply" / ManyIFEval, arXiv:2509.21051).
- → Every extra "always / never / must" dilutes the others. Cut directives the agent does not
  need; front-load the ones it cannot miss.

## A skill can make things *worse*, not just costlier

- Repository instruction files (AGENTS.md) — the same genre a skill belongs to — were found to
  **reduce task success versus no context at all, while adding >20% cost**; "unnecessary
  requirements make tasks harder" ("Evaluating AGENTS.md", arXiv:2602.11988).
- Anthropic frames the target as the **"right altitude"**: avoid both vague hand-waving and
  "hardcoding complex, brittle logic," which "creates fragility." Aim for "the smallest set of
  high-signal tokens that maximize the likelihood of [the] desired outcome" (Effective context
  engineering for AI agents, 2025).

## The counterweight: don't over-compress

- Aggressive minimization has its own failure mode — **"brevity bias"**: prompts collapse to
  short, generic text that *propagates recurring errors* ("Agentic Context Engineering",
  arXiv:2510.04618).
- → The goal is high-signal, not shortest. The smallest *sufficient* set, not the fewest words.

## What this means for authoring

- Default to leaving things out; make each rule earn its place ("does the agent already know
  this?").
- Count distinct directives, not just lines. A dozen sharp rules beat forty hedged ones.
- Put the one rule that must not be missed at the top.
- Prefer one excellent example to five; push reference detail to `references/`, deterministic
  work to `scripts/`.
- Stop trimming when you reach high-signal — not when you reach shortest.

## Sources

- Same Task, More Tokens — <https://arxiv.org/abs/2402.14848>
- How Many Instructions Can LLMs Follow at Once? (IFScale) — <https://arxiv.org/abs/2507.11538>
- When Instructions Multiply (ManyIFEval) — <https://arxiv.org/abs/2509.21051>
- NoLiMa — <https://arxiv.org/abs/2502.05167>
- Context Length Alone Hurts LLM Performance — <https://arxiv.org/abs/2510.05381>
- When Refusals Fail — <https://arxiv.org/abs/2512.02445>
- Agentic Context Engineering — <https://arxiv.org/abs/2510.04618>
- Evaluating AGENTS.md — <https://arxiv.org/abs/2602.11988>
- Lost in the Middle (TACL 2024) — <https://aclanthology.org/2024.tacl-1.9/>
- Context Rot (Chroma) — <https://research.trychroma.com/context-rot>
- Effective context engineering for AI agents (Anthropic) — <https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents>
