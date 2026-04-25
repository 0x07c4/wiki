---
page_type: synthesis
status: active
last_updated: 2026-04-25
source_count: 7
---

# Local Agent Knowledge Base Operating Model

## Question

What operating model should this repository use so it works as a local knowledge base for agents while remaining easy for the user to inspect in Obsidian?

## Short Answer

Use a four-layer model:

- `raw/` is the evidence layer.
- `wiki/` is the compiled knowledge layer.
- `llm-wiki` CLI, playbooks, templates, and `AGENTS.md` are the agent operation layer.
- Obsidian is the human navigation and review layer.

Plugins should extend this model only where repeated workflow friction appears. Obsidian's built-in graph views already provide the baseline knowledge-graph navigation surface.

## Evidence

- The seed source defines a persistent wiki pattern where raw sources stay immutable, the LLM maintains the wiki, and schema files discipline ingest, query, and lint behavior. It also describes the practical setup as agent on one side and Obsidian on the other: the agent edits, while the user browses and inspects. [Seed Source: LLM Wiki Pattern](../sources/seed-llm-wiki-pattern.md)
- Obsidian's Graph view is a core capability for visualizing note relationships, and Local Graph exposes the neighborhood around the active note. This makes Obsidian a native graph navigator for the markdown wiki rather than just a file viewer. [Source: Obsidian Graph View 2026-04-25](../sources/obsidian-graph-view-2026-04-25.md)
- Obsidian plugins can extend the app with TypeScript, add user-facing commands, and create custom views, so a narrow Agent Workbench can connect the human navigation layer to the agent operation layer. [Source: Obsidian Plugin Development 2026-04-25](../sources/obsidian-plugin-development-2026-04-25.md)
- The agent interaction formalism source argues that reliable agent systems need explicit protocol, capability boundaries, and invariants rather than prompt text alone. In this repository, those constraints live in `AGENTS.md`, playbooks, lint checks, and traceable source conventions. [Source: Agent Interaction Formalism](../sources/notes-agent-interaction-formalism.md)
- Recent agent frontier sources show the field moving toward models packaged with runtime, sandbox, tools, skills, approvals, and evaluation infrastructure. This supports treating local CLI commands and operational playbooks as part of the knowledge base, not as incidental scripts. [Source: AI Agent Frontier Scouting Pack 2026-04-25](../sources/agent-frontier-scouting-2026-04-25.md)
- The agent skills source cluster frames reusable procedures, scripts, and metadata as portable agent capability. This supports keeping project workflows such as ingest, lint, notes import, and Obsidian review as explicit playbooks. [Source: Agent Skills and Claude Code Cluster 2026-04-25](../sources/agent-skills-claude-code-cluster-2026-04-25.md)

## Implications

- Future agents should start from `wiki/index.md`, then use `llm-wiki search`, `query`, `status`, or `graph` when local structure matters.
- Tool integrations should prefer JSON output from `llm-wiki search --json`, `llm-wiki status --json`, `llm-wiki graph --json`, and `llm-wiki query --json`, following the [llm-wiki JSON Output Contract](llm-wiki-json-output-contract.md).
- Durable claims should flow from `raw/` into source summaries, then into concept, entity, or synthesis pages.
- The user should review the maintained layer in Obsidian, especially through overview pages, local graph neighborhoods, backlinks, and open questions.
- Obsidian plugins are worth considering when they reduce repeated friction in source intake, review, dashboards, presentation, or handoff to agent commands.
- The first plugin should stay read-first and handoff-oriented until the review workflow proves where direct writeback is safe.
- The repo should resist becoming either a passive note dump or a tool-only project; the value is the coupling of maintained knowledge and operating facilities.

## Open Questions

- Which Obsidian dashboards would make review materially faster?
- Should the repo include recommended `.obsidian/` workspace settings, or keep editor configuration outside version control?
- Which `llm-wiki` commands should be callable from the active Obsidian page?
- What metadata fields are needed before Dataview-style dashboards become useful?
- Which `llm-wiki` JSON fields should be stabilized before an Obsidian Agent Workbench is implemented?

## Related Pages

- [LLM Wiki](../concepts/llm-wiki.md)
- [Ingest, Query, Lint](../concepts/ingest-query-lint.md)
- [Agent Runtime](../concepts/agent-runtime.md)
- [Agent Skills](../concepts/agent-skills.md)
- [Obsidian](../entities/obsidian.md)
- [Obsidian Agent Workbench MVP](obsidian-agent-workbench-mvp.md)
- [llm-wiki JSON Output Contract](llm-wiki-json-output-contract.md)
- [Persistent Wiki vs Ad Hoc RAG](persistent-wiki-vs-ad-hoc-rag.md)

## Citations

- [seed-llm-wiki-pattern.md](../../raw/sources/seed-llm-wiki-pattern.md)
- [2026-04-25-obsidian-graph-view.md](../../raw/sources/obsidian/2026-04-25-obsidian-graph-view.md)
- [2026-04-25-obsidian-plugin-development.md](../../raw/sources/obsidian/2026-04-25-obsidian-plugin-development.md)
- [agent-interaction-formalism.md](../../raw/sources/notes/agent-interaction-formalism.md)
- [2026-04-25-agent-frontier-scouting.md](../../raw/sources/agent-frontier/2026-04-25-agent-frontier-scouting.md)
- [2026-04-25-agent-skills-claude-code-cluster.md](../../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md)
