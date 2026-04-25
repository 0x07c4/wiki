---
page_type: synthesis
status: draft
last_updated: 2026-04-25
source_count: 2
---

# AI Agent Frontier Radar 2026-04

## Question

What recent AI agent developments should this wiki track first?

## Short Answer

The agent frontier is moving from model capability alone toward complete execution systems. The most important themes are long-horizon models, sandboxed runtime, shared workspace agents, portable skills, open coordination standards, and evaluation that measures real tool-based work.

## Radar

### 1. Models Are Being Marketed Around Execution

Recent model releases from OpenAI, Anthropic, and Google increasingly emphasize agentic coding, computer use, long-running work, deep research, and tool coordination. The model itself matters, but the relevant claim is now usually "what work can this model carry across tools and time?"

Why it matters:

- coding models are becoming broader computer-work agents
- model releases are tied to products such as Codex, Claude Code, Gemini Deep Research, and computer-use APIs
- benchmark claims increasingly focus on Terminal-Bench, SWE-Bench Pro, OSWorld, tool-use, and knowledge-work evaluations

### 2. Runtime Is Becoming Product Infrastructure

OpenAI's Agents SDK, Codex app, workspace agents, and AgentKit all point in the same direction: useful agents need harnesses, sandboxes, tool integrations, memory, approval, review queues, dashboards, and enterprise controls.

Why it matters:

- the runtime layer is becoming more durable than any single model release
- shared agents need governance, visibility, and permission boundaries
- personal and team workflows need continuity across CLI, desktop, web, Slack, and cloud execution

### 3. Skills Are Becoming Procedural Memory

Agent Skills package reusable domain expertise as filesystem resources: metadata for discovery, instructions for workflows, scripts for deterministic operations, and reference files for domain context. This creates a middle layer between prompts and full integrations.

Why it matters:

- good skills can encode a team's repeatable workflows
- skills are composable and can load only when relevant
- skills also introduce a trust surface because they can guide tool use or run code
- the first durable selection filter should be quality and trust, not novelty

### 4. Standards Are Consolidating Around Agent Interop

MCP, AGENTS.md, goose, and Agent Skills are moving into foundation-style governance or open-standard positioning. This suggests the ecosystem wants shared primitives for connecting models to tools, instructions, and workspaces.

Why it matters:

- interop standards reduce custom integration work
- standards also create common security and supply-chain concerns
- project-level instructions and tool protocols are becoming part of agent runtime, not just documentation

### 5. Evaluation Is Moving Toward Real Execution

SWE-Bench Pro, Terminal-Bench 2.0, τ-bench, and OSWorld-Human all push beyond answer correctness. They test software changes, terminal operation, tool-user-policy loops, repeated reliability, GUI control, and latency.

Why it matters:

- agents need to be evaluated by trace and world-state outcomes
- latency and unnecessary steps can make a nominally accurate computer-use agent impractical
- evaluation should influence product design: approval, replay, rollback, and trace inspection need to be first-class

## Near-Term Ingest Queue

- Deep ingest OpenAI's GPT-5.5, Agents SDK, workspace agents, and Codex app materials as one product-runtime cluster
- Continue deep ingest of Anthropic Agent Skills and Claude Code by adding a curated skill repository watchlist
- Deep ingest Google's Gemini computer-use and Deep Research materials as one computer-use-and-research-agent cluster
- Deep ingest Terminal-Bench 2.0, SWE-Bench Pro, τ-bench, and OSWorld-Human as one evaluation cluster
- Deep ingest AAIF, MCP, AGENTS.md, and Agent Skills open-standard materials as one interoperability cluster

## Implications

- This wiki should maintain a recurring "agent frontier radar" synthesis instead of scattering release notes across chat history
- Source packs are useful for scouting, but stable claims should later be promoted into one-source-at-a-time pages
- For Solo, the relevant signal is not only "which model is best" but which runtime primitives, skill formats, and evaluation patterns are becoming standard

## Open Questions

- What threshold should decide whether a release gets its own source summary page?
- Which external skill repositories are trusted enough to track?
- Should the wiki keep a model-release timeline separate from deeper concept pages?
- How should security issues in skills, MCP servers, and code-execution agents be tracked?

## Related Pages

- [Source: AI Agent Frontier Scouting Pack 2026-04-25](../sources/agent-frontier-scouting-2026-04-25.md)
- [Source: Agent Skills and Claude Code Cluster 2026-04-25](../sources/agent-skills-claude-code-cluster-2026-04-25.md)
- [Agent Runtime](../concepts/agent-runtime.md)
- [Agent Skills](../concepts/agent-skills.md)
- [Agent Evaluation](../concepts/agent-evaluation.md)
- [Protocol Machine](../concepts/protocol-machine.md)
- [What Makes a Good Agent Skill](what-makes-a-good-agent-skill.md)

## Citations

- [2026-04-25-agent-frontier-scouting.md](../../raw/sources/agent-frontier/2026-04-25-agent-frontier-scouting.md)
- [2026-04-25-agent-skills-claude-code-cluster.md](../../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md)
