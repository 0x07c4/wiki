# Codex llm-wiki Skill Source Note

Captured: 2026-04-26  
Purpose: record the first Codex-native integration point for the local agent knowledge wiki.

This is a local implementation source note. It captures the user-level Codex setup and verification results at the time of writing.

## Implementation Inputs

- `$HOME/.codex/skills/llm-wiki/SKILL.md`
  - defines when Codex should use the local wiki
  - points Codex at `$HOME/workspace/wiki`
  - explains query, maintenance, notes-boundary, Obsidian-boundary, and durable-writeback rules

- `$HOME/.codex/skills/llm-wiki/scripts/llm-wiki`
  - wraps the repo-local CLI without requiring a global `llm-wiki` install
  - defaults `LLM_WIKI_REPO` to `$HOME/workspace/wiki`
  - runs `python3 -m llm_wiki.cli --repo-root "$LLM_WIKI_REPO"` with `PYTHONPATH` pointed at the repo `src/`

- `$HOME/.codex/skills/llm-wiki/agents/openai.yaml`
  - exposes UI metadata for the skill

- `$HOME/.codex/memories/ACTIVE.md`
  - records a global rule to prefer the wiki skill for local long-term context and traceable knowledge tasks

## Implemented Scope

- Codex can discover the `llm-wiki` skill from the standard `$HOME/.codex/skills` location.
- The skill gives future Codex sessions a concise operating procedure for querying and maintaining the wiki.
- The wrapper works without installing the Python package globally.
- Global `AGENTS.md` was not edited; the integration enters through the existing memory loop and skill discovery.

## Verification

- `python3 .../quick_validate.py $HOME/.codex/skills/llm-wiki`
- `$HOME/.codex/skills/llm-wiki/scripts/llm-wiki status --json`
- `$HOME/.codex/skills/llm-wiki/scripts/llm-wiki query "Obsidian Agent Workbench" --json`
- `$HOME/.codex/bin/sync-agent-config.sh --dry-run`

Results:

- skill validation passed
- status JSON returned the current wiki health payload
- query JSON returned relevant pages and traceable snippets
- sync dry-run included `skills/llm-wiki/SKILL.md`, `skills/llm-wiki/agents/openai.yaml`, and `skills/llm-wiki/scripts/llm-wiki`

## Integration Reading

- The skill is the correct first integration layer because it gives future Codex agents procedural knowledge without requiring a daemon, MCP server, or large global prompt.
- A short global memory rule is enough for automatic routing because `~/.codex/AGENTS.md` already requires reading `ACTIVE.md` before tasks.
- A future step can add a dedicated MCP or Codex plugin only if the CLI wrapper and skill trigger are not enough.
