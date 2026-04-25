# Notes to Wiki Checklist

Use this when importing selected entries from `~/workspace/notes` into this wiki.

## Boundary

- Treat `~/workspace/notes` as the upstream source of user thinking.
- Treat this repository as the compiled, LLM-maintained knowledge layer.
- Do not edit `~/workspace/notes` from this workflow unless the user explicitly asks.

## Before Importing

- read `~/workspace/notes/README.md`
- read `~/workspace/notes/INDEX.md`
- identify the specific note or notes the user wants to ingest
- prefer notes marked `active` or `evergreen`
- avoid bulk-importing draft notes unless the user asks

## Source Snapshot

- copy the selected note into `raw/sources/notes/` before ingesting it
- keep the snapshot content faithful to the upstream note
- use a stable filename that matches the original note when practical
- if the upstream repo is under git, record the source path and commit in the source summary when useful

## Wiki Ingest

- create or update exactly one source summary page for each imported note
- propagate only stable claims into concept, entity, or synthesis pages
- keep the original note path visible in the source summary when it helps traceability
- do not treat a wiki synthesis as a replacement for the original note

## Writeback

- wiki synthesis can propose a future writeback to `~/workspace/notes`
- actual writeback to `~/workspace/notes` requires explicit user confirmation
- when confirmed, prefer updating an existing note over creating a near-duplicate
