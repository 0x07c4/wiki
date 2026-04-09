from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
from typing import Any

FRONTMATTER_BOUNDARY = "---"
RELATIVE_LINK_RE = re.compile(r"(?<!\!)\[[^\]]+\]\(([^)]+)\)")
HEADING_RE = re.compile(r"^#{1,6}\s+(.+?)\s*$")
TOKEN_RE = re.compile(r"[A-Za-z0-9_\u4e00-\u9fff]+", re.UNICODE)

DEFAULT_INDEX_NAME = "index.md"
DEFAULT_CATEGORY_ORDER = [
    "Entry Points",
    "Sources",
    "Concepts",
    "Entities",
    "Synthesis",
    "Other Pages",
]


@dataclass(slots=True)
class PageRecord:
    path: Path
    rel_path: str
    title: str
    summary: str
    frontmatter: dict[str, Any]
    links: list[str]
    body: str

    @property
    def category(self) -> str:
        parts = Path(self.rel_path).parts
        if Path(self.rel_path).name in {"overview.md", "log.md"}:
            return "Entry Points"
        if len(parts) >= 2:
            head = parts[0]
            return {
                "sources": "Sources",
                "concepts": "Concepts",
                "entities": "Entities",
                "synthesis": "Synthesis",
            }.get(head, "Other Pages")
        return "Other Pages"

    @property
    def metadata_bits(self) -> list[str]:
        bits: list[str] = []
        page_type = self.frontmatter.get("page_type")
        status = self.frontmatter.get("status")
        source_count = self.frontmatter.get("source_count")
        if page_type:
            bits.append(str(page_type))
        if status:
            bits.append(str(status))
        if source_count is not None:
            bits.append(f"sources: {source_count}")
        return bits


def scan_markdown_pages(root: str | Path, *, index_name: str = DEFAULT_INDEX_NAME) -> list[PageRecord]:
    root_path = Path(root)
    pages: list[PageRecord] = []
    for path in sorted(root_path.rglob("*.md")):
        if path.name == index_name:
            continue
        pages.append(parse_markdown_page(path, root_path=root_path))
    return pages


def parse_markdown_page(path: str | Path, *, root_path: str | Path | None = None) -> PageRecord:
    file_path = Path(path)
    root = Path(root_path) if root_path is not None else file_path.parent
    text = file_path.read_text(encoding="utf-8")
    frontmatter, body = split_frontmatter(text)
    title = extract_title(body) or file_path.stem.replace("-", " ").replace("_", " ").title()
    summary = extract_summary(body)
    links = extract_relative_links(body)
    rel_path = str(file_path.relative_to(root))
    return PageRecord(
        path=file_path,
        rel_path=rel_path,
        title=title,
        summary=summary,
        frontmatter=frontmatter,
        links=links,
        body=body,
    )


def split_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    stripped = text.lstrip("\ufeff")
    lines = stripped.splitlines()
    if not lines or lines[0].strip() != FRONTMATTER_BOUNDARY:
        return {}, stripped

    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == FRONTMATTER_BOUNDARY:
            end_index = idx
            break
    if end_index is None:
        return {}, stripped

    frontmatter_lines = lines[1:end_index]
    body = "\n".join(lines[end_index + 1 :])
    return parse_frontmatter_lines(frontmatter_lines), body


def parse_frontmatter_lines(lines: list[str]) -> dict[str, Any]:
    data: dict[str, Any] = {}
    current_key: str | None = None
    current_list: list[Any] | None = None

    for raw_line in lines:
        line = raw_line.rstrip()
        if not line.strip():
            continue
        stripped = line.lstrip()
        if stripped.startswith("- ") and current_key and current_list is not None:
            current_list.append(parse_scalar(stripped[2:].strip()))
            continue
        if ":" not in line:
            continue

        key, value = line.split(":", 1)
        key = key.strip()
        value = value.strip()

        if value == "":
            current_key = key
            current_list = []
            data[key] = current_list
            continue

        parsed_value = parse_scalar(value)
        data[key] = parsed_value
        current_key = None
        current_list = None

    return data


