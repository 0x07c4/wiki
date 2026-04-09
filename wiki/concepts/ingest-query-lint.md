---
page_type: concept
status: active
last_updated: 2026-04-10
source_count: 1
---

# Ingest, Query, Lint

## Definition

This is the core operating loop for a maintained wiki.

## Ingest

Read a new source, create or update its source summary page, propagate the new information into concept or entity pages, then update the index and log.

## Query

Answer questions from the maintained wiki first. If the answer creates a durable artifact such as a comparison or thesis, propose filing it into `wiki/synthesis/`.

## Lint

Inspect the wiki for contradictions, stale claims, missing pages, weak cross-references, or synthesis that no longer matches the evidence.

## Why This Matters

Without an explicit operating loop, the wiki becomes either:

- a passive dump of source summaries, or
- a generic chat session with no durable structure

The loop is what keeps the knowledge base alive.

## Related Pages

- [LLM Wiki](llm-wiki.md)
- [Seed Source: LLM Wiki Pattern](../sources/seed-llm-wiki-pattern.md)

## Citations

- [seed-llm-wiki-pattern.md](../../raw/sources/seed-llm-wiki-pattern.md)
