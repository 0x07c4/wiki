# Log

## [2026-04-10] bootstrap | repository scaffold

- created `raw/` and `wiki/` directory structure
- added `AGENTS.md` as the operating schema
- added `overview.md`, `index.md`, and `log.md`
- added seed source, concept, entity, and synthesis pages derived from `llm-wiki.md`

## [2026-04-10] source | seed source mapped

- treated `llm-wiki.md` as the initial seed note for the wiki
- extracted the core concept, workflow pattern, and first synthesis page

## [2026-04-10] ingest | seed raw source canonicalized

- copied `llm-wiki.md` into `raw/sources/seed-llm-wiki-pattern.md` as the formal immutable source
- updated wiki citations to point at the curated raw source path
- added `source_path` metadata guidance for future source summary pages

## [2026-04-10] tooling | local CLI added

- added a local `llm-wiki` CLI for `reindex`, `search`, `lint`, and `ingest-init`
- `wiki/index.md` can now be generated from the actual wiki instead of maintained by hand
- added tests covering indexing, search, lint checks, and source scaffold creation

## [2026-04-10] tooling | query and status commands added

- added `llm-wiki query` to assemble markdown context bundles with snippets and trace paths
- added `llm-wiki status` and `llm-wiki graph` for backlinks, hubs, orphan detection, and adjacency inspection
- expanded tests to cover query context and graph/status summaries
- tightened snippet selection to prefer evidence-bearing prose over navigation links
- switched `ingest-init` to scaffold from `templates/source-page.md` and refresh `wiki/index.md`

## [2026-04-25] schema | notes-to-wiki boundary codified

- documented `~/workspace/notes` as the upstream source of user thinking
- documented this repository as the compiled LLM-maintained knowledge layer
- added a notes-to-wiki checklist for importing selected notes as raw source snapshots

## [2026-04-25] ingest | agent interaction formalism note

- snapshotted `/home/chikee/workspace/notes/agent-interaction-formalism.md` into `raw/sources/notes/agent-interaction-formalism.md`
- added a source summary for the upstream note
- added concept pages for agent runtime and protocol machine
- added a synthesis page on agent runtime as a transaction layer
- updated the overview to include the notes-derived runtime track

## [2026-04-25] scouting | AI agent frontier radar

- created a curated web source pack for recent AI agent progress across models, runtime platforms, skills, standards, and evaluations
- added a source summary for the scouting pack
- added concept pages for agent skills and agent evaluation
- updated the agent runtime concept with current product-infrastructure evidence
- added an AI agent frontier radar synthesis with a prioritized ingest queue

## [2026-04-25] ingest | agent skills and Claude Code cluster

- added a curated source pack for Agent Skills, Claude Code skills docs, Anthropic's engineering blog, the Agent Skills open standard, and Anthropic's public skills repository
- deepened the agent skills concept with Claude Code invocation, permissions, and quality signals
- added a synthesis page defining what makes a good agent skill
- updated the frontier radar ingest queue to continue toward a curated skill repository watchlist

## [2026-04-25] schema | local agent knowledge base objective clarified

- clarified that this repository is a local knowledge base for agents, not only a passive markdown wiki
- documented search, query, graph, lint, ingest, templates, and playbooks as part of the usable operating surface
- updated the overview to emphasize agent comprehension, traceability, and future-agent reuse

## [2026-04-25] schema | Obsidian workspace layer clarified

- elevated Obsidian from an optional viewer to the human-facing workspace for browsing, graph inspection, and writeback review
- documented Obsidian plugins as a possible workflow extension layer for source intake, dashboards, presentation, and agent handoff
- updated the seed source summary and core wiki concept to reflect Obsidian's role in the operating model

## [2026-04-25] source | Obsidian native graph clarified

- added an Obsidian Graph view source note confirming graph navigation as a native core-plugin capability
- updated the Obsidian entity to distinguish built-in global/local graph views from optional workflow plugins
- updated the overview and README to describe Obsidian as the human-facing graph navigator for this markdown knowledge base

## [2026-04-25] synthesis | local agent knowledge base operating model

- added an Obsidian workbench checklist for human review, graph navigation, and plugin-extension decisions
- added a synthesis page defining the four-layer model: evidence, compiled knowledge, agent operation, and human navigation
- updated `AGENTS.md`, `README.md`, and the overview so future agents treat Obsidian and CLI tooling as first-class parts of the system

## [2026-04-25] synthesis | Obsidian Agent Workbench MVP

- added an Obsidian plugin-development source note from official developer docs
- added a source summary for Obsidian plugin capabilities and development constraints
- added a synthesis page defining a read-first Obsidian Agent Workbench MVP for active-page context, repo health, and agent handoff
- updated the overview, README, Obsidian entity, and operating-model synthesis with the plugin direction

## [2026-04-25] tooling | JSON output for Obsidian integration

- added `--json` output to `llm-wiki status`, `llm-wiki graph`, and `llm-wiki query`
- added tests for machine-readable status, graph, and query payloads
- updated the Obsidian workbench docs to prefer structured CLI output for future plugin panels

## [2026-04-25] synthesis | llm-wiki JSON output contract

- added `schema_version` and `command` fields to JSON payloads
- captured the implemented `status`, `graph`, and `query` JSON fields in a local source note
- added a synthesis page defining schema version `1` as the first plugin integration contract
- linked the Obsidian Agent Workbench MVP to the JSON contract

## [2026-04-25] tooling | search JSON output

- added `--json` output to `llm-wiki search`
- added tests for normal search results and empty result payloads
- added a search JSON source note and expanded the JSON output contract to include search results
