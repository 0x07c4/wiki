from __future__ import annotations

from collections import defaultdict
from dataclasses import dataclass
from pathlib import Path

from llm_wiki.indexing import Page, build_index_markdown, scan_wiki_pages


REQUIRED_PAGE_FIELDS = {"page_type", "status", "last_updated"}
SPECIAL_NON_CONTENT = {"index.md", "log.md"}


@dataclass(slots=True)
class LintFinding:
    code: str
    path: str
    message: str


def wiki_pages_for_lint(repo_root: Path) -> list[Page]:
    return scan_wiki_pages(repo_root)


def check_required_frontmatter(pages: list[Page]) -> list[LintFinding]:
    findings: list[LintFinding] = []
    for page in pages:
        if page.path.name in SPECIAL_NON_CONTENT:
            continue
        missing = sorted(field for field in REQUIRED_PAGE_FIELDS if field not in page.frontmatter)
        if missing:
            findings.append(
                LintFinding(
                    code="missing-frontmatter",
                    path=page.display_path,
                    message=f"missing frontmatter fields: {', '.join(missing)}",
                )
            )
        if page.page_type == "source":
            source_path = page.frontmatter.get("source_path")
            if not source_path:
                findings.append(
                    LintFinding(
                        code="missing-source-path",
                        path=page.display_path,
                        message="source page missing source_path",
                    )
                )
            else:
                resolved = (page.path.parent / source_path).resolve()
                if not resolved.exists():
                    findings.append(
                        LintFinding(
                            code="missing-source-target",
                            path=page.display_path,
                            message=f"source_path target does not exist: {source_path}",
                        )
                    )
                elif not resolved.is_file():
                    findings.append(
                        LintFinding(
                            code="invalid-source-target",
                            path=page.display_path,
                            message=f"source_path target is not a file: {source_path}",
                        )
                    )
    return findings


def check_broken_links(pages: list[Page], repo_root: Path) -> list[LintFinding]:
    findings: list[LintFinding] = []
    for page in pages:
        for target in page.links:
            if not target.exists():
                findings.append(
                    LintFinding(
                        code="broken-link",
                        path=page.display_path,
                        message=f"broken link target: {target.relative_to(repo_root) if target.is_relative_to(repo_root) else target}",
                    )
                )
    return findings


def check_orphans(pages: list[Page], repo_root: Path) -> list[LintFinding]:
    findings: list[LintFinding] = []
    wiki_paths = {page.path.resolve() for page in pages}
    inbound: dict[Path, int] = defaultdict(int)

    for page in pages:
        for target in page.links:
            if target in wiki_paths:
                inbound[target] += 1

    for page in pages:
        if page.path.name in {"overview.md", "index.md", "log.md"}:
            continue
        if inbound[page.path.resolve()] == 0:
            findings.append(
                LintFinding(
                    code="orphan-page",
                    path=page.display_path,
                    message="no inbound wiki links",
                )
            )
    return findings


def check_index_drift(repo_root: Path) -> list[LintFinding]:
    generated = build_index_markdown(repo_root)
    index_path = repo_root / "wiki" / "index.md"
    existing = index_path.read_text(encoding="utf-8") if index_path.exists() else ""
    if existing == generated:
        return []
    return [
        LintFinding(
            code="index-drift",
            path="wiki/index.md",
            message="index content does not match the generated view of the wiki",
        )
    ]


def collect_findings(repo_root: Path) -> list[LintFinding]:
    pages = wiki_pages_for_lint(repo_root)
    findings: list[LintFinding] = []
    findings.extend(check_required_frontmatter(pages))
    findings.extend(check_broken_links(pages, repo_root))
    findings.extend(check_orphans(pages, repo_root))
    findings.extend(check_index_drift(repo_root))
    return sorted(findings, key=lambda item: (item.path, item.code, item.message))


def lint_command(repo_root: Path) -> int:
    findings = collect_findings(repo_root)
    if not findings:
        print("lint passed")
        return 0

    for finding in findings:
        print(f"{finding.code}: {finding.path}: {finding.message}")
    return 1

