# Obsidian Agent Workbench Skeleton Source Note

Captured: 2026-04-26  
Purpose: record the first read-only Obsidian Agent Workbench plugin skeleton for this wiki.

This is a local implementation source note. It captures the repository state and verification results at the time of writing.

## Implementation Inputs

- `tools/obsidian-agent-workbench/manifest.json`
  - declares the plugin as `llm-wiki-agent-workbench`
  - marks the plugin as desktop-only

- `tools/obsidian-agent-workbench/src/main.ts`
  - registers an `Agent Workbench` side view
  - adds ribbon and command-palette entry points
  - reads active markdown page metadata from Obsidian
  - prepares read-only `llm-wiki` command handoffs
  - does not write to `raw/`, `wiki/`, or `.obsidian/`

- `tools/obsidian-agent-workbench/package.json`
  - defines `typecheck`, `build`, and `dev` scripts
  - uses TypeScript, esbuild, and Obsidian plugin typings

- `tools/obsidian-agent-workbench/styles.css`
  - provides dense, utilitarian panel styling

## Implemented Scope

- Side panel view: `Agent Workbench`
- Sections:
  - `Active Page`
  - `Related Context`
  - `Repo Health`
  - `Agent Handoff`
  - `Review Queue`
- Commands:
  - `Open Agent Workbench`
  - `Refresh Agent Workbench`
  - `Copy llm-wiki status command`
  - `Copy llm-wiki search command for active page`
- Settings:
  - `llm-wiki command`
  - `Repository root`

## Verification

Executed from `tools/obsidian-agent-workbench/`:

- `npm install`
- `npm run typecheck`
- `npm run build`

Results:

- dependency install completed with zero reported vulnerabilities
- TypeScript typecheck passed
- esbuild generated `main.js`

## Integration Reading

- This is a read-only plugin skeleton, not an autonomous wiki editor.
- Build output `main.js` is generated locally and ignored by git.
- The plugin currently copies commands instead of running shell commands inside Obsidian.
- Future work should decide whether command execution belongs inside Obsidian or should stay as copy-only handoff.
