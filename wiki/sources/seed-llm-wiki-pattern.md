---
page_type: source
status: ingested
last_updated: 2026-04-10
source_count: 1
source_path: ../../raw/sources/seed-llm-wiki-pattern.md
---

# Seed Source: LLM Wiki Pattern

## Summary

The seed note argues that a useful knowledge system should not rely on re-reading raw documents from scratch for every question. Instead, an LLM should continuously maintain a structured wiki that accumulates summaries, cross-references, contradictions, and synthesis over time.

## Key Claims

- persistent markdown pages are a better long-term artifact than transient chat answers
- the wiki should sit between the user and raw sources
- ingest, query, and lint should be treated as first-class operations
- index and log files give the system enough structure to operate without heavyweight infrastructure at small scale

## Related Pages

- [LLM Wiki](../concepts/llm-wiki.md)
- [Ingest, Query, Lint](../concepts/ingest-query-lint.md)
- [Persistent Wiki vs Ad Hoc RAG](../synthesis/persistent-wiki-vs-ad-hoc-rag.md)
- [Obsidian](../entities/obsidian.md)

## Open Questions

- Which file conventions should become mandatory versus optional?
- When should a query answer become a durable synthesis page?
- Which maintenance tasks need explicit human approval?

## Citations

- [seed-llm-wiki-pattern.md](../../raw/sources/seed-llm-wiki-pattern.md)
