---
page_type: concept
status: active
last_updated: 2026-04-25
source_count: 1
---

# Agent Evaluation

## Definition

Agent evaluation measures whether an AI system can complete multi-step work with tools, state, policies, user interaction, and realistic environments. It is broader than answer accuracy or single-shot coding quality.

## Why It Matters

Agents fail in ways ordinary chat benchmarks do not capture: illegal tool use, missing approvals, brittle recovery, long latency, bad terminal behavior, unreliable repeated runs, and failure to follow domain policy. Agent evaluation needs to test execution traces and final world state, not just final text.

## Supporting Evidence

- SWE-Bench Pro raises difficulty for agentic coding by using broader and more contamination-resistant software tasks
- Terminal-Bench 2.0 tests agents in terminal environments where they must plan, execute, recover, and use containers
- τ-bench evaluates tool-agent-user interaction against domain policies and final database state, including reliability over repeated trials
- OSWorld-Human highlights latency and step inefficiency in computer-use agents, showing that accuracy alone can hide unusable workflows

## Tensions

- benchmarks can become stale quickly as frontier systems optimize for them
- realistic environments are expensive to run and hard to standardize
- product usefulness depends on user trust, reviewability, and handoff quality, which are harder to score than task pass/fail

## Related Pages

- [Source: AI Agent Frontier Scouting Pack 2026-04-25](../sources/agent-frontier-scouting-2026-04-25.md)
- [Agent Runtime](agent-runtime.md)
- [Agent Runtime as Transaction Layer](../synthesis/agent-runtime-as-transaction-layer.md)
- [AI Agent Frontier Radar 2026-04](../synthesis/ai-agent-frontier-radar-2026-04.md)

## Citations

- [2026-04-25-agent-frontier-scouting.md](../../raw/sources/agent-frontier/2026-04-25-agent-frontier-scouting.md)
