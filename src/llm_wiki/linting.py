from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from typing import Any, Iterable


FRONTMATTER_REQUIRED_KEYS = ("page_type", "status", "last_updated", "source_count")
DEFAULT_ORPHAN_EXEMPTIONS = {
    Path("wiki/index.md"),
    Path("wiki/log.md"),
}
INDEX_PATH = Path("wiki/index.md")

LINK_PATTERN = re.compile(r"(?<!\!)\[[^\]]*\]\(([^)]+)\)")


@dataclass(frozen=True)
class LintIssue:
    code: str
    path: str
    message: str
    detail: str = ""
    severity: str = "warning"


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    frontmatter_lines: list[str] = []
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            body = "\n".join(lines[idx + 1 :])
            return _parse_simple_yaml(frontmatter_lines), body
        frontmatter_lines.append(lines[idx])

    return {}, text


def _parse_simple_yaml(lines: Iterable[str]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for raw_line in lines:
        line = raw_line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()
        if not key:
            continue
        result[key] = _coerce_scalar(value)
    return result


def _coerce_scalar(value: str) -> Any:
    if value == "":
        return ""
    if value.isdigit():
        return int(value)
    if value.startswith("\"") and value.endswith("\"") and len(value) >= 2:
        return value[1:-1]
    if value.startswith("'") and value.endswith("'") and len(value) >= 2:
        return value[1:-1]
    lower = value.lower()
    if lower == "true":
        return True
    if lower == "false":
        return False
    return value


@dataclass(frozen=True)
class WikiPage:
    path: Path
    frontmatter: dict[str, Any]
    body: str

    @property
    def rel_path(self) -> Path:
        return self.path

    @property
    def links(self) -> list[str]:
        return [match.group(1).strip() for match in LINK_PATTERN.finditer(self.body)]


def scan_wiki_pages(repo_root: Path) -> list[WikiPage]:
    wiki_root = repo_root / "wiki"
    pages: list[WikiPage] = []
    if not wiki_root.exists():
        return pages

    for path in sorted(wiki_root.rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        frontmatter, body = parse_frontmatter(text)
        pages.append(WikiPage(path=path.relative_to(repo_root), frontmatter=frontmatter, body=body))
    return pages


def lint_wiki(repo_root: Path) -> list[LintIssue]:
    repo_root = repo_root.resolve()
    pages = scan_wiki_pages(repo_root)
    pages_by_rel = {page.path: page for page in pages}
    issues: list[LintIssue] = []

    inbound: dict[Path, set[Path]] = {page.path: set() for page in pages}

    for page in pages:
        _lint_frontmatter(page, issues)
        _lint_source_path(page, repo_root, issues)
        for link in page.links:
            target = _resolve_relative_link(repo_root, page.path, link)
            if target is None:
                continue
            target_abs = repo_root / target
            if target not in pages_by_rel and not target_abs.exists():
                issues.append(
                    LintIssue(
                        code="broken-link",
                        path=str(page.path),
                        message=f"Broken relative link: {link}",
                        detail=f"Could not resolve {link!r} from {page.path.as_posix()}",
                    )
                )
                continue
            if target in inbound:
                inbound[target].add(page.path)

    _lint_orphans(pages, inbound, issues)
    _lint_index_drift(repo_root, pages_by_rel, issues)
    return issues


def _lint_frontmatter(page: WikiPage, issues: list[LintIssue]) -> None:
    if page.path in DEFAULT_ORPHAN_EXEMPTIONS:
        return

    if not page.frontmatter:
        issues.append(
            LintIssue(
                code="missing-frontmatter",
                path=str(page.path),
                message="Missing YAML frontmatter",
            )
        )
        return

    missing = [key for key in FRONTMATTER_REQUIRED_KEYS if key not in page.frontmatter]
    if missing:
        issues.append(
            LintIssue(
                code="frontmatter-missing-keys",
                path=str(page.path),
                message="Frontmatter missing required keys",
                detail=", ".join(missing),
            )
        )


def _lint_source_path(page: WikiPage, repo_root: Path, issues: list[LintIssue]) -> None:
    if page.path.parts[:2] != ("wiki", "sources"):
        return

    source_path = page.frontmatter.get("source_path")
    if not source_path:
        issues.append(
            LintIssue(
                code="source-page-missing-source-path",
                path=str(page.path),
                message="Source page is missing source_path",
            )
        )
        return

    resolved = (repo_root / page.path.parent / Path(str(source_path))).resolve()
    if not resolved.exists():
        issues.append(
            LintIssue(
                code="source-page-broken-source-path",
                path=str(page.path),
                message="Source page source_path does not exist",
                detail=str(resolved),
            )
        )


def _lint_orphans(
    pages: list[WikiPage],
    inbound: dict[Path, set[Path]],
    issues: list[LintIssue],
) -> None:
    for page in pages:
        if page.path in DEFAULT_ORPHAN_EXEMPTIONS:
            continue
        if inbound.get(page.path):
            continue
        issues.append(
            LintIssue(
                code="orphan-page",
                path=str(page.path),
                message="Page has no inbound links",
            )
        )


def _lint_index_drift(
    repo_root: Path,
    pages_by_rel: dict[Path, WikiPage],
    issues: list[LintIssue],
) -> None:
    index_page = pages_by_rel.get(INDEX_PATH)
    if index_page is None:
        issues.append(
            LintIssue(
                code="missing-index",
                path=str(INDEX_PATH),
                message="wiki/index.md is missing",
                severity="error",
            )
        )
        return

    listed = set(_extract_index_targets(repo_root, index_page.body))
    expected = {
        page.path
        for page in pages_by_rel.values()
        if page.path not in DEFAULT_ORPHAN_EXEMPTIONS and page.path != INDEX_PATH
    }

    for path in sorted(expected - listed):
        issues.append(
            LintIssue(
                code="index-missing-page",
                path=str(INDEX_PATH),
                message="Index is missing a live wiki page",
                detail=path.as_posix(),
            )
        )

    for target in sorted(listed):
        target_path = (repo_root / target).resolve()
        if not target_path.exists():
            issues.append(
                LintIssue(
                    code="index-broken-link",
                    path=str(INDEX_PATH),
                    message="Index links to a missing page",
                    detail=target.as_posix(),
                )
            )


def _extract_index_targets(repo_root: Path, body: str) -> list[Path]:
    targets: list[Path] = []
    for match in LINK_PATTERN.finditer(body):
        link = match.group(1).strip()
        target = _resolve_relative_link(repo_root, INDEX_PATH, link)
        if target is not None:
            targets.append(target)
    return targets


def _resolve_relative_link(repo_root: Path, source_path: Path, link: str) -> Path | None:
    if not link or link.startswith("#"):
        return None
    if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", link):
        return None

    target = link.split("#", 1)[0].split("?", 1)[0]
    if not target:
        return None

    resolved = (repo_root / source_path.parent / target).resolve()
    try:
        return resolved.relative_to(repo_root)
    except ValueError:
        return resolved


def format_issues(issues: Iterable[LintIssue]) -> str:
    lines = []
    for issue in issues:
        extra = f" | {issue.detail}" if issue.detail else ""
        lines.append(f"{issue.severity.upper()} {issue.code} {issue.path}: {issue.message}{extra}")
    return "\n".join(lines)
