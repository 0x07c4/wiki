---
page_type: overview
status: seed
last_updated: 2026-04-10
source_count: 1
---

# Overview

This wiki tracks a single core idea: use an LLM to maintain a persistent markdown knowledge base instead of rediscovering knowledge from raw documents on every query.

## Current Thesis

A maintained wiki can outperform ad hoc retrieval when the work requires repeated synthesis across many sources. The value comes from persistent structure:

- source summaries are already written
- cross-references already exist
- contradictions can be tracked over time
- durable analyses can be filed back into the wiki

## Active Concepts

- [LLM Wiki](concepts/llm-wiki.md)
- [Ingest, Query, Lint](concepts/ingest-query-lint.md)

## Active Entities

- [Obsidian](entities/obsidian.md)

## Durable Synthesis

- [Persistent Wiki vs Ad Hoc RAG](synthesis/persistent-wiki-vs-ad-hoc-rag.md)

## Seed Source

- [Seed Source: LLM Wiki Pattern](sources/seed-llm-wiki-pattern.md)

## Open Questions

- What metadata conventions are worth standardizing across all page types?
- At what scale does plain index navigation stop being enough?
- Which parts of ingest should stay explicitly human-reviewed?

## Citations

- [seed-llm-wiki-pattern.md](../raw/sources/seed-llm-wiki-pattern.md)
