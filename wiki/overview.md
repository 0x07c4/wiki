---
page_type: overview
status: active
last_updated: 2026-04-25
source_count: 8
---

# Overview

This wiki is a local knowledge base for agents, with Obsidian as the human-facing workbench and native graph navigator. It combines immutable source snapshots, maintained markdown pages, and local tooling so future agents can quickly find context, trace claims, understand relationships, and decide what to ingest or synthesize next.

It currently tracks three connected ideas: use an LLM to maintain a persistent markdown knowledge base, compile stable thinking about agent runtime and human-in-the-loop execution, and keep a curated radar of recent AI agent progress.

## Current Thesis

A maintained local knowledge base can outperform ad hoc retrieval when agents repeatedly need to understand the same domain, reuse prior synthesis, and avoid re-reading raw material from scratch. The useful artifact is not only the markdown content, but also the operating surface around it: index, log, templates, ingest playbooks, local search, query bundles, lint checks, and graph views.

This wiki can also serve as a compiled layer above upstream personal notes, preserving traceability while turning stable thoughts into concepts and durable synthesis.

- source summaries are already written
- cross-references already exist
- contradictions can be tracked over time
- durable analyses can be filed back into the wiki
- agents can use local commands to locate and inspect context before answering
- the user can use Obsidian's built-in graph views to inspect link structure, then extend the workflow with plugins where needed
- the first plugin direction is a read-first Obsidian Agent Workbench for active-page context, repo health, and agent handoff
- JSON output from `llm-wiki` now has a versioned contract for tool and plugin consumers
- upstream notes can remain the user's source of intent while the wiki maintains the structured knowledge layer
- fast-moving AI agent releases can be collected as source packs before being promoted into stable pages

## Active Concepts

- [LLM Wiki](concepts/llm-wiki.md)
- [Ingest, Query, Lint](concepts/ingest-query-lint.md)
- [Agent Runtime](concepts/agent-runtime.md)
- [Protocol Machine](concepts/protocol-machine.md)
- [Agent Skills](concepts/agent-skills.md)
- [Agent Evaluation](concepts/agent-evaluation.md)

## Active Entities

- [Obsidian](entities/obsidian.md)

## Durable Synthesis

- [Persistent Wiki vs Ad Hoc RAG](synthesis/persistent-wiki-vs-ad-hoc-rag.md)
- [Local Agent Knowledge Base Operating Model](synthesis/local-agent-knowledge-base-operating-model.md)
- [Obsidian Agent Workbench MVP](synthesis/obsidian-agent-workbench-mvp.md)
- [llm-wiki JSON Output Contract](synthesis/llm-wiki-json-output-contract.md)
- [Agent Runtime as Transaction Layer](synthesis/agent-runtime-as-transaction-layer.md)
- [AI Agent Frontier Radar 2026-04](synthesis/ai-agent-frontier-radar-2026-04.md)
- [What Makes a Good Agent Skill](synthesis/what-makes-a-good-agent-skill.md)

## Sources

- [Seed Source: LLM Wiki Pattern](sources/seed-llm-wiki-pattern.md)
- [Source: Agent Interaction Formalism](sources/notes-agent-interaction-formalism.md)
- [Source: AI Agent Frontier Scouting Pack 2026-04-25](sources/agent-frontier-scouting-2026-04-25.md)
- [Source: Agent Skills and Claude Code Cluster 2026-04-25](sources/agent-skills-claude-code-cluster-2026-04-25.md)
- [Source: Obsidian Graph View 2026-04-25](sources/obsidian-graph-view-2026-04-25.md)
- [Source: Obsidian Plugin Development 2026-04-25](sources/obsidian-plugin-development-2026-04-25.md)
- [Source: llm-wiki JSON Contract 2026-04-25](sources/llm-wiki-json-contract-2026-04-25.md)
- [Source: llm-wiki Search JSON Contract 2026-04-25](sources/llm-wiki-search-json-contract-2026-04-25.md)

## Open Questions

- What metadata conventions are worth standardizing across all page types?
- At what scale does plain index navigation stop being enough?
- Which local tools most improve agent comprehension per unit of maintenance cost?
- Would a dedicated Obsidian plugin make source intake, review, graph navigation, or agent handoff materially better?
- Which Obsidian-facing review dashboards would make human-in-the-loop wiki maintenance faster?
- Which `llm-wiki` JSON fields should become stable API for Obsidian integration?
- Should search results include matched-field explanations before the first Obsidian workbench build slice?
- Which parts of ingest should stay explicitly human-reviewed?
- Which wiki synthesis pages should eventually be promoted back into `~/workspace/notes`?
- Which agent frontier sources should be deep-ingested next instead of remaining in source-pack form?
- Which public skill repositories deserve a maintained watchlist?

## Citations

- [seed-llm-wiki-pattern.md](../raw/sources/seed-llm-wiki-pattern.md)
- [agent-interaction-formalism.md](../raw/sources/notes/agent-interaction-formalism.md)
- [2026-04-25-agent-frontier-scouting.md](../raw/sources/agent-frontier/2026-04-25-agent-frontier-scouting.md)
- [2026-04-25-agent-skills-claude-code-cluster.md](../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md)
- [2026-04-25-obsidian-graph-view.md](../raw/sources/obsidian/2026-04-25-obsidian-graph-view.md)
- [2026-04-25-obsidian-plugin-development.md](../raw/sources/obsidian/2026-04-25-obsidian-plugin-development.md)
- [2026-04-25-llm-wiki-json-contract.md](../raw/sources/tooling/2026-04-25-llm-wiki-json-contract.md)
- [2026-04-25-llm-wiki-search-json-contract.md](../raw/sources/tooling/2026-04-25-llm-wiki-search-json-contract.md)
