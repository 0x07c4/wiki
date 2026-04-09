# Lint Checklist

Use this during periodic health checks of the wiki.

## Structural Checks

- pages with no inbound or outbound links
- duplicate pages that should be merged
- concepts mentioned repeatedly but missing their own page
- entity pages that never connect back to source summaries

## Claim Quality Checks

- stale claims superseded by newer sources
- synthesis pages that overstate the evidence
- important statements without citations
- contradictions across concept, entity, and synthesis pages

## Operational Checks

- source pages that never propagated into the rest of the wiki
- `wiki/index.md` entries missing or out of date
- `wiki/log.md` missing recent ingests or durable writebacks
- frontmatter drift across similar page types

## Fix Strategy

- apply obvious low-risk link and index fixes directly
- summarize broader merges or thesis changes before making them
- prefer tightening an existing page over creating another near-duplicate page
