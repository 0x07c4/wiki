# llm-wiki JSON Output Contract Source Note

Captured: 2026-04-25  
Purpose: record the implemented JSON output surface for `llm-wiki status`, `llm-wiki graph`, and `llm-wiki query`.

This is a local implementation source note. It captures the behavior implemented in the repository code and tests at the time of writing.

## Implementation Inputs

- `src/llm_wiki/cli.py`
  - `status --json`
  - `graph --json`
  - `query --json`

- `src/llm_wiki/status.py`
  - `status_to_dict`
  - `graph_to_dict`
  - `format_status_json`
  - `format_graph_json`

- `src/llm_wiki/querying.py`
  - `query_context_to_dict`
  - `render_query_context_json`

- `tests/test_status.py`
  - machine-readable status and graph payload assertions

- `tests/test_querying.py`
  - machine-readable query payload assertions

## Captured Contract

All JSON payloads include:

- `schema_version`: currently `"1"`
- `command`: one of `status`, `graph`, or `query`

### `llm-wiki status --json`

Top-level fields:

- `schema_version`
- `command`
- `counts`
- `raw`
- `page_types`
- `hubs`
- `orphans`
- `graph`

Stable node fields in `hubs`, `orphans`, and `graph`:

- `path`
- `title`
- `page_type`
- `backlinks`
- `outbound`
- `outbound_targets`

### `llm-wiki graph --json`

Top-level fields:

- `schema_version`
- `command`
- `nodes`
- `edges`
- `adjacency`

Stable node fields:

- `path`
- `title`
- `page_type`
- `backlinks`
- `outbound`

Stable edge fields:

- `source`
- `target`

### `llm-wiki query "<question>" --json`

Top-level fields:

- `schema_version`
- `command`
- `query`
- `selected_pages`
- `notes`

Stable selected page fields:

- `rank`
- `title`
- `path`
- `page_type`
- `score`
- `summary`
- `source_path`
- `snippets`

Stable snippet fields:

- `line_number`
- `text`

## Integration Reading

- Obsidian Agent Workbench should consume these JSON payloads before parsing markdown output.
- Schema version `1` means fields listed above should be treated as the initial plugin integration contract.
- New optional fields can be added without changing the schema version.
- Removing or renaming stable fields should require a schema version change and test updates.
