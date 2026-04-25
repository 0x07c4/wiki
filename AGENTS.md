# AGENTS

This repository is an LLM-maintained local knowledge base for agents.

The durable artifact is the agent-usable knowledge layer under `wiki/`, plus the local tools and playbooks that make it easy to search, query, lint, ingest, and understand. The chat transcript is not durable.

## Objective

Build and maintain a persistent, interlinked, agent-readable knowledge base that sits between the user, future agents, and raw source documents.

This repository should help an agent:

- find relevant prior context quickly
- trace claims back to curated sources
- understand how concepts, entities, and syntheses relate
- decide whether to answer from existing knowledge, ingest a new source, or propose a durable writeback
- use local tooling instead of re-scanning the whole repository

It should also preserve a strong human-facing workspace. Obsidian is the expected browsing and inspection layer: the user can read pages, follow links, use Obsidian's built-in graph views, and review agent writebacks while the agent maintains the files.

The user is responsible for:

- curating sources
- steering emphasis
- validating important writebacks

The LLM is responsible for:

- summarizing sources
- maintaining links and cross-references
- updating concept, entity, and synthesis pages
- keeping the index and log current
- improving the local search, query, graph, lint, and ingest facilities when they become bottlenecks

## Relationship to `~/workspace/notes`

`~/workspace/notes` is an upstream personal-thinking repository. Treat it as the user's source of intent, not as part of this wiki's maintained layer.

Operational boundary:

- Do not edit `~/workspace/notes` during wiki maintenance unless the user explicitly asks for that writeback.
- Selected notes can be ingested into this wiki only as sources, usually by snapshotting a stable note into `raw/sources/notes/`.
- Prefer ingesting notes whose status is `active` or `evergreen`, or notes the user explicitly selects.
- A wiki synthesis may propose that a conclusion should be promoted back into `~/workspace/notes`, but the actual notes writeback requires explicit user confirmation.
- When a note snapshot is ingested, preserve traceability to the raw snapshot and mention the original notes path in the source summary when useful.

## Operational Aids

These aids are part of the knowledge base's operating surface, not incidental scripts.

- Obsidian is the human-facing workspace for browsing, built-in graph inspection, clipping, and plugin-based views over the markdown repo
- `templates/` contains starter structures for source, concept, entity, and synthesis pages
- `tools/obsidian-agent-workbench/` contains the read-only Obsidian Agent Workbench plugin skeleton
- `playbooks/ingest-checklist.md` is the default ingest runbook
- `playbooks/lint-checklist.md` is the default lint runbook
- `playbooks/notes-to-wiki-checklist.md` is the default runbook for importing selected `~/workspace/notes` entries
- `playbooks/obsidian-workbench-checklist.md` is the default runbook for human review and navigation in Obsidian
- `llm-wiki search` is the cheap local discovery tool, with JSON output for tool consumers
- `llm-wiki query` builds an LLM-ready markdown or JSON context bundle with traceable snippets
- `llm-wiki status` and `llm-wiki graph` expose structural health and link topology, with JSON output for tool consumers
- `wiki/synthesis/llm-wiki-json-output-contract.md` defines the stable JSON fields for tool and plugin consumers

## Directory Map

- `raw/inbox/`: newly dropped sources that have not been ingested yet
- `raw/sources/`: immutable curated source files
- `raw/sources/notes/`: optional snapshots of selected upstream notes
- `raw/assets/`: local images or attachments referenced by sources
- `wiki/overview.md`: top-level summary of the wiki
- `wiki/index.md`: catalog of pages
- `wiki/log.md`: append-only operational log
- `wiki/sources/`: source summary pages
- `wiki/entities/`: stable entity pages
- `wiki/concepts/`: stable concept pages
- `wiki/synthesis/`: durable analyses, comparisons, and conclusions

## Non-Negotiable Rules

