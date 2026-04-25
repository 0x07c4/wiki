# Obsidian Workbench Checklist

Use this when the user is browsing, reviewing, or steering this wiki from Obsidian.

## Boundary

- Treat Obsidian as the human-facing workspace.
- Treat the CLI and `AGENTS.md` workflows as the agent-facing operation layer.
- Treat `raw/` as evidence and `wiki/` as the maintained knowledge layer.
- Do not commit `.obsidian/` settings or plugin configuration unless the user explicitly asks.

## Before Review

- read `wiki/index.md`
- read `wiki/overview.md`
- scan the latest entries in `wiki/log.md`
- identify the pages changed by the current task
- run `llm-wiki status` when link structure, hubs, or orphan pages matter

## Human Navigation Loop

- start from `wiki/overview.md` for the current thesis
- use `wiki/index.md` for page discovery
- use Obsidian's built-in Graph view to inspect vault-wide link shape
- use Obsidian's Local Graph on the active page to inspect nearby concepts, sources, and synthesis pages
- open source summaries before raw sources unless the user wants raw evidence directly
- check `Open Questions` sections for unresolved follow-up work

## Agent Support Loop

- report changed pages and the reason each page changed
- keep links relative so Obsidian and CLI navigation both work
- keep headings stable so Obsidian outline navigation remains useful
- add frontmatter consistently enough for future Dataview-style dashboards
- prefer improving cross-links, citations, and page summaries over adding duplicate pages
- use `llm-wiki query` when the agent needs a traceable context bundle
- use `llm-wiki search --json`, `llm-wiki status --json`, `llm-wiki graph --json`, and `llm-wiki query --json` for tool or plugin integrations

## Plugin Candidates

Use plugins as workflow extensions around the native markdown and graph model:

- Web Clipper-style source intake into `raw/inbox/`
- Dataview-style dashboards over frontmatter, stale pages, open questions, and source counts
- Marp-style presentation exports from synthesis pages
- review panels for proposed agent writebacks
- handoff commands that connect the active Obsidian page to `llm-wiki query`, `status`, or `graph`
- structured panels that consume `llm-wiki` JSON output instead of parsing human-readable markdown

## Before Finalizing

- update `wiki/index.md` after durable wiki changes
- append to `wiki/log.md`
- run `llm-wiki lint`
- tell the user what to inspect in Obsidian first
