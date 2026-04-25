---
page_type: source
status: ingested
last_updated: 2026-04-26
source_count: 1
source_path: ../../raw/sources/tooling/2026-04-26-codex-llm-wiki-skill.md
---

# Source: Codex llm-wiki Skill 2026-04-26

## Summary

This local source note captures the first Codex-native integration point for the local agent knowledge wiki. It matters because future Codex sessions can now discover a dedicated `llm-wiki` skill, query the wiki through a repo-local wrapper, and follow the wiki's boundaries without relying on chat history.

## Key Claims

- The `llm-wiki` skill is installed under `$HOME/.codex/skills/llm-wiki`.
- The skill points Codex at `$HOME/workspace/wiki` as the local agent knowledge base.
- The bundled wrapper runs the repo-local CLI without requiring a global `llm-wiki` install.
- Global `AGENTS.md` was left unchanged; routing enters through skill discovery and the existing `ACTIVE.md` memory loop.
- The skill validation and wrapper query checks passed.

## Evidence Notes

- `SKILL.md` defines trigger conditions and the query/maintenance workflow.
- `scripts/llm-wiki` wraps `python3 -m llm_wiki.cli` with `PYTHONPATH` pointed at the wiki repo.
- `ACTIVE.md` now records a concise rule to prefer the wiki skill for local long-term context and traceable knowledge tasks.
- `status --json` and `query --json` succeeded through the wrapper.
- `sync-agent-config.sh --dry-run` included the new `llm-wiki` skill files in the sanitized export.

## Related Pages

- [Codex Wiki Integration](../synthesis/codex-wiki-integration.md)
- [Local Agent Knowledge Base Operating Model](../synthesis/local-agent-knowledge-base-operating-model.md)
- [llm-wiki JSON Output Contract](../synthesis/llm-wiki-json-output-contract.md)
- [Agent Skills](../concepts/agent-skills.md)

## Open Questions

- Should the next integration layer be an MCP server, a Codex plugin, or more CLI-backed skill affordances?
- Should global `AGENTS.md` eventually gain a very short local-wiki rule, or is `ACTIVE.md` plus skill discovery sufficient?

## Citations

- [2026-04-26-codex-llm-wiki-skill.md](../../raw/sources/tooling/2026-04-26-codex-llm-wiki-skill.md)