def parse_scalar(value: str) -> Any:
    if value.startswith(("'", '"')) and value.endswith(("'", '"')) and len(value) >= 2:
        return value[1:-1]
    lowered = value.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered in {"null", "none", "~"}:
        return None
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if re.fullmatch(r"-?\d+\.\d+", value):
        return float(value)
    return value


def extract_title(body: str) -> str:
    for line in body.splitlines():
        match = HEADING_RE.match(line)
        if match:
            return match.group(1).strip()
    return ""


def extract_summary(body: str) -> str:
    lines = body.splitlines()
    if not lines:
        return ""

    preferred_headings = {"summary", "definition", "short answer", "role"}
    current_section: str | None = None
    block: list[str] = []

    def flush_block() -> str:
        nonlocal block
        text = "\n".join(block).strip()
        block = []
        return collapse_paragraph(text)

    for line in lines:
        heading = HEADING_RE.match(line)
        if heading:
            if current_section in preferred_headings:
                summary = flush_block()
                if summary:
                    return summary
            current_section = heading.group(1).strip().lower()
            continue

        if current_section in preferred_headings:
            if not line.strip():
                summary = flush_block()
                if summary:
                    return summary
                continue
            if line.lstrip().startswith(("-", "*", ">", "|")):
                block.append(line.strip())
                continue
            block.append(line.strip())

    if current_section in preferred_headings:
        summary = flush_block()
        if summary:
            return summary

    # Fallback: first plain paragraph after the title.
    paragraphs = split_paragraphs(body)
    for paragraph in paragraphs:
        if not paragraph.lstrip().startswith("#"):
            return collapse_paragraph(paragraph)
    return ""


def split_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    for line in text.splitlines():
        if not line.strip():
            if current:
                paragraphs.append("\n".join(current))
                current = []
            continue
        current.append(line)
    if current:
        paragraphs.append("\n".join(current))
    return paragraphs


def collapse_paragraph(text: str) -> str:
    normalized = " ".join(part.strip() for part in text.splitlines()).strip()
    return normalized


def extract_relative_links(body: str) -> list[str]:
    links: list[str] = []
    for match in RELATIVE_LINK_RE.finditer(body):
        target = match.group(1).strip()
        if is_external_link(target):
            continue
        if target not in links:
            links.append(target)
    return links


def is_external_link(target: str) -> bool:
    lowered = target.lower()
    return (
        lowered.startswith(("http://", "https://", "mailto:", "ftp://"))
        or lowered.startswith("#")
        or lowered.startswith("/")
        or lowered.startswith("file:")
    )


def build_index_markdown(
    root: str | Path,
    *,
    index_name: str = DEFAULT_INDEX_NAME,
    updated: str | None = None,
) -> str:
    root_path = Path(root)
    if updated is None:
        updated = date.today().isoformat()

    pages = scan_markdown_pages(root_path, index_name=index_name)
    grouped = group_pages(pages)

    lines: list[str] = ["# Index", "", f"Updated: {updated}", ""]
    for category in DEFAULT_CATEGORY_ORDER:
        entries = grouped.get(category, [])
        if not entries:
            continue
        lines.append(f"## {category}")
        lines.append("")
        for page in entries:
            link = page.rel_path.replace("\\", "/")
            summary = page.summary or "No summary available."
            meta = format_metadata(page.metadata_bits)
            suffix = f" [{meta}]" if meta else ""
            lines.append(f"- [{page.title}]({link}): {summary}{suffix}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def group_pages(pages: list[PageRecord]) -> dict[str, list[PageRecord]]:
    grouped: dict[str, list[PageRecord]] = {category: [] for category in DEFAULT_CATEGORY_ORDER}
    for page in pages:
        grouped.setdefault(page.category, []).append(page)

    for entries in grouped.values():
        entries.sort(key=lambda item: item.rel_path)
    return grouped


def format_metadata(bits: list[str]) -> str:
    return ", ".join(bit for bit in bits if bit)


def collect_search_text(page: PageRecord) -> str:
    frontmatter_text = " ".join(str(value) for value in page.frontmatter.values())
    return "\n".join([page.title, page.summary, frontmatter_text, page.body])


def tokenise(text: str) -> list[str]:
    return [token.lower() for token in TOKEN_RE.findall(text)]
