# Obsidian Agent Workbench

Read-only Obsidian plugin skeleton for this `llm-wiki` repository.

The plugin is intentionally narrow:

- shows active markdown page metadata
- shows outbound links known to Obsidian
- prepares safe `llm-wiki` JSON commands
- avoids writing to `raw/`, `wiki/`, or `.obsidian/`

## Development

```bash
npm install
npm run typecheck
npm run build
```

Build output is `main.js` in this directory. It is ignored by git.

## Commands

- `Open Agent Workbench`
- `Refresh Agent Workbench`
- `Copy llm-wiki status command`
- `Copy llm-wiki search command for active page`

## Settings

- `llm-wiki command`: defaults to `llm-wiki`
- `Repository root`: optional override; when empty, the plugin uses the vault base path on desktop

## Boundary

This plugin is a read-only workbench. It does not run writeback, edit wiki pages, or modify raw sources.
