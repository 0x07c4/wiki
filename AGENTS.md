# AGENTS

This repository is an LLM-maintained wiki.

The durable artifact is the markdown wiki under `wiki/`, not the chat transcript.

## Objective

Build and maintain a persistent, interlinked wiki that sits between the user and raw source documents.

The user is responsible for:

- curating sources
- steering emphasis
- validating important writebacks

The LLM is responsible for:

- summarizing sources
- maintaining links and cross-references
- updating concept, entity, and synthesis pages
- keeping the index and log current

## Directory Map

- `raw/inbox/`: newly dropped sources that have not been ingested yet
- `raw/sources/`: immutable curated source files
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

## Workflow: Query

When answering a question:

1. Read `wiki/index.md` first.
2. Open only the relevant wiki pages and raw sources.
3. Answer from the maintained wiki, with citations where possible.
4. If the answer produced a durable new artifact, propose a writeback target in `wiki/synthesis/`.
5. Write the page only after the user confirms.

## Workflow: Lint

During a lint pass, look for:

- contradictions between pages
- stale claims superseded by newer sources
- orphan pages with weak linkage
- important concepts mentioned without their own page
- missing cross-references
- source pages that do not propagate into the rest of the wiki
- synthesis pages that no longer reflect the evidence

For each issue, either:

- apply the obvious low-risk fix, or
- summarize the proposed change before making a broader structural update

## Naming Guidance

- Use short, descriptive, stable file names.
- Prefer nouns for entities and concepts.
- Prefer question or comparison framing for synthesis pages when useful.
- Keep timestamps in `wiki/log.md`, not in every file name unless chronology is essential.
