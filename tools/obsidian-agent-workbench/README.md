# Obsidian Agent Workbench

Read-only Obsidian plugin for this `llm-wiki` repository.

The plugin is intentionally narrow:

- shows active markdown page metadata
- shows outbound links known to Obsidian and opens existing linked pages
- renders a compact repo health summary from `llm-wiki status --json`
- copies safe `llm-wiki` JSON output for agent handoff
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
- `Copy llm-wiki status JSON`
- `Copy llm-wiki search JSON for active page`

## Settings

- `llm-wiki command`: optional override. Leave blank to run the local repo CLI with `python3 -m llm_wiki.cli` and `PYTHONPATH=src`.
- `Repository root`: optional override; when empty, the plugin uses the vault base path on desktop

## Boundary

This plugin is a read-only workbench. It can run safe local read commands and copy their output, but it does not run writeback, edit wiki pages, or modify raw sources.
