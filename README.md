# Agent Knowledge Wiki

This repository is a local knowledge base for AI agents.

It turns the idea in [llm-wiki.md](llm-wiki.md) into a maintained markdown knowledge layer plus practical tooling for locating, understanding, and updating that knowledge.

The goal is not to build a chat app or a passive note archive. The goal is to give future agents a reliable local reference system that compounds over time:

- raw sources stay immutable
- the wiki is the maintained, agent-readable knowledge layer
- `AGENTS.md` is the operating schema for agent behavior
- the CLI, playbooks, templates, index, log, and graph views are part of the system's usable surface
- Obsidian is the human-facing workspace for reading, reviewing, and using built-in graph views over the maintained markdown

## Repository layout

- `llm-wiki.md`: the original idea note that seeded this repo
- `raw/inbox/`: new sources waiting to be processed
- `raw/sources/`: curated raw sources after ingest
- `raw/assets/`: downloaded images or attachments referenced by raw sources
- `templates/`: starter page templates for future wiki pages
- `playbooks/`: operational checklists for ingest and lint
- `wiki/overview.md`: the top-level entry point for the maintained wiki
- `wiki/index.md`: content-oriented catalog of pages
- `wiki/log.md`: append-only record of ingests, queries, and lint passes
- `wiki/sources/`: one page per source
- `wiki/entities/`: people, companies, tools, projects
- `wiki/concepts/`: concepts, methods, recurring ideas
- `wiki/synthesis/`: cross-source analysis and durable writebacks

## Default workflow

1. Put a new source into `raw/inbox/`.
2. Ask the LLM to ingest it using the rules in [AGENTS.md](AGENTS.md).
3. Move the source into `raw/sources/` once it becomes part of the curated collection.
4. Let the LLM update source summaries, concept pages, entity pages, `wiki/index.md`, and `wiki/log.md`.
5. Ask questions against the maintained wiki and local query tools, not just against raw files.
6. Promote durable answers into `wiki/synthesis/` after review.
7. Improve tooling when repeated agent work shows that search, navigation, ingest, or linting is too slow or ambiguous.

## Relationship to `~/workspace/notes`

This repository can use `~/workspace/notes` as an upstream source, but the two repos have different jobs:

- `~/workspace/notes` is the user's personal thinking and decision entry point.
- this wiki is the LLM-maintained compiled knowledge layer.

Selected stable notes can be snapshotted into `raw/sources/notes/` and ingested like any other source. The wiki may produce synthesis pages from those notes and other sources, but writeback into `~/workspace/notes` should only happen after explicit user confirmation.

## Obsidian layer

Obsidian is treated as the human workbench for this repo:

- read wiki pages while the agent edits them
- follow links and inspect graph structure through Obsidian's built-in global and local graph views
- use Web Clipper-style flows to bring external sources into markdown
- use plugins such as Dataview or Marp when frontmatter queries or generated presentations are useful
- evaluate whether a purpose-built Obsidian plugin would make source intake, graph navigation, review, or agent handoff smoother

## Operational Files

- [playbooks/ingest-checklist.md](playbooks/ingest-checklist.md): default runbook for source ingest
- [playbooks/lint-checklist.md](playbooks/lint-checklist.md): default runbook for wiki health checks
- [playbooks/notes-to-wiki-checklist.md](playbooks/notes-to-wiki-checklist.md): runbook for importing selected notes as sources
- [playbooks/obsidian-workbench-checklist.md](playbooks/obsidian-workbench-checklist.md): runbook for using Obsidian as the human review and graph navigation layer
- [templates/source-page.md](templates/source-page.md): source summary template
- [templates/concept-page.md](templates/concept-page.md): concept page template
- [templates/entity-page.md](templates/entity-page.md): entity page template
- [templates/synthesis-page.md](templates/synthesis-page.md): synthesis page template

## Seed content

This starter already includes a small seed wiki derived from [llm-wiki.md](llm-wiki.md) and canonicalized as a raw source at [raw/sources/seed-llm-wiki-pattern.md](raw/sources/seed-llm-wiki-pattern.md):

- [overview](wiki/overview.md)
- [source summary](wiki/sources/seed-llm-wiki-pattern.md)
- [core concept](wiki/concepts/llm-wiki.md)
- [workflow concept](wiki/concepts/ingest-query-lint.md)
- [entity page](wiki/entities/obsidian.md)
- [synthesis page](wiki/synthesis/persistent-wiki-vs-ad-hoc-rag.md)

## Operating model

The current operating model is captured in [Local Agent Knowledge Base Operating Model](wiki/synthesis/local-agent-knowledge-base-operating-model.md):

- `raw/` is the evidence layer
- `wiki/` is the compiled knowledge layer
- `llm-wiki`, playbooks, templates, and `AGENTS.md` are the agent operation layer
- Obsidian is the human navigation and review layer
- plugins extend intake, dashboards, review, presentation, or handoff when repeated friction justifies them

The first concrete plugin direction is captured in [Obsidian Agent Workbench MVP](wiki/synthesis/obsidian-agent-workbench-mvp.md). Its first version should be read-first: active-page context, repo health, and agent handoff before direct writeback.

The machine-readable CLI contract is captured in [llm-wiki JSON Output Contract](wiki/synthesis/llm-wiki-json-output-contract.md). Tool consumers should prefer `--json` output and treat `schema_version: "1"` as the initial integration contract.

## Next expansion

- continue ingesting high-value agent-field sources one at a time
- maintain synthesis pages that help future agents decide what matters
- tighten `AGENTS.md` when the workflow shows friction
- stabilize the JSON fields that an Obsidian Agent Workbench would consume
- decide whether search results need matched-field explanations before plugin implementation

## CLI

This repo now ships with a local CLI entrypoint:

```bash
python3 -m pip install -e .
llm-wiki --help
```

Core commands in this repository:

- `llm-wiki reindex`
- `llm-wiki search <query>`
- `llm-wiki query <question>`
- `llm-wiki lint`
- `llm-wiki ingest-init <source>`
- `llm-wiki status`
- `llm-wiki graph`

The intent is pragmatic:

- `reindex` keeps `wiki/index.md` generated from the actual wiki
- `search` gives the LLM a cheap local discovery tool; `--json` returns machine-readable results
- `query` assembles an LLM-ready markdown or JSON context bundle with traceable snippets
- `lint` catches structural drift before it compounds
- `ingest-init` canonicalizes raw sources, scaffolds source pages from the repo template, and refreshes `wiki/index.md`
- `status` shows counts, hubs, backlinks, and orphan pages; `--json` returns machine-readable output
- `graph` prints simple adjacency so link structure is visible in plain text; `--json` returns nodes, edges, and adjacency

Example usage:

```bash
llm-wiki reindex
llm-wiki search "llm wiki"
llm-wiki search "Obsidian Agent Workbench" --json
llm-wiki query "What is the core difference between a persistent wiki and ad hoc RAG?"
llm-wiki query "Obsidian Agent Workbench" --json
llm-wiki lint
llm-wiki ingest-init raw/inbox/new-article.md
llm-wiki status
llm-wiki status --json
llm-wiki graph
llm-wiki graph --json
```
