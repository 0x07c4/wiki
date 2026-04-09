from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from llm_wiki.indexing import build_index_markdown, parse_markdown_page, scan_markdown_pages  # noqa: E402
from llm_wiki.search import search_pages  # noqa: E402


def write_page(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class IndexingTests(unittest.TestCase):
    def test_parse_page_extracts_frontmatter_title_summary_and_links(self) -> None:
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            page = tmp_path / "wiki" / "sources" / "seed.md"
            write_page(
                page,
                """---
page_type: source
status: ingested
source_count: 2
published: true
tags:
  - wiki
  - llm
---

# Seed Source

## Summary

This source explains the wiki pattern and links to [LLM Wiki](../concepts/llm-wiki.md) and [Raw Source](../../raw/sources/seed.md).

## Details

More text.
""",
            )

            record = parse_markdown_page(page, root_path=tmp_path / "wiki")

            self.assertEqual(record.rel_path, "sources/seed.md")
            self.assertEqual(record.title, "Seed Source")
            self.assertEqual(
                record.summary,
                "This source explains the wiki pattern and links to [LLM Wiki](../concepts/llm-wiki.md) and [Raw Source](../../raw/sources/seed.md).",
            )
            self.assertEqual(record.frontmatter["page_type"], "source")
            self.assertEqual(record.frontmatter["status"], "ingested")
            self.assertEqual(record.frontmatter["source_count"], 2)
            self.assertIs(record.frontmatter["published"], True)
            self.assertEqual(record.frontmatter["tags"], ["wiki", "llm"])
            self.assertEqual(record.links, ["../concepts/llm-wiki.md", "../../raw/sources/seed.md"])

    def test_build_index_groups_pages_and_includes_metadata(self) -> None:
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            wiki = tmp_path / "wiki"
            write_page(
                wiki / "overview.md",
                """---
page_type: overview
status: seed
source_count: 1
---

# Overview

This wiki tracks a persistent markdown knowledge base.
""",
            )
            write_page(
                wiki / "log.md",
                """# Log

## [2026-04-10] bootstrap | repository scaffold
""",
            )
            write_page(
                wiki / "sources" / "seed.md",
                """---
page_type: source
status: ingested
source_count: 1
source_path: ../../raw/sources/seed.md
---

# Seed Source

## Summary

Seed summary.
""",
            )
            write_page(
                wiki / "concepts" / "llm-wiki.md",
                """---
page_type: concept
status: active
source_count: 1
---

# LLM Wiki

## Definition

Persistent wiki maintained by an LLM.
""",
            )

            rendered = build_index_markdown(wiki, updated="2026-04-10")

            self.assertIn("# Index", rendered)
            self.assertIn("## Entry Points", rendered)
            self.assertIn("## Sources", rendered)
            self.assertIn("## Concepts", rendered)
            self.assertIn("- [Overview](overview.md): This wiki tracks a persistent markdown knowledge base. [overview, seed, sources: 1]", rendered)
            self.assertIn("- [Log](log.md): No summary available.", rendered)
            self.assertIn("- [Seed Source](sources/seed.md): Seed summary. [source, ingested, sources: 1]", rendered)
            self.assertIn("- [LLM Wiki](concepts/llm-wiki.md): Persistent wiki maintained by an LLM. [concept, active, sources: 1]", rendered)

    def test_search_ranks_title_and_body_matches(self) -> None:
        with TemporaryDirectory() as tmpdir:
            tmp_path = Path(tmpdir)
            wiki = tmp_path / "wiki"
            write_page(
                wiki / "entities" / "obsidian.md",
                """---
page_type: entity
status: active
source_count: 1
---

# Obsidian

## Role

Obsidian is the local markdown workspace used to inspect the wiki graph.
""",
            )
            write_page(
                wiki / "concepts" / "llm-wiki.md",
                """---
page_type: concept
status: active
source_count: 1
---

# LLM Wiki

## Definition

Persistent markdown knowledge base maintained by an LLM.

The wiki graph remains useful as the collection grows.
""",
            )

            pages = scan_markdown_pages(wiki)
            results = search_pages(pages, "obsidian graph")

            self.assertEqual([result.path for result in results][:1], ["entities/obsidian.md"])
            self.assertGreater(results[0].score, results[-1].score)
            self.assertIn("wiki graph", results[0].snippet.lower())


if __name__ == "__main__":
    unittest.main()
