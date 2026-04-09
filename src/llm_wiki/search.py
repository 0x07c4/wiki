from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from .indexing import PageRecord, collect_search_text, scan_markdown_pages, tokenise


@dataclass(slots=True)
class SearchResult:
    path: str
    title: str
    summary: str
    score: float
    snippet: str


def search_wiki(root: str | Path, query: str, *, limit: int = 10, index_name: str = "index.md") -> list[SearchResult]:
    pages = scan_markdown_pages(root, index_name=index_name)
    return search_pages(pages, query, limit=limit)


def search_pages(pages: Iterable[PageRecord], query: str, *, limit: int = 10) -> list[SearchResult]:
    query = query.strip()
    if not query:
        return []

    query_tokens = tokenise(query)
    if not query_tokens:
        return []

    results: list[SearchResult] = []
    for page in pages:
        score = score_page(page, query, query_tokens)
        if score <= 0:
            continue
        snippet = build_snippet(page.body, query_tokens)
        results.append(
            SearchResult(
                path=page.rel_path.replace("\\", "/"),
                title=page.title,
                summary=page.summary,
                score=score,
                snippet=snippet,
            )
        )

    results.sort(key=lambda result: (-result.score, result.path))
    return results[:limit]


def score_page(page: PageRecord, query: str, query_tokens: list[str]) -> float:
    text = collect_search_text(page).lower()
    title = page.title.lower()
    summary = page.summary.lower()
    frontmatter_text = " ".join(str(value) for value in page.frontmatter.values()).lower()
    body = page.body.lower()

    score = 0.0

    if query.lower() in title:
        score += 40
    if query.lower() in summary:
        score += 20
    if query.lower() in body:
        score += 10

    score += weighted_token_score(title, query_tokens, 8)
    score += weighted_token_score(summary, query_tokens, 5)
    score += weighted_token_score(frontmatter_text, query_tokens, 2)
    score += weighted_token_score(body, query_tokens, 3)

    present = sum(1 for token in query_tokens if token in text)
    if present == len(query_tokens):
        score += 15
    else:
        score += present * 2

    score += min(len(page.links), 5) * 0.25
    return score


def weighted_token_score(text: str, tokens: list[str], weight: float) -> float:
    total = 0.0
    for token in tokens:
        total += text.count(token) * weight
    return total


def build_snippet(body: str, tokens: list[str], *, window: int = 90) -> str:
    lower = body.lower()
    positions = [lower.find(token) for token in tokens if token in lower]
    positions = [position for position in positions if position >= 0]
    if not positions:
        collapsed = " ".join(body.split())
        return collapsed[: window * 2].strip()

    start = max(min(positions) - window, 0)
    end = min(start + window * 2, len(body))
    snippet = body[start:end].replace("\n", " ").strip()
    return snippet
