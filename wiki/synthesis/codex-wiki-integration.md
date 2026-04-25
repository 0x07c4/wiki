---
page_type: synthesis
status: active
last_updated: 2026-04-26
source_count: 1
---

# Codex Wiki Integration

## Question

How should this local wiki be connected to the user's Codex environment?

## Short Answer

Use a Codex skill as the first integration layer. The skill gives future Codex sessions a discoverable procedure for querying and maintaining `$HOME/workspace/wiki`, while a small `ACTIVE.md` rule nudges tasks that need local long-term context toward the skill.

This is enough before building heavier infrastructure. It avoids a daemon or MCP server while preserving the wiki's existing operating model: immutable `raw/`, maintained `wiki/`, local CLI tooling, and Obsidian for human review.

## Current Implementation

- Installed `$HOME/.codex/skills/llm-wiki`.
- Added a wrapper at `$HOME/.codex/skills/llm-wiki/scripts/llm-wiki`.
- The wrapper runs the local wiki CLI through `python3 -m llm_wiki.cli` with `PYTHONPATH=$HOME/workspace/wiki/src`.
- Added an `ACTIVE.md` rule so future Codex sessions prefer the wiki for local long-term context, agent/wiki/Obsidian/skills topics, and traceable knowledge tasks.
- Left global `AGENTS.md` unchanged.
- Verified that `sync-agent-config.sh --dry-run` includes the new skill in the sanitized agent config export.

## Why This Shape

- Skill discovery is Codex-native and already part of the user's synced agent configuration.
- The wrapper removes the need for a global Python package install.
- Keeping global `AGENTS.md` short avoids turning the entry prompt into a growing manual.
- `ACTIVE.md` already participates in the global memory loop, so a concise routing rule is enough.

## Next Integration Steps

1. Test the skill in a fresh Codex session with a query that should trigger local wiki usage.
2. Add richer `search` or `query` affordances only if repeated tasks show friction.
3. Consider an MCP server only after the CLI and skill boundary prove insufficient.
4. Keep Obsidian plugin work focused on human review; keep Codex skill work focused on agent-side retrieval and maintenance.

## Open Questions

- Should a future MCP expose `search`, `query`, `status`, and `graph` as structured tools instead of shell commands?
- Should the skill include a review helper for changed wiki pages?
- Should `sync-agent-config.sh` be run now to push the skill to `agent.git`, or left to the existing scheduled/manual sync flow?

## Related Pages

- [Source: Codex llm-wiki Skill 2026-04-26](../sources/codex-llm-wiki-skill-2026-04-26.md)
- [Local Agent Knowledge Base Operating Model](local-agent-knowledge-base-operating-model.md)
- [llm-wiki JSON Output Contract](llm-wiki-json-output-contract.md)
- [Agent Skills](../concepts/agent-skills.md)

## Citations

- [2026-04-26-codex-llm-wiki-skill.md](../../raw/sources/tooling/2026-04-26-codex-llm-wiki-skill.md)
