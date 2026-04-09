from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
import re
import shutil

from .linting import parse_frontmatter


SOURCE_TEMPLATE = """---
page_type: source
status: draft
last_updated: {last_updated}
source_count: 1
source_path: {source_path}
---

# Source: {title}

## Summary

One short paragraph explaining what this source says and why it matters.

## Key Claims

- claim 1
- claim 2
- claim 3

## Evidence Notes

- evidence, examples, or data points worth preserving

## Related Pages

- [Concept](../concepts/example-concept.md)
- [Entity](../entities/example-entity.md)
- [Synthesis](../synthesis/example-question.md)

## Open Questions

- what remains unclear?
- what should be checked against other sources?

## Citations

- [{raw_name}]({raw_source_rel})
"""


@dataclass(frozen=True)
class IngestInitResult:
    source_name: str
    canonical_source_path: Path
    draft_page_path: Path
    title: str
    created_source_copy: bool
    created_draft: bool


def ingest_init(repo_root: Path, source_file: Path, overwrite: bool = False) -> IngestInitResult:
    repo_root = repo_root.resolve()
    source_file = _resolve_input_path(repo_root, source_file)
    if not source_file.exists():
        raise FileNotFoundError(source_file)

    source_name = _slugify(source_file.stem) + source_file.suffix.lower()
    canonical_source_path = repo_root / "raw" / "sources" / source_name
    draft_page_path = repo_root / "wiki" / "sources" / f"{_slugify(source_file.stem)}.md"

    created_source_copy = False
    if source_file.resolve() != canonical_source_path.resolve():
        canonical_source_path.parent.mkdir(parents=True, exist_ok=True)
        if canonical_source_path.exists() and not overwrite:
            raise FileExistsError(canonical_source_path)
        shutil.copyfile(source_file, canonical_source_path)
        created_source_copy = True

    title = _derive_title(source_file, fallback=source_file.stem)
    draft_page_path.parent.mkdir(parents=True, exist_ok=True)
    if draft_page_path.exists() and not overwrite:
        raise FileExistsError(draft_page_path)

    rel_source_path = Path(os.path.relpath(canonical_source_path, draft_page_path.parent))
    draft_text = SOURCE_TEMPLATE.format(
        last_updated=_today(),
        source_path=rel_source_path.as_posix(),
        title=title,
        raw_name=canonical_source_path.name,
        raw_source_rel=rel_source_path.as_posix(),
    )
    draft_page_path.write_text(draft_text, encoding="utf-8")

    return IngestInitResult(
        source_name=source_file.name,
        canonical_source_path=canonical_source_path,
        draft_page_path=draft_page_path,
        title=title,
        created_source_copy=created_source_copy,
        created_draft=True,
    )


def _resolve_input_path(repo_root: Path, source_file: Path) -> Path:
    if source_file.is_absolute():
        return source_file
    candidate = (repo_root / source_file).resolve()
    if candidate.exists():
        return candidate
    return source_file.resolve()


def _derive_title(source_file: Path, fallback: str) -> str:
    text = source_file.read_text(encoding="utf-8")
    _, body = parse_frontmatter(text)
    for line in body.splitlines():
        match = re.match(r"^#\s+(.+?)\s*$", line.strip())
        if match:
            return match.group(1).strip()
    return fallback.replace("-", " ").strip().title()


def _slugify(value: str) -> str:
    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value).strip("-").lower()
    return slug or "source"


def _today() -> str:
    from datetime import date

    return date.today().isoformat()
