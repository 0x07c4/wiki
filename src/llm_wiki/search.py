from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from pathlib import Path

from llm_wiki.indexing import Page, scan_wiki_pages, tokenize


@dataclass(slots=True)
class SearchResult:
    page: Page
    score: int


def score_page(page: Page, query_tokens: list[str]) -> int:
    title_counts = Counter(tokenize(page.title))
    summary_counts = Counter(tokenize(page.summary))
    body_counts = Counter(tokenize(page.body))
    path_counts = Counter(tokenize(page.display_path))

    score = 0
    for token in query_tokens:
        score += title_counts[token] * 6
        score += summary_counts[token] * 4
        score += body_counts[token] * 1
        score += path_counts[token] * 2
    return score


def search_pages(repo_root: Path, query: str, limit: int = 10) -> list[SearchResult]:
    tokens = tokenize(query)
    if not tokens:
        return []

    results: list[SearchResult] = []
    for page in scan_wiki_pages(repo_root):
        score = score_page(page, tokens)
        if score > 0:
            results.append(SearchResult(page=page, score=score))

    results.sort(key=lambda item: (-item.score, item.page.display_path))
    return results[:limit]


def search_command(repo_root: Path, query: str, limit: int = 10) -> int:
    results = search_pages(repo_root, query=query, limit=limit)
    if not results:
        print(f'no results for "{query}"')
        return 1

    for index, result in enumerate(results, start=1):
        print(f"{index}. score={result.score} {result.page.display_path}")
        print(f"   {result.page.title}")
        if result.page.summary:
            print(f"   {result.page.summary}")
    return 0

