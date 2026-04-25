---
page_type: source
status: ingested
last_updated: 2026-04-25
source_count: 1
source_path: ../../raw/sources/notes/agent-interaction-formalism.md
---

# Source: Agent Interaction Formalism

## Summary

This upstream note argues that agent systems should be constrained by executable protocol, capability boundaries, and invariants instead of prompt text alone. It also frames agent runtime as a transaction-like layer that controls intent, preview, approval, commit, recovery, replay, and audit.

## Source Metadata

- upstream path: `/home/chikee/workspace/notes/agent-interaction-formalism.md`
- upstream commit: `417ec3c8a1be6c1f35066e8e67606fb7b5a457b1`
- upstream status: `evergreen`

## Key Claims

- agent architecture should be modeled as `protocol + capabilities + invariants`
- state machines or typestate are the most practical main abstraction for agent interaction
- capability and effect boundaries should govern side effects such as file writes, commands, and external requests
- natural language belongs in intent and deliberation layers, not in protocol, effect, or correctness layers
- agent runtime is an AI system transaction layer, mediating intent, preview, approval, commit, recovery, and audit
- human-in-the-loop is not merely a fallback; it provides commit semantics for high-value workflows

## Evidence Notes

- the note distinguishes protocol order, capability boundaries, and invariant checks as separate but complementary constraints
- it maps runtime enforcement to orchestrator, tool executor, UI projection, and eval/replay
- it identifies `thread`, `turn`, `item`, `approval`, `diff`, `plan`, `event stream`, and `replay` as runtime primitives
- it compares approval to a commit protocol with prepare, approve or reject, and commit or abort phases
- it argues that most current agents remain closer to `LLM + tools + prompt glue` than `runtime + protocol + bounded effects`

## Related Pages

- [Agent Runtime](../concepts/agent-runtime.md)
- [Protocol Machine](../concepts/protocol-machine.md)
- [Agent Runtime as Transaction Layer](../synthesis/agent-runtime-as-transaction-layer.md)
- [LLM Wiki](../concepts/llm-wiki.md)

## Open Questions

- Which runtime primitives should become mandatory in the wiki's future agent-system vocabulary?
- How should future Solo-specific notes be split between concept pages and synthesis pages?
- When should a wiki synthesis be promoted back into `~/workspace/notes`?

## Citations

- [agent-interaction-formalism.md](../../raw/sources/notes/agent-interaction-formalism.md)
