---
page_type: source
status: ingested
last_updated: 2026-04-26
source_count: 1
source_path: ../../raw/sources/tooling/2026-04-26-obsidian-agent-workbench-json-copy.md
---

# Source: Obsidian Agent Workbench JSON Copy 2026-04-26

## Summary

This local source note captures the first interactive read-only iteration of the Obsidian Agent Workbench plugin. It matters because the plugin now reduces handoff friction by copying actual `llm-wiki` JSON output, while still avoiding wiki writeback or raw-source mutation.

## Key Claims

- Related-context links in the side panel can open existing Obsidian pages.
- JSON buttons run safe local `llm-wiki` read commands and copy stdout.
- The default command path uses the current repo's `src` through `python3 -m llm_wiki.cli`, so a global `llm-wiki` install is not required.
- If command execution fails, the plugin falls back to copying the shell command.
- The plugin remains read-only and does not edit `raw/`, `wiki/`, or `.obsidian/`.

## Evidence Notes

- `src/main.ts` implements the local CLI invocation, JSON-copy path, command-copy fallback, and clickable links.
- `esbuild.config.mjs` externalizes Node built-ins required by desktop command execution.
- `README.md` now documents the read-only JSON-copy boundary.
- Typecheck, build, local CLI JSON output, and standard-library tests passed.

## Related Pages

- [Obsidian Agent Workbench MVP](../synthesis/obsidian-agent-workbench-mvp.md)
- [llm-wiki JSON Output Contract](../synthesis/llm-wiki-json-output-contract.md)
- [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)
- [Obsidian](../entities/obsidian.md)

## Open Questions

- Should future versions render JSON results inside the panel instead of only copying them?
- Should review queue data come from `git status`, `wiki/log.md`, or a dedicated generated file?

## Citations

- [2026-04-26-obsidian-agent-workbench-json-copy.md](../../raw/sources/tooling/2026-04-26-obsidian-agent-workbench-json-copy.md)
