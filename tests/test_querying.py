from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm_wiki.querying import build_query_context, build_query_context_markdown


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class QueryingTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

        write(
            self.repo_root / "wiki" / "overview.md",
            """---
page_type: overview
status: active
last_updated: 2026-04-10
---

# Overview

This wiki tracks a persistent markdown knowledge base maintained by an LLM.
""",
        )
        write(self.repo_root / "wiki" / "index.md", "# Index\n")
        write(self.repo_root / "wiki" / "log.md", "# Log\n")
        write(
            self.repo_root / "wiki" / "concepts" / "llm-wiki.md",
            """---
page_type: concept
status: active
last_updated: 2026-04-10
---

# LLM Wiki

An LLM Wiki is a persistent, interlinked markdown knowledge base maintained by an LLM on top of immutable raw sources.

## Why It Matters

It keeps compound knowledge current instead of rediscovering it from scratch.
""",
        )
        write(
            self.repo_root / "wiki" / "sources" / "seed.md",
            """---
page_type: source
status: active
last_updated: 2026-04-10
source_path: ../../raw/sources/seed.md
---

# Seed Source

The seed note argues that persistent wikis outperform ad hoc RAG for repeated synthesis.

## Key Claims

- persistent wiki
- ad hoc RAG
""",
        )
        write(self.repo_root / "raw" / "sources" / "seed.md", "# Seed\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_build_query_context_includes_traces_and_snippets(self) -> None:
        bundle = build_query_context(self.repo_root, query="persistent wiki", limit=3, snippets_per_page=2)
        self.assertGreaterEqual(len(bundle.contexts), 2)

        first = bundle.contexts[0]
        self.assertEqual(first.page.path.name, "llm-wiki.md")
        self.assertEqual(first.trace_path, "wiki/concepts/llm-wiki.md")
        self.assertTrue(first.snippets)
        self.assertIn("persistent", first.snippets[0].text.lower())

        source_context = next(context for context in bundle.contexts if context.page.path.name == "seed.md")
        self.assertEqual(source_context.source_path, "../../raw/sources/seed.md")
        self.assertIn("persistent wikis outperform ad hoc rag", source_context.snippets[0].text.lower())

    def test_markdown_bundle_is_llm_ready(self) -> None:
        markdown = build_query_context_markdown(self.repo_root, query="ad hoc rag", limit=2, snippets_per_page=2)
        self.assertIn("# Query Context: ad hoc rag", markdown)
        self.assertIn("## Selected Pages", markdown)
        self.assertIn("trace: wiki/sources/seed.md", markdown)
        self.assertIn("source_path: ../../raw/sources/seed.md", markdown)
        self.assertIn("Use the trace path", markdown)


if __name__ == "__main__":
    unittest.main()
