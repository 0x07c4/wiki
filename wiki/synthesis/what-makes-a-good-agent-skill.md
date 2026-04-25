---
page_type: synthesis
status: draft
last_updated: 2026-04-25
source_count: 1
---

# What Makes a Good Agent Skill

## Question

How should this wiki judge whether an agent skill is worth tracking, installing, or recommending?

## Short Answer

A good agent skill is a small, trusted, testable procedure package. It should trigger at the right time, improve task reliability, keep context usage low, bound side effects, and make its behavior auditable.

## Rubric

### 1. Trigger Precision

The `description` should clearly state what the skill does and when to use it. This is not marketing copy; it is routing metadata for the agent.

Good signal:

- the trigger condition is obvious
- the skill activates for the intended task family
- it does not steal unrelated requests

### 2. Bounded Scope

The skill should do one coherent job or one coherent family of jobs. Broad "do everything" skills are hard to evaluate and easy to invoke accidentally.

Good signal:

- one primary workflow
- clear inputs and outputs
- explicit non-goals when misuse is likely

### 3. Progressive Disclosure

The main `SKILL.md` should be short enough to orient the agent, with heavy reference material moved into separate files that load only when needed.

Good signal:

- concise main instructions
- linked references for details
- examples and templates separated from core workflow

### 4. Deterministic Helpers

Scripts should be used for operations where deterministic behavior is better than generated text: parsing, validation, conversion, linting, formatting, or data extraction.

Good signal:

- scripts have clear names
- scripts can run locally and fail visibly
- script output is what enters context, not large code blobs

### 5. Permission Discipline

The skill should make side effects explicit. Risky workflows should be user-invoked rather than model-invoked, and tool permissions should be scoped.

Good signal:

- `disable-model-invocation: true` for deploy, commit, publish, send, or other high-impact actions
- `allowed-tools` only for tools that fit the workflow
- no hidden network calls or broad filesystem access without justification

### 6. Eval And Examples

The skill should include examples, fixtures, or tests that make expected behavior inspectable.

Good signal:

- before/after examples
- validation scripts
- known failure cases
- small eval checklist for regressions

### 7. Provenance And Maintenance

Treat skills like software dependencies.

Good signal:

- clear author or repository
- license and version history
- recent maintenance
- minimal external dependencies
- security notes for bundled scripts or fetched resources

## Practical Classification

- Recommended: trusted source, narrow trigger, examples/tests, safe permission posture
- Watchlist: promising pattern but missing tests, provenance, or security review
- Avoid: broad trigger, opaque scripts, network calls, unclear license, or side effects without explicit user control

## Implications

- This wiki should track skill repositories separately from individual skills.
- "优秀 skill" should mean reliable, scoped, auditable, and maintained, not just clever.
- Installing a skill should follow the same instinct as adding a project dependency: read it, inspect scripts, check permissions, and test it on non-critical data first.

## Open Questions

- Should this wiki maintain a formal `wiki/synthesis/agent-skill-watchlist.md`?
- What minimum security review is enough before recommending a third-party skill?
- How should skills for Codex, Claude Code, and ChatGPT be compared when their runtime behavior differs?

## Related Pages

- [Source: Agent Skills and Claude Code Cluster 2026-04-25](../sources/agent-skills-claude-code-cluster-2026-04-25.md)
- [Agent Skills](../concepts/agent-skills.md)
- [Agent Runtime](../concepts/agent-runtime.md)
- [AI Agent Frontier Radar 2026-04](ai-agent-frontier-radar-2026-04.md)

## Citations

- [2026-04-25-agent-skills-claude-code-cluster.md](../../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md)