1. Treat files under `raw/` as immutable. Do not rewrite source content.
2. Treat files under `wiki/` as the maintained knowledge layer.
3. Read `wiki/index.md` before broad exploration so work stays scoped.
4. Prefer updating existing pages before creating new ones.
5. Every durable claim should remain traceable to one or more raw sources.
6. Use relative markdown links between wiki pages.
7. Update `wiki/index.md` and `wiki/log.md` whenever ingest or durable writeback changes the wiki.
8. Do not write back query results as durable wiki content without explicit user confirmation.
9. Default to one-source-at-a-time ingest unless the user asks for batching.
10. Keep pages concise, structured, and easy to diff.
11. Prefer adapting a file from `templates/` over inventing page structure from scratch.

## Page Conventions

Use YAML frontmatter on wiki pages when practical.

Recommended fields:

- `page_type`
- `status`
- `last_updated`
- `source_count`
- `source_path` for source summary pages

Recommended sections by page type:

- Source page: summary, key claims, related pages, open questions, citations
- Entity page: role, relevance, known facts, relationships, citations
- Concept page: definition, why it matters, supporting evidence, tensions, related pages
- Synthesis page: question, short answer, evidence, implications, open questions, citations

## Workflow: Ingest

When ingesting a new source:

1. Read the source from `raw/inbox/` or `raw/sources/`.
2. Extract the main claims, evidence, uncertainties, and reusable concepts.
3. Create or update one page under `wiki/sources/`.
4. Update any affected concept, entity, or synthesis pages.
5. Update `wiki/overview.md` if the overall picture changed.
6. Update `wiki/index.md`.
7. Append one entry to `wiki/log.md`.
8. Show the user which wiki pages changed and why.

Use `playbooks/ingest-checklist.md` as the default execution checklist.
If the source comes from `~/workspace/notes`, also use `playbooks/notes-to-wiki-checklist.md`.

## Workflow: Query

When answering a question:

1. Read `wiki/index.md` first.
2. Open only the relevant wiki pages and raw sources.
3. Use `llm-wiki query "<question>"` when a fast context bundle would help scope the answer.
4. Answer from the maintained wiki, with citations where possible.
5. If the answer produced a durable new artifact, propose a writeback target in `wiki/synthesis/`.
6. Write the page only after the user confirms.

## Workflow: Obsidian Workbench

When the task involves human review, Obsidian navigation, graph inspection, or plugin-supported browsing:

1. Read `wiki/index.md`, `wiki/overview.md`, and recent `wiki/log.md` entries.
2. Use `playbooks/obsidian-workbench-checklist.md`.
3. Treat Obsidian's built-in Graph view and Local Graph as the baseline human navigation layer.
4. Keep relative links, frontmatter, headings, and citations useful for both Obsidian and CLI workflows.
5. Treat plugins as workflow extensions for intake, dashboards, presentation, review, or handoff; do not assume plugin-specific behavior unless it is documented or the user confirms it.
6. Prefer `llm-wiki search --json`, `llm-wiki status --json`, `llm-wiki graph --json`, and `llm-wiki query --json` when building tool or plugin integrations, following `wiki/synthesis/llm-wiki-json-output-contract.md`.
7. Do not add or modify `.obsidian/` configuration unless the user explicitly asks.

## Workflow: Lint

During a lint pass, look for:

- contradictions between pages
- stale claims superseded by newer sources
- orphan pages with weak linkage
- important concepts mentioned without their own page
- missing cross-references
- source pages that do not propagate into the rest of the wiki
- synthesis pages that no longer reflect the evidence

Use `playbooks/lint-checklist.md` as the default execution checklist.
Use `llm-wiki status` and `llm-wiki graph` when backlink and orphan structure matters.

For each issue, either:

- apply the obvious low-risk fix, or
- summarize the proposed change before making a broader structural update

## Naming Guidance

- Use short, descriptive, stable file names.
- Prefer nouns for entities and concepts.
- Prefer question or comparison framing for synthesis pages when useful.
- Keep timestamps in `wiki/log.md`, not in every file name unless chronology is essential.
