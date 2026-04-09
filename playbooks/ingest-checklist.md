# Ingest Checklist

Use this when a new source enters `raw/inbox/` or `raw/sources/`.

## Before Writing

- confirm the source file path
- confirm whether the source is already ingested
- read `wiki/index.md` first
- scan for existing concept, entity, and synthesis pages that may need updates

## During Ingest

- extract the main claims
- capture evidence, not just conclusions
- note uncertainty, contradiction, or weakly supported claims
- create or update exactly one source summary page
- update only the concept, entity, and synthesis pages actually affected
- keep links relative and explicit

## Before Finalizing

- update `wiki/overview.md` if the top-level thesis changed
- update `wiki/index.md`
- append one entry to `wiki/log.md`
- verify that every new durable claim has a citation path back to `raw/sources/`
- summarize which files changed and why

## Default Output

For a normal ingest, expect changes in:

- one file under `wiki/sources/`
- zero or more files under `wiki/concepts/`
- zero or more files under `wiki/entities/`
- zero or more files under `wiki/synthesis/`
- `wiki/index.md`
- `wiki/log.md`
