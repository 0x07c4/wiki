---
page_type: entity
status: active
last_updated: 2026-04-25
source_count: 3
---

# Obsidian

## Role

Obsidian is the human-facing workspace for this agent-maintained markdown knowledge base. The agent maintains files; the user uses Obsidian to browse, inspect, navigate, review the evolving wiki, and use built-in graph views over the repo's markdown links.

## Relevance

In the seed note, Obsidian functions like the human-facing IDE for the knowledge base:

- the user reads and inspects pages
- the user reviews agent writebacks in real time
- built-in Graph view reveals vault-wide link structure
- built-in Local Graph reveals the neighborhood around the active note
- Web Clipper can help convert external articles into markdown sources
- local attachment handling can preserve images under `raw/assets/`
- plugins such as Dataview and Marp can extend how the wiki is queried, viewed, or presented
- custom plugins can add commands, ribbon actions, and custom views, so a focused Agent Workbench panel is technically plausible

## Plugin Layer

Obsidian's native graph should be treated as a baseline capability. Additional plugins should be treated as workflow extensions, not as prerequisites for graph navigation. A future plugin or plugin bundle could improve:

- source intake from browser clips into `raw/inbox/`
- review of proposed agent writebacks before they become durable pages
- graph navigation around concepts, entities, sources, and synthesis pages
- frontmatter-driven dashboards for stale pages, source counts, open questions, and recent log entries
- handoff between human browsing in Obsidian and agent operations in the CLI

This repo should avoid assuming one specific plugin is mandatory until a source is ingested or the user chooses a concrete plugin direction.

The current concrete direction is a read-first [Obsidian Agent Workbench MVP](../synthesis/obsidian-agent-workbench-mvp.md): active-page context, related wiki links, repo health, and safe agent handoff before direct writeback.

## Relationships

- supports the browsing layer for the [LLM Wiki](../concepts/llm-wiki.md)
- complements the [Ingest, Query, Lint](../concepts/ingest-query-lint.md) workflow
- provides the human review surface around agent-maintained pages and raw sources
- anchors the human side of the [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)
- is the target host for the [Obsidian Agent Workbench MVP](../synthesis/obsidian-agent-workbench-mvp.md)

## Citations

- [seed-llm-wiki-pattern.md](../../raw/sources/seed-llm-wiki-pattern.md)
- [2026-04-25-obsidian-graph-view.md](../../raw/sources/obsidian/2026-04-25-obsidian-graph-view.md)
- [2026-04-25-obsidian-plugin-development.md](../../raw/sources/obsidian/2026-04-25-obsidian-plugin-development.md)
