---
page_type: source
status: ingested
last_updated: 2026-04-25
source_count: 1
source_path: ../../raw/sources/obsidian/2026-04-25-obsidian-graph-view.md
---

# Source: Obsidian Graph View 2026-04-25

## Summary

This source note confirms that Obsidian has native graph capability through its core Graph view. It matters because this repo's human-facing layer should treat graph navigation as a built-in Obsidian affordance, while positioning additional plugins as workflow extensions.

## Key Claims

- Graph view is a core Obsidian plugin that visualizes note relationships in a vault.
- Notes appear as nodes, and internal links appear as edges.
- Local Graph shows notes connected to the active note and can vary connection depth.
- Obsidian stores notes as local Markdown files and maintains metadata that powers features such as Graph view.

## Evidence Notes

- Graph view supports filters, groups, display controls, and force controls.
- Local Graph is distinct from global Graph view: it starts from the active note's neighborhood.
- For this wiki, the native graph is a human navigation surface over links that agents maintain in markdown.

## Related Pages

- [Obsidian](../entities/obsidian.md)
- [LLM Wiki](../concepts/llm-wiki.md)

## Open Questions

- Which Obsidian plugins best complement the native graph for review, dashboards, and agent handoff?
- Should this repo eventually include an `.obsidian/` recommended workspace profile, or keep editor configuration outside the repo?

## Citations

- [2026-04-25-obsidian-graph-view.md](../../raw/sources/obsidian/2026-04-25-obsidian-graph-view.md)
