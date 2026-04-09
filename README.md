# LLM Wiki Starter

This repository turns the idea in [llm-wiki.md](llm-wiki.md) into a minimal working skeleton.

The goal is not to build a chat app. The goal is to maintain a persistent markdown wiki that compounds over time:

- raw sources stay immutable
- the wiki is the maintained knowledge layer
- `AGENTS.md` is the operating schema for the LLM

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
5. Ask questions against the wiki, not just against raw files.
6. Promote durable answers into `wiki/synthesis/` after review.

## Operational Files

- [playbooks/ingest-checklist.md](playbooks/ingest-checklist.md): default runbook for source ingest
- [playbooks/lint-checklist.md](playbooks/lint-checklist.md): default runbook for wiki health checks
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

## Next expansion

- add 2 to 3 real raw sources
- ingest them one at a time
- tighten `AGENTS.md` when the workflow shows friction
- add tooling only after the manual workflow is stable

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
- `search` gives the LLM a cheap local discovery tool
- `query` assembles an LLM-ready markdown context bundle with traceable snippets
- `lint` catches structural drift before it compounds
- `ingest-init` canonicalizes raw sources, scaffolds source pages from the repo template, and refreshes `wiki/index.md`
- `status` shows counts, hubs, backlinks, and orphan pages
- `graph` prints simple adjacency so link structure is visible in plain text

Example usage:

```bash
llm-wiki reindex
llm-wiki search "llm wiki"
llm-wiki query "What is the core difference between a persistent wiki and ad hoc RAG?"
llm-wiki lint
llm-wiki ingest-init raw/inbox/new-article.md
llm-wiki status
llm-wiki graph
```
