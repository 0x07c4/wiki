# AI Agent Frontier Scouting Pack

Captured: 2026-04-25  
Purpose: initial source pack for tracking recent AI agent progress across theory, model releases, runtime platforms, skills, standards, evaluations, and ideas.

This is a curated source list, not a full article mirror. External pages remain the source of record; this file preserves the scouting set and the facts selected for wiki ingestion.

## Selection Criteria

- prioritize official announcements, docs, specifications, research papers, and benchmark maintainers
- prefer sources with direct relevance to agent runtime, long-horizon execution, tool use, computer use, skills, or evaluation
- use third-party commentary only as follow-up candidates, not as primary evidence for durable claims

## Sources

### OpenAI

- OpenAI, "Introducing GPT-5.5", 2026-04-23.
  URL: https://openai.com/index/introducing-gpt-5-5/
  Captured fact: GPT-5.5 is positioned around agentic coding, computer use, knowledge work, and scientific research; OpenAI reports Terminal-Bench 2.0, SWE-Bench Pro, OSWorld-Verified, Toolathlon, BrowseComp, FrontierMath, CyberGym, and related evaluations.

- OpenAI, "Introducing workspace agents in ChatGPT", 2026-04-22.
  URL: https://openai.com/index/introducing-workspace-agents-in-chatgpt/
  Captured fact: workspace agents are shared, Codex-powered agents for teams, run in the cloud, operate across tools, can ask for approval, and include enterprise governance and monitoring controls.

- OpenAI, "Codex for (almost) everything", 2026-04-16.
  URL: https://openai.com/index/codex-for-almost-everything/
  Captured fact: Codex is expanding beyond coding into computer operation, connected tools, memory, context-aware suggestions, repeatable work, and broader software-development lifecycle support.

- OpenAI, "The next evolution of the Agents SDK", 2026-04-15.
  URL: https://openai.com/index/the-next-evolution-of-the-agents-sdk/
  Captured fact: the Agents SDK adds a model-native harness, native sandbox execution, workspace manifests, MCP, skills, AGENTS.md, shell, apply_patch, durable execution, and separation of harness from compute.

- OpenAI, "Introducing the Codex app", 2026-02-02.
  URL: https://openai.com/index/introducing-the-codex-app/
  Captured fact: the Codex app is framed as a command center for multi-agent coding, with worktrees, skills, automations, review queues, and cross-surface session continuity.

- OpenAI, "Introducing AgentKit", 2025-10-06.
  URL: https://openai.com/index/introducing-agentkit/
  Captured fact: AgentKit combines Agent Builder, Connector Registry, ChatKit, Evals, trace grading, prompt optimization, third-party model support, and reinforcement fine-tuning features for agent development.

### Anthropic / Claude

- Anthropic, "Introducing Claude Sonnet 4.5", 2025-09-29.
  URL: https://www.anthropic.com/news/claude-sonnet-4-5
  Captured fact: Sonnet 4.5 is positioned for coding, complex agents, computer use, long-running tasks, Claude Agent SDK, checkpoints, context editing, memory, and browser/computer interaction.

- Anthropic, "Introducing Claude Opus 4.5", 2025-11-24.
  URL: https://www.anthropic.com/news/claude-opus-4-5
  Captured fact: Opus 4.5 is positioned for coding, agents, computer use, deep research, slides/spreadsheets, tool calling, and stronger prompt-injection robustness.

- Anthropic, "Introducing Agent Skills", 2025-10-16; update 2025-12-18.
  URL: https://claude.com/blog/skills
  Captured fact: Skills are folders of instructions, scripts, and resources loaded when relevant; Anthropic later published Agent Skills as an open standard for portability.

- Anthropic, "Agent Skills" documentation.
  URL: https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview
  Captured fact: skills are filesystem-based, progressively disclosed, can package metadata, instructions, resources, and code, and require careful trust review because they can direct tool and code execution.

- Anthropic, "Claude Code" product page.
  URL: https://www.anthropic.com/product/claude-code
  Captured fact: Claude Code is presented as an agentic coding system that reads codebases, edits files, runs tests, manages CI failures, and defaults to asking before modifying files or running commands.

