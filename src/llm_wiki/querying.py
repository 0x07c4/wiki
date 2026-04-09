from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from llm_wiki.indexing import Page, scan_wiki_pages, tokenize
from llm_wiki.search import SearchResult, search_pages


@dataclass(slots=True)
class QuerySnippet:
    line_number: int
    text: str


@dataclass(slots=True)
class QueryPageContext:
    page: Page
    score: int
    snippets: list[QuerySnippet]

    @property
    def trace_path(self) -> str:
        return self.page.display_path

    @property
    def source_path(self) -> str | None:
        source_path = self.page.frontmatter.get("source_path")
        if source_path:
            return source_path
        return None


@dataclass(slots=True)
class QueryContextBundle:
    query: str
    contexts: list[QueryPageContext]


def select_relevant_pages(repo_root: Path, query: str, limit: int = 5) -> list[SearchResult]:
    return search_pages(repo_root, query=query, limit=limit)


def _line_snippets(page: Page, query_tokens: list[str], radius: int = 1, limit: int = 3) -> list[QuerySnippet]:
    lines = page.body.splitlines()
    scored_lines: list[tuple[int, int, str]] = []

    for index, line in enumerate(lines, start=1):
        line_tokens = tokenize(line)
        match_count = sum(line_tokens.count(token) for token in query_tokens)
        if match_count == 0:
            continue
        start = max(1, index - radius)
        end = min(len(lines), index + radius)
        context_lines = lines[start - 1 : end]
        snippet_text = "\n".join(context_lines).strip()
        scored_lines.append((match_count, index, snippet_text))

    scored_lines.sort(key=lambda item: (-item[0], item[1], item[2]))
    snippets: list[QuerySnippet] = []
    seen_texts: set[str] = set()
    for _, line_number, text in scored_lines:
        if text in seen_texts:
            continue
        snippets.append(QuerySnippet(line_number=line_number, text=text))
        seen_texts.add(text)
        if len(snippets) >= limit:
            break

    return snippets


def build_query_context(repo_root: Path, query: str, limit: int = 5, snippets_per_page: int = 3) -> QueryContextBundle:
    results = select_relevant_pages(repo_root, query=query, limit=limit)
    query_tokens = tokenize(query)

    contexts: list[QueryPageContext] = []
    for result in results:
        snippets = _line_snippets(result.page, query_tokens=query_tokens, limit=snippets_per_page)
        if not snippets and result.page.summary:
            snippets = [QuerySnippet(line_number=1, text=result.page.summary)]
        contexts.append(QueryPageContext(page=result.page, score=result.score, snippets=snippets))

    return QueryContextBundle(query=query, contexts=contexts)


def render_query_context_markdown(bundle: QueryContextBundle) -> str:
    lines: list[str] = []
    lines.append(f"# Query Context: {bundle.query}")
    lines.append("")
    lines.append("## Selected Pages")
    lines.append("")

    if not bundle.contexts:
        lines.append("- No relevant pages found.")
        lines.append("")
        return "\n".join(lines).rstrip() + "\n"

    for index, context in enumerate(bundle.contexts, start=1):
        lines.append(f"### {index}. {context.page.title}")
        lines.append("")
        lines.append(f"- score: {context.score}")
        lines.append(f"- trace: {context.trace_path}")
        if context.source_path:
            lines.append(f"- source_path: {context.source_path}")
        lines.append(f"- summary: {context.page.summary or 'No summary available.'}")
        if context.snippets:
            lines.append("- snippets:")
            for snippet in context.snippets:
                lines.append(f"  - line {snippet.line_number}:")
                snippet_lines = snippet.text.splitlines() or [""]
                for snippet_line in snippet_lines:
                    lines.append(f"    {snippet_line}")
        else:
            lines.append("- snippets: none")
        lines.append("")

    lines.append("## Notes")
    lines.append("")
    lines.append("- Use the trace path to map each passage back to a concrete wiki file.")
    lines.append("- Source pages may include `source_path` for raw provenance.")
    return "\n".join(lines).rstrip() + "\n"


def build_query_context_markdown(repo_root: Path, query: str, limit: int = 5, snippets_per_page: int = 3) -> str:
    bundle = build_query_context(repo_root, query=query, limit=limit, snippets_per_page=snippets_per_page)
    return render_query_context_markdown(bundle)

