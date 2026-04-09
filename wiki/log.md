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
