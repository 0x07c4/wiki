# llm-wiki Search JSON Contract Source Note

Captured: 2026-04-25
Purpose: record the implemented JSON output surface for `llm-wiki search --json`.

This is a local implementation source note. It captures the behavior implemented in the repository code and tests at the time of writing.

## Implementation Inputs

- `src/llm_wiki/cli.py`
  - `search --json`

- `src/llm_wiki/search.py`
  - `search_results_to_dict`
  - `render_search_json`
  - `search_command(..., json_output=True)`

- `tests/test_indexing.py`
  - machine-readable search payload assertions
  - empty-result payload assertions

## Captured Contract

`llm-wiki search "<query>" --json` includes:

- `schema_version`: currently `"1"`
- `command`: `search`
- `query`
- `results`

Stable result fields:

- `rank`
- `path`
- `title`
- `page_type`
- `score`
- `summary`
- `source_path`

## Integration Reading

- Obsidian Agent Workbench can use `search --json` for active-page related lookup and quick page discovery.
- Empty result sets are represented as `results: []`, which gives UI consumers a normal empty state instead of a command failure path.
- Schema version `1` matches the existing JSON output family for `status`, `graph`, and `query`.
