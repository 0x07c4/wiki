---
page_type: source
status: ingested
last_updated: 2026-04-26
source_count: 1
source_path: ../../raw/sources/tooling/2026-04-26-obsidian-agent-workbench-status-panel.md
---

# Source: Obsidian Agent Workbench Status Panel 2026-04-26

## Summary

This local source note captures the first in-panel rendering of `llm-wiki status --json` inside the Obsidian Agent Workbench. It matters because repo health is now visible directly in Obsidian instead of requiring the user to inspect copied JSON.

## Key Claims

- The `Repo Health` section renders raw source count, wiki page count, inbox count, orphan count, and top hubs.
- Status loading is asynchronous and guards against stale render results.
- Top hub entries can open the corresponding vault files.
- JSON copy buttons remain available for agent handoff.
- The plugin remains read-only and does not edit `raw/`, `wiki/`, or `.obsidian/`.

## Evidence Notes

- `src/main.ts` adds status payload types, `readStatus()`, async repo-health rendering, and clickable hub links.
- `styles.css` adds compact dashboard styling.
- `README.md` documents the repo health summary.
- TypeScript typecheck passed.

## Related Pages

- [Obsidian Agent Workbench MVP](../synthesis/obsidian-agent-workbench-mvp.md)
- [llm-wiki JSON Output Contract](../synthesis/llm-wiki-json-output-contract.md)
- [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)
- [Obsidian](../entities/obsidian.md)

## Open Questions

- Should the review queue be rendered from `git status`, recent `wiki/log.md`, or a dedicated review artifact?
- Should `search` and `query` JSON also render previews directly in the panel?

## Citations

- [2026-04-26-obsidian-agent-workbench-status-panel.md](../../raw/sources/tooling/2026-04-26-obsidian-agent-workbench-status-panel.md)
