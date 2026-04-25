---
page_type: concept
status: active
last_updated: 2026-04-25
source_count: 1
---

# Protocol Machine

## Definition

A protocol machine is an agent-system architecture where legal interaction order, capability boundaries, and invariant checks are explicit runtime constraints instead of informal prompt instructions.

## Why It Matters

Agent failures are often not just bad answers. They are illegal transitions, unsafe side effects, missing approvals, or UI projections that guess state from text. A protocol machine gives the system a concrete place to enforce what can happen next.

## Supporting Evidence

- the upstream note argues that one formalism is not enough: protocol order, capability boundaries, and invariants solve different parts of the problem
- state machine or typestate is the most practical core abstraction for daily product and runtime flow
- capability and effect checks should guard side effects such as command execution and file writes
- invariants such as preview-before-apply and no-write-without-approval should be checked against structured traces

## Tensions

- protocol can overfit too early if the product interaction is still changing rapidly
- free-form natural language is still useful for intent capture, steering, and review
- the useful level of formalism should be executable enough to constrain behavior without becoming a proof burden for every routine flow

## Related Pages

- [Source: Agent Interaction Formalism](../sources/notes-agent-interaction-formalism.md)
- [Agent Runtime](agent-runtime.md)
- [Agent Runtime as Transaction Layer](../synthesis/agent-runtime-as-transaction-layer.md)

## Citations

- [agent-interaction-formalism.md](../../raw/sources/notes/agent-interaction-formalism.md)
