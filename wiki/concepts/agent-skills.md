---
page_type: concept
status: active
last_updated: 2026-04-25
source_count: 2
---

# Agent Skills

## Definition

Agent skills are reusable capability packages that give an agent task-specific procedures, metadata, scripts, templates, reference files, or workflow rules. They sit between one-off prompts and full tool integrations, acting as portable procedural memory for agents.

## Why It Matters

Skills are becoming a practical way to make agents more specialized without retraining the model or stuffing every instruction into the initial prompt. They support progressive disclosure: the agent can discover that a skill exists, load instructions when relevant, and access scripts or resources only when needed.

For code agents, skills also become a lightweight runtime extension point. A skill can be personal, project-specific, enterprise-managed, or plugin-provided; it can be model-invoked or user-invoked; and in Claude Code it can carry tool permissions, path filters, subagent execution, hooks, and shell preprocessing.

## Supporting Evidence

- Anthropic defines Skills as folders containing instructions, scripts, and resources that load when relevant
- Claude's docs describe Skill metadata, triggered instructions, and deeper resources or executable scripts as different loading levels
- OpenAI's Codex and Agents SDK materials treat skills as part of the broader agentic primitive set alongside MCP and AGENTS.md
- prebuilt document skills such as PowerPoint, Excel, Word, and PDF show the near-term product pattern: package repeatable expert workflows into reusable agent capabilities
- the Agent Skills open standard defines a portable folder format centered on `SKILL.md`
- Claude Code extends Skills with invocation control, `allowed-tools`, dynamic context injection, and forked subagent execution
- Anthropic's public skills repository shows Skills spanning document work, technical workflows, creative tasks, and enterprise communication

## Quality Signals

- precise `description` that clearly says what the skill does and when to use it
- narrow scope with an obvious trigger and success condition
- concise `SKILL.md` with deeper references split into supporting files
- deterministic scripts for operations that should not rely on token generation
- examples, tests, or evals that show the skill works on real tasks
- explicit permission posture for side-effecting actions
- clear provenance, versioning, license, and maintenance history

## Tensions

- a useful skill is closer to installing software than saving a prompt, because scripts and external resources can affect tool execution
- cross-surface portability is still uneven; skills may not automatically sync between app, API, CLI, and code-agent environments
- open skill ecosystems need trust, review, versioning, and provenance, otherwise skills become a supply-chain risk
- overly broad descriptions cause accidental activation; overly narrow descriptions make good skills invisible
- dynamic shell preprocessing is powerful, but it can surprise users if it runs commands before the model sees the prompt

## Related Pages

- [Source: AI Agent Frontier Scouting Pack 2026-04-25](../sources/agent-frontier-scouting-2026-04-25.md)
- [Source: Agent Skills and Claude Code Cluster 2026-04-25](../sources/agent-skills-claude-code-cluster-2026-04-25.md)
- [What Makes a Good Agent Skill](../synthesis/what-makes-a-good-agent-skill.md)
- [Agent Runtime](agent-runtime.md)
- [Protocol Machine](protocol-machine.md)
- [AI Agent Frontier Radar 2026-04](../synthesis/ai-agent-frontier-radar-2026-04.md)

## Citations

- [2026-04-25-agent-frontier-scouting.md](../../raw/sources/agent-frontier/2026-04-25-agent-frontier-scouting.md)
- [2026-04-25-agent-skills-claude-code-cluster.md](../../raw/sources/agent-skills/2026-04-25-agent-skills-claude-code-cluster.md)
