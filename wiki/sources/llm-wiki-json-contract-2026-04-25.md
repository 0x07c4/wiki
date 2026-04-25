---
page_type: source
status: ingested
last_updated: 2026-04-25
source_count: 1
source_path: ../../raw/sources/tooling/2026-04-25-llm-wiki-json-contract.md
---

# Source: llm-wiki JSON Contract 2026-04-25

## Summary

This local source note captures the implemented JSON output contract for `llm-wiki status --json`, `llm-wiki graph --json`, and `llm-wiki query --json`. It matters because the future Obsidian Agent Workbench needs a stable machine-readable surface instead of scraping human-readable markdown output.

## Key Claims

- JSON payloads include `schema_version` and `command`.
- `status --json` exposes counts, raw file lists, page type counts, hubs, orphans, and graph node records.
- `graph --json` exposes nodes, edges, and adjacency.
- `query --json` exposes selected pages, scores, provenance paths, summaries, and snippets.
- Schema version `1` should be treated as the first plugin integration contract.

## Evidence Notes

- The contract is implemented in `src/llm_wiki/status.py` and `src/llm_wiki/querying.py`.
- The CLI exposes the flags through `src/llm_wiki/cli.py`.
- Tests in `tests/test_status.py` and `tests/test_querying.py` assert machine-readable payload fields.

## Related Pages

- [llm-wiki JSON Output Contract](../synthesis/llm-wiki-json-output-contract.md)
- [Obsidian Agent Workbench MVP](../synthesis/obsidian-agent-workbench-mvp.md)
- [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)

## Open Questions

- Which optional fields should be added before an Obsidian plugin consumes this contract?
- Should `search` also gain JSON output?
- Should schema validation fixtures be stored under `tests/fixtures/`?

## Citations

- [2026-04-25-llm-wiki-json-contract.md](../../raw/sources/tooling/2026-04-25-llm-wiki-json-contract.md)
