---
name: ldl
description: Diagnose and improve the user's own explanation through a learning-by-teaching loop. Use when the user types `/ldl` followed by their current understanding, asks to test their understanding in their own words, or wants misconceptions, near-misses, and conflated concepts identified.
argument-hint: "[your explanation]"
disable-model-invocation: true
---

# ldl

The learner teaches; the agent diagnoses. Do not replace their attempt with a lecture. Preserve what works, expose the precise gaps, then make them teach it again.

## Loop

1. Treat the user's explanation as their current mental model.
2. Verify factual claims using available sources and tools. If a term may be private jargon or a typo, resolve it before grading.
3. Return only the sections that apply:

### Correct

The load-bearing claims they understand correctly.

### Fix

Factual errors. State the correction and briefly explain why.

### Close

Rewrite near-misses while preserving their wording. Highlight changes as:

> The ~~old wording~~ **corrected wording**.

### Conflation

Name the concepts being mixed together, then give the shortest distinction that separates them.

### Missing link

Add an omitted causal or logical step only when its absence breaks the explanation.

4. Explain the learner's misconception, not every edit. Prefer the smallest conceptual correction that repairs the whole model.
5. Source factual corrections where practical.
6. End with:

> **Teach it again in your own words, without looking above.**

On the retry, focus on what changed. Repeat until the explanation is accurate, then confirm it and give one compact canonical formulation.

## Anti-patterns

- Replacing the attempt with a complete lecture.
- Correcting harmless wording that does not affect understanding.
- Saying only “wrong” or giving the answer without explaining the misconception.
- Praising vaguely instead of identifying what was actually understood.
- Skipping the second teach-back.
