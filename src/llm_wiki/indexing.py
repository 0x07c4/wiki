from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


MARKDOWN_LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n?", re.DOTALL)
TOKEN_RE = re.compile(r"[a-z0-9]+")

ENTRY_POINT_NAMES = {"overview.md", "log.md", "index.md"}


@dataclass(slots=True)
class Page:
    repo_root: Path
    path: Path
    wiki_rel_path: Path
    page_type: str
    title: str
    summary: str
    body: str
    frontmatter: dict[str, str]
    links: list[Path]

    @property
    def stem(self) -> str:
        return self.path.stem

    @property
    def display_path(self) -> str:
        return self.path.relative_to(self.repo_root).as_posix()

    @property
    def index_link(self) -> str:
        return self.wiki_rel_path.as_posix()


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}, text

    frontmatter: dict[str, str] = {}
    for line in match.group(1).splitlines():
        stripped = line.strip()
        if not stripped or stripped.startswith("#") or ":" not in stripped:
            continue
        key, value = stripped.split(":", 1)
        frontmatter[key.strip()] = value.strip().strip('"').strip("'")

    return frontmatter, text[match.end() :]


def extract_title(body: str, fallback: str) -> str:
    for line in body.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip()
    return fallback


def extract_summary(body: str) -> str:
    lines = body.splitlines()
    blocks: list[str] = []
    current: list[str] = []
    in_code_block = False

    def flush() -> None:
        if current:
            blocks.append(" ".join(item.strip() for item in current if item.strip()))
            current.clear()

    for raw_line in lines:
        line = raw_line.rstrip()
        stripped = line.strip()

        if stripped.startswith("```"):
            in_code_block = not in_code_block
            flush()
            continue
        if in_code_block:
            continue
        if not stripped:
            flush()
            continue
        if stripped.startswith("#"):
            flush()
            continue
        if stripped.startswith(("- ", "* ", "1. ", "2. ", "3. ", ">")):
            flush()
            continue

        current.append(stripped)

    flush()
    return blocks[0] if blocks else ""


def extract_links(body: str, base_path: Path) -> list[Path]:
    links: list[Path] = []
    for _, target in MARKDOWN_LINK_RE.findall(body):
        cleaned = target.strip()
        if not cleaned or cleaned.startswith(("http://", "https://", "mailto:", "#")):
            continue
        target_without_anchor = cleaned.split("#", 1)[0]
        if not target_without_anchor:
            continue
        resolved = (base_path.parent / target_without_anchor).resolve()
        links.append(resolved)
    return links


def infer_page_type(path: Path, frontmatter: dict[str, str]) -> str:
    page_type = frontmatter.get("page_type")
    if page_type:
        return page_type

    parent = path.parent.name
    if parent in {"sources", "concepts", "entities", "synthesis"}:
        return parent[:-1] if parent.endswith("s") else parent
    if path.name == "overview.md":
        return "overview"
    if path.name == "log.md":
        return "log"
    if path.name == "index.md":
        return "index"
    return "other"


def load_page(repo_root: Path, path: Path) -> Page:
    text = path.read_text(encoding="utf-8")
    frontmatter, body = parse_frontmatter(text)
    title = extract_title(body, path.stem.replace("-", " ").title())
    summary = extract_summary(body)
    wiki_rel_path = path.relative_to(repo_root / "wiki")
    return Page(
        repo_root=repo_root,
        path=path.resolve(),
        wiki_rel_path=wiki_rel_path,
        page_type=infer_page_type(path, frontmatter),
        title=title,
        summary=summary,
        body=body,
        frontmatter=frontmatter,
        links=extract_links(body, path.resolve()),
    )


def scan_wiki_pages(repo_root: Path) -> list[Page]:
    wiki_root = repo_root / "wiki"
    paths = sorted(path for path in wiki_root.rglob("*.md") if path.is_file())
    return [load_page(repo_root, path) for path in paths]


def summary_for_index(page: Page) -> str:
    if page.summary:
        return truncate_summary(page.summary)
    if page.path.name == "log.md":
        return "chronological record of ingests and durable writebacks"
    if page.path.name == "index.md":
        return "content-oriented catalog of wiki pages"
    if page.path.name == "overview.md":
        return "top-level summary of the wiki's current thesis and open questions"
    return "no summary available yet"


def truncate_summary(text: str, limit: int = 160) -> str:
    if len(text) <= limit:
        return text
    return text[: limit - 3].rstrip() + "..."


def display_name(page: Page) -> str:
    if page.path.name in ENTRY_POINT_NAMES:
        return page.path.stem
    return page.path.stem


def group_pages(pages: Iterable[Page]) -> dict[str, list[Page]]:
    grouped: dict[str, list[Page]] = {
        "Entry Points": [],
        "Sources": [],
        "Concepts": [],
        "Entities": [],
        "Synthesis": [],
        "Other": [],
    }

    for page in pages:
        if page.path.name in ENTRY_POINT_NAMES:
            grouped["Entry Points"].append(page)
            continue
        match page.page_type:
            case "source":
                grouped["Sources"].append(page)
            case "concept":
                grouped["Concepts"].append(page)
            case "entity":
                grouped["Entities"].append(page)
            case "synthesis":
                grouped["Synthesis"].append(page)
            case _:
                grouped["Other"].append(page)

    for value in grouped.values():
        value.sort(key=lambda page: page.index_link)

    return grouped


def build_index_markdown(repo_root: Path) -> str:
    pages = [page for page in scan_wiki_pages(repo_root) if page.path.name != "index.md"]
    grouped = group_pages(pages)

    lines = ["# Index", "", f"Updated: {current_date_string()}", ""]
    ordered_sections = ["Entry Points", "Sources", "Concepts", "Entities", "Synthesis", "Other"]

    for section in ordered_sections:
        section_pages = grouped[section]
        if not section_pages:
            continue
        lines.append(f"## {section}")
        lines.append("")
        for page in section_pages:
            lines.append(
                f"- [{display_name(page)}]({page.index_link}): {summary_for_index(page)}"
            )
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def current_date_string() -> str:
    from datetime import date

    return date.today().isoformat()


def write_index(repo_root: Path) -> str:
    content = build_index_markdown(repo_root)
    index_path = repo_root / "wiki" / "index.md"
    index_path.write_text(content, encoding="utf-8")
    return content


def reindex_command(repo_root: Path, check: bool = False, to_stdout: bool = False) -> int:
    generated = build_index_markdown(repo_root)
    index_path = repo_root / "wiki" / "index.md"
    existing = index_path.read_text(encoding="utf-8") if index_path.exists() else ""

    if to_stdout:
        print(generated, end="")
        return 0

    if check:
        if existing != generated:
            print("wiki/index.md is out of date")
            return 1
        print("wiki/index.md is up to date")
        return 0

    if existing != generated:
        index_path.write_text(generated, encoding="utf-8")
        print(f"updated {index_path.relative_to(repo_root).as_posix()}")
    else:
        print("wiki/index.md already up to date")
    return 0


def tokenize(text: str) -> list[str]:
    return TOKEN_RE.findall(text.lower())
