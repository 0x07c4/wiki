# Obsidian Agent Workbench JSON Copy Source Note

Captured: 2026-04-26  
Purpose: record the first interactive read-only iteration of the Obsidian Agent Workbench plugin.

This is a local implementation source note. It captures the repository state and verification results at the time of writing.

## Implementation Inputs

- `tools/obsidian-agent-workbench/src/main.ts`
  - keeps the side panel read-only
  - opens existing related context links through Obsidian
  - runs safe `llm-wiki` read commands and copies JSON output to the clipboard
  - falls back to copying the shell command if command execution fails
  - defaults to the local repo CLI through `python3 -m llm_wiki.cli` with `PYTHONPATH=src`
  - still avoids writing to `raw/`, `wiki/`, or `.obsidian/`

- `tools/obsidian-agent-workbench/esbuild.config.mjs`
  - externalizes Node built-in modules so desktop-only command execution can bundle cleanly

- `tools/obsidian-agent-workbench/styles.css`
  - styles related-context links and missing-link states

- `tools/obsidian-agent-workbench/README.md`
  - updates the documented boundary from copy-only commands to read-only JSON output copying

## Implemented Scope

- Existing related-context links are clickable.
- `Copy status JSON`, `Copy graph JSON`, `Copy search JSON`, and `Copy query JSON` copy actual JSON output when the local CLI runs successfully.
- The plugin no longer requires a globally installed `llm-wiki` executable for the default path.
- `Copy lint command` remains a command handoff because lint is not a JSON payload.

## Verification

- `npm run typecheck`
- `npm run build`
- `env PYTHONPATH=src python3 -m llm_wiki.cli status --json`
- `python3 -m unittest discover -s tests`

Results:

- TypeScript typecheck passed.
- esbuild generated `main.js`.
- local CLI JSON output succeeded without a global `llm-wiki` executable.
- standard-library Python tests passed.
- `python3 -m pytest` was not available in the current environment, so `unittest` was used.

## Integration Reading

- The plugin has moved from command-preparation only to safe read-command execution.
- The user still stays in control: the plugin only copies output or commands and does not perform durable wiki writebacks.
- The local repo CLI fallback reduces setup friction for Obsidian usage.
