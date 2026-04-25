# Obsidian Plugin Development Source Note

Captured: 2026-04-25  
Purpose: capture official Obsidian developer facts needed to scope a possible Agent Workbench plugin or panel for this wiki.

This is a curated source note, not a full mirror of external pages. External pages remain the source of record.

## Sources

- Obsidian Developer Docs, "Home".
  URL: https://docs.obsidian.md/Home
  Captured facts:
  - Obsidian Developer Docs cover building plugins and themes.
  - Plugins extend Obsidian using TypeScript.

- Obsidian Developer Docs, "Build a plugin".
  URL: https://docs.obsidian.md/Plugins/Getting%20started/Build%20a%20plugin
  Captured facts:
  - Plugin development uses a sample plugin, Node.js, and a build step.
  - Obsidian recommends using a separate vault for plugin development to avoid data loss in the main vault.
  - A plugin has a `manifest.json` with metadata such as `id`, `name`, and `description`.
  - Plugins can add ribbon icons and commands.

- Obsidian Developer Docs, "Build a Bases view".
  URL: https://docs.obsidian.md/plugins/guides/bases-view
  Captured facts:
  - Bases is a core plugin for dynamic views over notes, including tables, cards, lists, and more.
  - Plugins can use the Obsidian API to create custom views of data powering Bases.
  - Custom Bases views should handle many entries efficiently and avoid unnecessary rendering.

- Obsidian Developer Docs, "Defer views".
  URL: https://docs.obsidian.md/plugins/guides/defer-views
  Captured facts:
  - Since Obsidian v1.7.2, views are created as `DeferredView` at load and switched to the concrete view when visible.
  - Plugins that communicate with custom views should account for visibility and check the concrete view instance.
  - Manually loading deferred views can hurt performance and should be used sparingly.

## Initial Reading

- A future Obsidian Agent Workbench should start as a narrow plugin or view, not a broad replacement for Obsidian's native graph and markdown navigation.
- The MVP should prioritize navigation, status, and command handoff before editing wiki files directly.
- Development should happen in a separate vault until the plugin is safe enough to use against this repo.
- If the plugin adds custom views, it should respect Obsidian's deferred-view behavior and avoid expensive full-vault rendering.
