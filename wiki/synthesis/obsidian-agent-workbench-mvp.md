---
page_type: synthesis
status: active
last_updated: 2026-04-26
source_count: 9
---

# Obsidian Agent Workbench MVP

## Question

What is the smallest useful Obsidian plugin or panel for this local agent knowledge base?

## Short Answer

Build the first version as a read-first Agent Workbench, not an autonomous editor. The MVP should help the user inspect the active wiki page, understand nearby context, run or copy safe `llm-wiki` commands, and review what an agent changed.

The plugin should not replace Obsidian's built-in graph views. It should sit beside them as a control and review panel for this repository's agent workflow. It can consume `llm-wiki search --json`, `llm-wiki status --json`, `llm-wiki graph --json`, and `llm-wiki query --json` according to the [llm-wiki JSON Output Contract](llm-wiki-json-output-contract.md) instead of scraping human-readable command output.

## MVP Scope

- Active page status: page type, source count, last updated, source path, and open questions.
- Nearby context: backlinks, outbound wiki links, related source summaries, and synthesis pages.
- Repo health shortcuts: show latest `wiki/log.md` entries, orphan status, and top hubs from `llm-wiki status --json`.
- Agent handoff commands: generate commands such as `llm-wiki search "<active page topic>" --json`, `llm-wiki query "<active page question>" --json`, `llm-wiki graph --json`, `llm-wiki lint`, and `llm-wiki status --json`.
- Review mode: list changed wiki pages and point the user to pages worth inspecting in Obsidian first.

## Non-Goals

- Do not edit `raw/` or `wiki/` directly from the plugin in the first version.
- Do not bypass agent confirmation for durable writebacks.
- Do not replace Obsidian Graph view or Local Graph.
- Do not depend on one complex dashboard before the basic active-page workflow is proven.
- Do not commit `.obsidian/` settings into this repo unless the user explicitly chooses that path.

## Evidence

- The repo's operating model separates evidence, compiled knowledge, agent operation, and human navigation layers. The plugin should improve the handoff between the human navigation layer and the agent operation layer. [Local Agent Knowledge Base Operating Model](local-agent-knowledge-base-operating-model.md)
- Obsidian has native global and local graph views, so the plugin should complement graph navigation rather than reimplement it. [Source: Obsidian Graph View 2026-04-25](../sources/obsidian-graph-view-2026-04-25.md)
- Obsidian plugins extend the app with TypeScript, can add ribbon icons and commands, and can create custom views or custom Bases views. This makes a side panel or dashboard feasible. [Source: Obsidian Plugin Development 2026-04-25](../sources/obsidian-plugin-development-2026-04-25.md)
- Obsidian recommends developing plugins in a separate vault, which fits this repo's rule that `.obsidian/` configuration should not be changed casually. [Source: Obsidian Plugin Development 2026-04-25](../sources/obsidian-plugin-development-2026-04-25.md)
- The agent interaction formalism source favors explicit protocols and capability boundaries. For this plugin, that means command handoff and review surfaces should come before direct write access. [Source: Agent Interaction Formalism](../sources/notes-agent-interaction-formalism.md)
- The agent skills source cluster supports packaging repeated procedures into explicit reusable workflows. The plugin can expose those workflows to the user without hiding the underlying CLI and playbooks. [Source: Agent Skills and Claude Code Cluster 2026-04-25](../sources/agent-skills-claude-code-cluster-2026-04-25.md)
- The local CLI now exposes a versioned JSON contract for `status`, `graph`, and `query`, which gives the plugin a structured integration surface without parsing markdown. [Source: llm-wiki JSON Contract 2026-04-25](../sources/llm-wiki-json-contract-2026-04-25.md)
- `search --json` extends the integration surface with structured page-discovery results and an empty-results state. [Source: llm-wiki Search JSON Contract 2026-04-25](../sources/llm-wiki-search-json-contract-2026-04-25.md)

## Candidate UI

- Side panel title: `Agent Workbench`
- Section: `Active Page`
- Section: `Related Context`
- Section: `Repo Health`
- Section: `Agent Handoff`
- Section: `Review Queue`

The panel should be dense and utilitarian. It is a workbench for repeated review, not a landing page.

## First Build Slice

- Parse active markdown file frontmatter.
- Extract wiki links from the active page.
- Show latest log entries.
- Run or prepare read-only search/status/query/graph commands, preferring JSON output for panel rendering.
- Never write files from the plugin.

## Current Implementation

The first skeleton exists under `tools/obsidian-agent-workbench/`. It implements:

- a desktop-only Obsidian plugin manifest
- a TypeScript plugin entry point
- an `Agent Workbench` side view
- active-page metadata display
- outbound link display from Obsidian metadata
- command-copy handoffs for `llm-wiki` JSON workflows
- settings for `llm-wiki` command and repository root

It remains read-only and copy-only. It does not execute shell commands or write wiki files. [Source: Obsidian Agent Workbench Skeleton 2026-04-26](../sources/obsidian-agent-workbench-skeleton-2026-04-26.md)

## Open Questions

- Should command execution happen inside Obsidian, or should the plugin only copy shell commands for now?
- Which JSON fields should be treated as stable plugin API versus internal CLI details?
- Should review queue data come from `git status`, `wiki/log.md`, or a dedicated agent-generated review file?
- Would an Obsidian Bases view be better than a custom side panel for dashboards over frontmatter?
- Should search results include match reasons before the first interactive plugin version?

## Related Pages

- [Obsidian](../entities/obsidian.md)
- [Local Agent Knowledge Base Operating Model](local-agent-knowledge-base-operating-model.md)
- [llm-wiki JSON Output Contract](llm-wiki-json-output-contract.md)
- [Source: Obsidian Agent Workbench Skeleton 2026-04-26](../sources/obsidian-agent-workbench-skeleton-2026-04-26.md)
- [LLM Wiki](../concepts/llm-wiki.md)
- [Ingest, Query, Lint](../concepts/ingest-query-lint.md)
- [Agent Runtime](../concepts/agent-runtime.md)
- [Agent Skills](../concepts/agent-skills.md)

## Citations

- [2026-04-25-obsidian-plugin-development.md](../../raw/sources/obsidian/2026-04-25-obsidian-plugin-development.md)
- [2026-04-25-obsidian-graph-view.md](../../raw/sources/obsidian/2026-04-25-obsidian-graph-view.md)
- [agent-interaction-formalism.md](../../raw/sources/notes/agent-interaction-formalism.md)
- [2026-04-25-agent-skills-claude-code-cluster.md](../../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md)
- [seed-llm-wiki-pattern.md](../../raw/sources/seed-llm-wiki-pattern.md)
- [2026-04-25-llm-wiki-json-contract.md](../../raw/sources/tooling/2026-04-25-llm-wiki-json-contract.md)
- [2026-04-25-llm-wiki-search-json-contract.md](../../raw/sources/tooling/2026-04-25-llm-wiki-search-json-contract.md)
- [2026-04-26-obsidian-agent-workbench-skeleton.md](../../raw/sources/tooling/2026-04-26-obsidian-agent-workbench-skeleton.md)
