---
page_type: source
status: ingested
last_updated: 2026-04-25
source_count: 1
source_path: ../../raw/sources/tooling/2026-04-25-llm-wiki-search-json-contract.md
---

# Source: llm-wiki Search JSON Contract 2026-04-25

## Summary

This local source note captures the implemented JSON output contract for `llm-wiki search --json`. It matters because the Obsidian Agent Workbench needs structured page-discovery results for active-page lookup and quick navigation.

## Key Claims

- `search --json` emits `schema_version: "1"` and `command: "search"`.
- The payload includes the original `query` and a `results` list.
- Each result includes rank, path, title, page type, score, summary, and source path.
- Empty result sets are represented as `results: []`.

## Evidence Notes

- The contract is implemented in `src/llm_wiki/search.py`.
- The CLI exposes the flag through `src/llm_wiki/cli.py`.
- Tests in `tests/test_indexing.py` assert normal search payloads and empty-result payloads.

## Related Pages

- [llm-wiki JSON Output Contract](../synthesis/llm-wiki-json-output-contract.md)
- [Obsidian Agent Workbench MVP](../synthesis/obsidian-agent-workbench-mvp.md)
- [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)

## Open Questions

- Should search results include match reasons or matched fields?
- Should search output include the requested `limit`?
- Should search support active-page related search as a first-class mode?

## Citations

- [2026-04-25-llm-wiki-search-json-contract.md](../../raw/sources/tooling/2026-04-25-llm-wiki-search-json-contract.md)
