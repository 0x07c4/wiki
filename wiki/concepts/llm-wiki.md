---
page_type: concept
status: active
last_updated: 2026-04-25
source_count: 2
---

# LLM Wiki

## Definition

An LLM Wiki is a persistent, interlinked markdown knowledge base maintained by an LLM on top of immutable raw sources.

## Why It Matters

The model does the bookkeeping that makes knowledge systems decay in normal use:

- summarizing each source
- updating related pages
- keeping links current
- preserving durable synthesis outside chat history

## Key Properties

- raw sources remain the ground truth
- the wiki is the working memory layer
- schema files such as `AGENTS.md` define disciplined behavior
- the knowledge base compounds instead of resetting on every query
- Obsidian can serve as the human workbench while the LLM maintains the markdown files, with built-in graph views exposing link structure

## Tensions

- automation is useful, but durable writebacks still need human review
- indexing can stay simple at small scale, but larger collections may need search tooling
- page structure should be consistent enough for maintenance without becoming rigid ceremony

## Related Pages

- [Seed Source: LLM Wiki Pattern](../sources/seed-llm-wiki-pattern.md)
- [Source: Obsidian Graph View 2026-04-25](../sources/obsidian-graph-view-2026-04-25.md)
- [Ingest, Query, Lint](ingest-query-lint.md)
- [Persistent Wiki vs Ad Hoc RAG](../synthesis/persistent-wiki-vs-ad-hoc-rag.md)
- [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)

## Citations

- [seed-llm-wiki-pattern.md](../../raw/sources/seed-llm-wiki-pattern.md)
- [2026-04-25-obsidian-graph-view.md](../../raw/sources/obsidian/2026-04-25-obsidian-graph-view.md)
