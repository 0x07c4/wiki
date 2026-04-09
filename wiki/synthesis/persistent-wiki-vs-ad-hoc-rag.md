---
page_type: synthesis
status: draft
last_updated: 2026-04-10
source_count: 1
---

# Persistent Wiki vs Ad Hoc RAG

## Question

Why maintain a wiki at all instead of answering directly from raw sources every time?

## Short Answer

Because the expensive part of knowledge work is not just retrieval. It is maintaining synthesis over time.

## Evidence

- ad hoc retrieval forces the model to rediscover structure on every query
- repeated synthesis across many documents is costly and fragile if nothing is persisted
- a maintained wiki stores summaries, links, contradictions, and prior conclusions in reusable form
- durable answers can themselves become part of the knowledge base

## Implications

- the system gets better as more sources are ingested
- repeated questions become cheaper to answer
- the human can spend more time on curation and judgment, less on bookkeeping

## Limits

- this only works if the wiki is actually maintained
- low-quality writebacks can compound bad structure
- larger corpora may still need better search than a hand-maintained index

## Related Pages

- [LLM Wiki](../concepts/llm-wiki.md)
- [Ingest, Query, Lint](../concepts/ingest-query-lint.md)
- [Seed Source: LLM Wiki Pattern](../sources/seed-llm-wiki-pattern.md)

## Citations

- [seed-llm-wiki-pattern.md](../../raw/sources/seed-llm-wiki-pattern.md)
