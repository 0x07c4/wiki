---
page_type: source
status: ingested
last_updated: 2026-04-25
source_count: 1
source_path: ../../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md
---

# Source: Agent Skills and Claude Code Cluster 2026-04-25

## Summary

This source cluster deepens the wiki's understanding of Agent Skills as a reusable procedural-memory primitive. It covers the open Agent Skills format, Claude platform behavior, Claude Code extensions, Anthropic's engineering rationale, and Anthropic's public skills repository.

## Key Claims

- skills are folders containing `SKILL.md` plus optional scripts, references, templates, assets, or other resources
- skills use progressive disclosure: metadata is always discoverable, full instructions load only when relevant, and deeper resources load only when needed
- the `description` field is not cosmetic; it is the main routing signal for model-invoked skills
- Claude Code extends the base format with operational controls such as user invocation, model invocation, allowed tools, path matching, hooks, shell preprocessing, and forked subagent execution
- skills are useful for repeatable playbooks, team conventions, domain workflows, and deterministic helper scripts
- skills should be treated as a software supply-chain surface because they can influence tool use and may include executable code

## Evidence Notes

- Agent Skills open standard describes the portable folder format and three-stage progressive-disclosure model
- Claude platform docs define cross-surface behavior and warn about untrusted Skills
- Claude Code docs specify local project and personal skill paths, invocation modes, frontmatter controls, and advanced runtime behavior
- Anthropic's engineering blog frames Skills as onboarding-guide-like procedural knowledge for agents
- Anthropic's public `skills` repository provides examples and warns that examples should be tested before critical use

## Related Pages

- [Agent Skills](../concepts/agent-skills.md)
- [What Makes a Good Agent Skill](../synthesis/what-makes-a-good-agent-skill.md)
- [Agent Runtime](../concepts/agent-runtime.md)
- [AI Agent Frontier Radar 2026-04](../synthesis/ai-agent-frontier-radar-2026-04.md)

## Open Questions

- Which public skill repositories are worth tracking as trusted examples?
- Should this wiki maintain a separate curated catalog of recommended skills?
- How should security review results for third-party skills be represented?

## Citations

- [2026-04-25-agent-skills-claude-code-cluster.md](../../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md)
