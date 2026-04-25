---
page_type: synthesis
status: draft
last_updated: 2026-04-25
source_count: 1
---

# Agent Runtime as Transaction Layer

## Question

Why treat agent runtime as a transaction-like layer instead of just a chat loop with tools?

## Short Answer

Because high-value agent work needs controlled execution. The important boundary is not when text generation finishes, but when side effects are previewed, approved, committed, recovered, and audited.

## Evidence

- user intent should not directly become file writes, command execution, or external requests
- agent work needs stages such as drafted, previewed, approved, applied, failed, and rolled back
- approval is part of the commit protocol, not merely a UI prompt
- structured runtime history is required for replay, audit, eval, and debugging
- human-in-the-loop workflows match this model because the user participates at steer, preview, approve, reject, fork, and rollback points

## Implications

- product UI should expose preview, approval, and commit points as first-class states
- provider adapters should feed runtime events, not define product semantics
- model improvements reduce friction, but protocol, capability, and invariant design still handle essential complexity
- systems that remain `LLM + tools + prompt glue` will struggle with recovery, replay, audit, and provider substitution

## Limits

- transaction-like control does not mean every tool side effect can be perfectly rolled back
- long-running agent work may need user steering and partial commits rather than a single atomic transaction
- this synthesis currently rests on one upstream note and should be checked against future runtime sources

## Related Pages

- [Source: Agent Interaction Formalism](../sources/notes-agent-interaction-formalism.md)
- [Agent Runtime](../concepts/agent-runtime.md)
- [Protocol Machine](../concepts/protocol-machine.md)

## Citations

- [agent-interaction-formalism.md](../../raw/sources/notes/agent-interaction-formalism.md)