### Google / Gemini

- Google, "Gemini 3.1 Pro: A smarter model for your most complex tasks", 2026-02-19.
  URL: https://blog.google/innovation-and-ai/models-and-research/gemini-models/gemini-3-1-pro/
  Captured fact: Gemini 3.1 Pro is framed as upgraded core intelligence for complex reasoning and agentic workflows, available through Gemini API, Vertex AI, Gemini CLI, Antigravity, Android Studio, and consumer products.

- Google DeepMind, "Deep Research Max: a step change for autonomous research agents", 2026-04-21.
  URL: https://blog.google/innovation-and-ai/models-and-research/gemini-models/next-generation-gemini-deep-research/
  Captured fact: Deep Research and Deep Research Max are autonomous research agents built with Gemini 3.1 Pro, adding MCP support, native visualizations, and long-horizon research workflows.

- Google DeepMind, "Introducing the Gemini 2.5 Computer Use model", 2025-10-07.
  URL: https://blog.google/innovation-and-ai/models-and-research/google-deepmind/gemini-computer-use-model/
  Captured fact: Gemini 2.5 Computer Use exposes a `computer_use` tool loop that uses screenshots, recent action history, UI action calls, safety checks, and user confirmation for some actions.

### Standards / Ecosystem

- Linux Foundation, "Linux Foundation Announces the Formation of the Agentic AI Foundation", 2025-12-09.
  URL: https://www.linuxfoundation.org/press/linux-foundation-announces-the-formation-of-the-agentic-ai-foundation
  Captured fact: AAIF was formed with founding contributions including MCP, goose, and AGENTS.md, with support from major AI and cloud companies.

- Anthropic, "Introducing the Model Context Protocol", 2024-11-25.
  URL: https://www.anthropic.com/news/model-context-protocol
  Captured fact: MCP was introduced as an open standard for connecting AI assistants to data systems, tools, and development environments.

- Model Context Protocol specification, latest captured version.
  URL: https://modelcontextprotocol.io/specification/draft
  Captured fact: MCP defines a JSON-RPC-based protocol for hosts, clients, and servers with resources, prompts, tools, sampling, roots, elicitation, progress, cancellation, and trust/safety guidance.

### Evaluation / Research

- Terminal-Bench, "Introducing Terminal-Bench 2.0 and Harbor", 2025-11-07.
  URL: https://www.tbench.ai/news/announcement-2-0
  Captured fact: Terminal-Bench 2.0 is a harder, better verified benchmark for agents in realistic terminal environments; Harbor targets scalable containerized evaluation and optimization.

- Scale AI, "SWE-Bench Pro: Raising the Bar for Agentic Coding", 2025-09-19.
  URL: https://scale.com/blog/swe-bench-pro
  Captured fact: SWE-Bench Pro extends agentic coding evaluation beyond SWE-Bench Verified with more diverse, difficult, contamination-resistant, human-augmented tasks.

- Shunyu Yao et al., "τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains", 2024-06-17.
  URL: https://huggingface.co/papers/2406.12045
  Captured fact: τ-bench evaluates tool-agent-user interaction with simulated users, domain APIs, policy guidelines, database-state evaluation, and reliability over repeated trials.

- Reyna Abhyankar, Qi Qi, Yiying Zhang, "OSWorld-Human: Benchmarking the Efficiency of Computer-Use Agents", 2025-06-19.
  URL: https://huggingface.co/papers/2506.16042
  Captured fact: OSWorld-Human studies computer-use agent efficiency, finding high latency and unnecessary extra steps compared with human trajectories.

## Initial Reading

- The dominant trend is not merely stronger base models; it is the packaging of models inside runtime, sandbox, tool, memory, skill, approval, and evaluation infrastructure.
- Coding agents are expanding into general computer work and knowledge-work execution.
- Skills are emerging as portable procedural memory for agents, but they also create a supply-chain and tool-execution trust surface.
- Benchmarks are moving from answer correctness toward long-horizon execution, realistic terminals, GUI control, domain rules, repeated-trial reliability, and latency.
