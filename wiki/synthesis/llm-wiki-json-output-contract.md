---
page_type: synthesis
status: active
last_updated: 2026-04-25
source_count: 2
---

# llm-wiki JSON Output Contract

## Question

What JSON contract should tool consumers use for `llm-wiki search`, `status`, `graph`, and `query`?

## Short Answer

Use `schema_version: "1"` as the initial machine-readable contract for `llm-wiki search --json`, `llm-wiki status --json`, `llm-wiki graph --json`, and `llm-wiki query --json`.

The contract is intentionally small. It gives Obsidian Agent Workbench enough structure to render search results, repo health, graph context, and query context without parsing human-readable markdown.

## Contract Rules

- All payloads include `schema_version` and `command`.
- Consumers should treat listed fields as stable for schema version `1`.
- Producers may add optional fields without changing the schema version.
- Producers should not remove or rename stable fields without incrementing `schema_version`.
- Consumers should ignore unknown fields.

## `search --json`

Top-level fields:

- `schema_version`
- `command`
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

Empty result sets are represented as `results: []`.

## `status --json`

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

## `graph --json`

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

## `query --json`

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

## Implications

- Obsidian Agent Workbench can render search results, active-page context, repo health, graph edges, and query snippets from structured data.
- The plugin should prefer JSON output over parsing markdown.
- Test coverage should guard the stable fields used by downstream consumers.
- Future CLI changes should distinguish additive fields from breaking schema changes.

## Open Questions

- Should JSON examples be committed as fixtures?
- Should command output include an absolute or repo-relative `repo_root` field?
- Should query snippets include end line numbers as well as start line numbers?
- Should search results include match reasons or matched fields?

## Related Pages

- [Source: llm-wiki JSON Contract 2026-04-25](../sources/llm-wiki-json-contract-2026-04-25.md)
- [Source: llm-wiki Search JSON Contract 2026-04-25](../sources/llm-wiki-search-json-contract-2026-04-25.md)
- [Obsidian Agent Workbench MVP](obsidian-agent-workbench-mvp.md)
- [Local Agent Knowledge Base Operating Model](local-agent-knowledge-base-operating-model.md)
- [Ingest, Query, Lint](../concepts/ingest-query-lint.md)

## Citations

- [2026-04-25-llm-wiki-json-contract.md](../../raw/sources/tooling/2026-04-25-llm-wiki-json-contract.md)
- [2026-04-25-llm-wiki-search-json-contract.md](../../raw/sources/tooling/2026-04-25-llm-wiki-search-json-contract.md)
