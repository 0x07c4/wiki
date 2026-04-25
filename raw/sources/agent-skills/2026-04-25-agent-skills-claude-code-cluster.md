# Agent Skills and Claude Code Source Cluster

Captured: 2026-04-25  
Purpose: deeper source pack for tracking Agent Skills as an emerging primitive for procedural memory, workflow reuse, and agent specialization.

This is a curated source list and extracted fact set, not a full mirror of external pages. External pages remain the source of record.

## Sources

### Agent Skills Open Standard

- Agent Skills, "Agent Skills Overview".
  URL: https://agentskills.io/
  Captured facts:
  - Agent Skills are a lightweight, open format for extending agents with specialized knowledge and workflows.
  - The core unit is a folder containing `SKILL.md` with at least `name` and `description`, plus instructions.
  - Skills may bundle optional scripts, reference materials, templates, assets, and other resources.
  - Skills use progressive disclosure: discovery loads metadata, activation loads `SKILL.md`, execution may load resources or run bundled code.
  - The format aims at portable, version-controlled reuse across skills-compatible agents.

### Claude Platform Agent Skills Docs

- Anthropic, "Agent Skills" documentation.
  URL: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  Captured facts:
  - Skills provide domain-specific expertise, workflows, context, and best practices.
  - Claude API supports prebuilt and custom Skills in the code execution container.
  - Claude Code supports custom filesystem-based Skills.
  - Claude.ai supports prebuilt and custom Skills, but custom Skills have different sharing rules by surface.
  - Required `SKILL.md` frontmatter fields are `name` and `description`.
  - Skills can include code and resources; scripts can provide deterministic operations without loading all code into context.
  - Anthropic warns that untrusted Skills can misuse tools, access files, or exfiltrate data, so Skills should be audited like software.

### Claude Code Skills Docs

- Anthropic, "Extend Claude with skills" in Claude Code docs.
  URL: https://code.claude.com/docs/en/skills
  Captured facts:
  - Claude Code skills can be model-invoked automatically or user-invoked with `/skill-name`.
  - Claude Code recommends turning repeated playbooks, checklists, and procedural sections of `CLAUDE.md` into skills.
  - Skills can live at enterprise, personal, project, or plugin scope.
  - Claude Code extends the open standard with fields such as invocation controls, allowed tools, model and effort overrides, forked subagent execution, hooks, path matching, and shell behavior.
  - Skills can pre-approve specific tools with `allowed-tools`, but baseline permissions still apply.
  - `disable-model-invocation: true` is recommended for workflows where the user should control timing, such as deploy or commit.
  - Skills can inject dynamic context through shell preprocessing, which is powerful but should be controlled by policy.

### Anthropic Engineering Blog

- Anthropic Engineering, "Equipping agents for the real world with Agent Skills", 2025-10-16; updated 2025-12-18.
  URL: https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills
  Captured facts:
  - Anthropic frames Skills as organized folders of instructions, scripts, and resources that agents discover and load dynamically.
  - The motivating problem is that real work requires procedural knowledge and organizational context, not only model capability.
  - Anthropic compares building a skill to creating an onboarding guide for a new hire.
  - Skills are meant to be composable, scalable, and portable.
  - Anthropic expects Skills to complement MCP by teaching agents workflows involving external tools and software.
  - A future direction is agents creating, editing, and evaluating Skills themselves.

### Anthropic Skills Repository

- Anthropic, `anthropics/skills` GitHub repository.
  URL: https://github.com/anthropics/skills
  Captured facts:
  - The repository contains Anthropic's implementation examples for Skills and points to agentskills.io for the standard.
  - It includes example Skills across creative, design, development, technical, enterprise, communication, and document workflows.
  - Each skill is self-contained in a folder with `SKILL.md`.
  - The repository includes document skills for docx, pdf, pptx, and xlsx as source-available references.
  - The README warns that examples are educational and should be tested thoroughly before critical use.

## Initial Reading

- A skill is best understood as procedural memory packaged as code-adjacent files, not as a long prompt.
- The `description` field is operationally important because it controls discovery and therefore whether the skill loads at the right time.
- Good skills use progressive disclosure: concise `SKILL.md`, deeper references only when needed, and scripts for deterministic work.
- Claude Code's extensions make skills closer to runtime policy: invocation control, allowed tools, forked subagents, path matching, and dynamic context.
- Skills have a supply-chain risk profile because they can guide tool use and include executable code.
- A high-quality skill needs a quality rubric: trigger precision, bounded scope, deterministic helpers, examples, tests/evals, permission discipline, provenance, and maintenance.
