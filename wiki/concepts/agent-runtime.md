---
page_type: concept
status: active
last_updated: 2026-04-25
source_count: 2
---

# Agent Runtime

## Definition

An agent runtime is the infrastructure layer between product interaction and model or tool providers. It represents the structured lifecycle of agent work: thread, turn, item, plan, diff, approval, event stream, replay, recovery, and audit.

## Why It Matters

Once an agent can perform multi-step work, call tools, read or write files, and require approval, the hard problem is no longer only model output. The system needs a stable layer that says what is happening, which side effects are allowed, where the user can intervene, and how the work can be recovered or reviewed.

## Supporting Evidence

- the upstream note describes agent runtime as the layer that turns user intent into controlled execution
- runtime primitives such as `thread`, `turn`, `item`, `approval`, `diff`, and `plan` are needed when agent work must be recoverable and auditable
- if product semantics are tied directly to a provider, then changing providers can make the interaction model drift
- UI should read runtime projections instead of inferring state from provider-specific text
- 2025-2026 agent releases increasingly package models with harnesses, sandboxes, shared agents, skills, memory, approvals, worktrees, automations, and evaluation infrastructure

## Tensions

- many side effects are not truly reversible, so runtime can provide transaction-like control without guaranteeing database-style rollback
- natural language remains useful for intent and deliberation, but it cannot be the final source of execution semantics
- a runtime layer can become too heavy if it models every possible action before the product workflow stabilizes

## Related Pages

- [Source: Agent Interaction Formalism](../sources/notes-agent-interaction-formalism.md)
- [Source: AI Agent Frontier Scouting Pack 2026-04-25](../sources/agent-frontier-scouting-2026-04-25.md)
- [Agent Skills](agent-skills.md)
- [Agent Evaluation](agent-evaluation.md)
- [Protocol Machine](protocol-machine.md)
- [Agent Runtime as Transaction Layer](../synthesis/agent-runtime-as-transaction-layer.md)
- [AI Agent Frontier Radar 2026-04](../synthesis/ai-agent-frontier-radar-2026-04.md)

## Citations

- [agent-interaction-formalism.md](../../raw/sources/notes/agent-interaction-formalism.md)
- [2026-04-25-agent-frontier-scouting.md](../../raw/sources/agent-frontier/2026-04-25-agent-frontier-scouting.md)
