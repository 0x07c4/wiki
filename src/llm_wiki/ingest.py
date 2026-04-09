from __future__ import annotations

import shutil
import unicodedata
from datetime import date
from pathlib import Path

from llm_wiki.indexing import extract_title, parse_frontmatter, write_index


def slugify(value: str) -> str:
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    output: list[str] = []
    previous_dash = False
    for char in normalized.lower():
        if char.isalnum():
            output.append(char)
            previous_dash = False
        else:
            if not previous_dash:
                output.append("-")
                previous_dash = True
    slug = "".join(output).strip("-")
    return slug or "source"


def read_markdown_title(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    _, body = parse_frontmatter(text)
    return extract_title(body, path.stem.replace("-", " ").title())


def ensure_parent(path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)


def relative_source_path(source_page_path: Path, raw_source_path: Path) -> str:
    return raw_source_path.relative_to(source_page_path.parent, walk_up=True).as_posix()


def canonicalize_source(repo_root: Path, source: Path, copy: bool) -> Path:
    raw_inbox = repo_root / "raw" / "inbox"
    raw_sources = repo_root / "raw" / "sources"
    raw_sources.mkdir(parents=True, exist_ok=True)

    resolved = source.resolve()
    if resolved.is_relative_to(raw_sources.resolve()):
        return resolved

    destination = raw_sources / source.name
    if destination.exists():
        return destination.resolve()

    if resolved.is_relative_to(raw_inbox.resolve()) and not copy:
        shutil.move(str(resolved), str(destination))
    else:
        shutil.copy2(resolved, destination)
    return destination.resolve()


def source_page_content(title: str, source_page_path: Path, raw_source_path: Path) -> str:
    today = date.today().isoformat()
    source_rel = relative_source_path(source_page_path, raw_source_path)
    template_path = source_page_path.parents[2] / "templates" / "source-page.md"
    if template_path.exists():
        template = template_path.read_text(encoding="utf-8")
    else:
        template = (
            "---\n"
            "page_type: source\n"
            "status: draft\n"
            "last_updated: YYYY-MM-DD\n"
            "source_count: 1\n"
            "source_path: ../../raw/sources/example-source.md\n"
            "---\n\n"
            "# Source: Title\n\n"
            "## Summary\n\n"
            "TODO: summarize this source.\n\n"
            "## Key Claims\n\n"
            "- claim 1\n"
            "- claim 2\n"
            "- claim 3\n\n"
            "## Evidence Notes\n\n"
            "- evidence, examples, or data points worth preserving\n\n"
            "## Related Pages\n\n"
            "- [Concept](../concepts/example-concept.md)\n"
            "- [Entity](../entities/example-entity.md)\n"
            "- [Synthesis](../synthesis/example-question.md)\n\n"
            "## Open Questions\n\n"
            "- what remains unclear?\n"
            "- what should be checked against other sources?\n\n"
            "## Citations\n\n"
            "- [example-source.md](../../raw/sources/example-source.md)\n"
        )

    replacements = {
        "YYYY-MM-DD": today,
        "example-source.md": raw_source_path.name,
        "../../raw/sources/example-source.md": source_rel,
        "# Source: Title": f"# Source: {title}",
        "- [example-source.md](../../raw/sources/example-source.md)": f"- [{raw_source_path.name}]({source_rel})",
        "One short paragraph explaining what this source says and why it matters.": "TODO: summarize this source.",
        "- claim 1\n- claim 2\n- claim 3": "- TODO",
        "- evidence, examples, or data points worth preserving": "- TODO",
        "- [Concept](../concepts/example-concept.md)\n- [Entity](../entities/example-entity.md)\n- [Synthesis](../synthesis/example-question.md)": "- TODO",
        "- what remains unclear?\n- what should be checked against other sources?": "- TODO",
    }

    content = template
    for before, after in replacements.items():
        content = content.replace(before, after)
    return content


def append_log_entry(repo_root: Path, title: str, raw_source_path: Path, source_page_path: Path) -> None:
    log_path = repo_root / "wiki" / "log.md"
    today = date.today().isoformat()
    entry = (
        f"\n## [{today}] ingest-init | {title}\n\n"
        f"- canonicalized raw source at `{raw_source_path.relative_to(repo_root).as_posix()}`\n"
        f"- scaffolded source page at `{source_page_path.relative_to(repo_root).as_posix()}`\n"
    )
    existing = log_path.read_text(encoding="utf-8") if log_path.exists() else "# Log\n"
    if entry.strip() not in existing:
        log_path.write_text(existing.rstrip() + entry + "\n", encoding="utf-8")


def ingest_init(repo_root: Path, source: str, copy: bool = False) -> tuple[Path, Path]:
    source_path = (repo_root / source).resolve() if not Path(source).is_absolute() else Path(source).resolve()
    if not source_path.exists():
        raise FileNotFoundError(f"source does not exist: {source}")
    if not source_path.is_file():
        raise ValueError(f"source is not a file: {source}")

    canonical_source = canonicalize_source(repo_root, source_path, copy=copy)
    title = read_markdown_title(canonical_source)
    slug = slugify(canonical_source.stem)

    source_page_path = repo_root / "wiki" / "sources" / f"{slug}.md"
    ensure_parent(source_page_path)

    if not source_page_path.exists():
        source_page_path.write_text(
            source_page_content(title=title, source_page_path=source_page_path, raw_source_path=canonical_source),
            encoding="utf-8",
        )
    append_log_entry(repo_root, title=title, raw_source_path=canonical_source, source_page_path=source_page_path)
    write_index(repo_root)
    return canonical_source, source_page_path


def ingest_init_command(repo_root: Path, source: str, copy: bool = False) -> int:
    canonical_source, source_page = ingest_init(repo_root, source=source, copy=copy)
    print(f"raw source: {canonical_source.relative_to(repo_root).as_posix()}")
    print(f"source page: {source_page.relative_to(repo_root).as_posix()}")
    return 0
