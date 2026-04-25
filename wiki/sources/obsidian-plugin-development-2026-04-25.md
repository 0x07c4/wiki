---
page_type: source
status: ingested
last_updated: 2026-04-25
source_count: 1
source_path: ../../raw/sources/obsidian/2026-04-25-obsidian-plugin-development.md
---

# Source: Obsidian Plugin Development 2026-04-25

## Summary

This source note captures official Obsidian developer facts needed to scope a possible Agent Workbench plugin for this wiki. It confirms that plugins extend Obsidian with TypeScript, can add user-facing actions, and can create custom data views, while warning that plugin development should happen in a separate vault and custom views must respect Obsidian's lazy view behavior.

## Key Claims

- Obsidian plugins extend the app using TypeScript.
- A plugin includes metadata in `manifest.json`.
- Plugins can add ribbon icons and command-palette actions.
- Bases is a core plugin for dynamic views over notes, and plugins can create custom Bases views.
- Obsidian recommends developing plugins in a separate vault to avoid damaging a main vault.
- Since Obsidian v1.7.2, custom view interaction needs to account for deferred views.

## Evidence Notes

- A plugin panel for this wiki should start as read-first navigation and command handoff, not direct autonomous writeback.
- Custom dashboard views are plausible, but they must be designed for large vaults and avoid unnecessary rendering.
- Safe development requires a separate test vault before enabling the plugin in this repository.

## Related Pages

- [Obsidian](../entities/obsidian.md)
- [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)
- [Obsidian Agent Workbench MVP](../synthesis/obsidian-agent-workbench-mvp.md)

## Open Questions

- Should the first implementation be a normal side panel, a Bases view, or only command-palette actions?
- Which CLI commands should be callable from Obsidian without creating unsafe writeback paths?

## Citations

- [2026-04-25-obsidian-plugin-development.md](../../raw/sources/obsidian/2026-04-25-obsidian-plugin-development.md)
