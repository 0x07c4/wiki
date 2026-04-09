from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm_wiki.indexing import build_index_markdown
from llm_wiki.search import search_pages


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class IndexingTests(unittest.TestCase):
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

This wiki tracks an LLM-maintained markdown knowledge base.
""",
        )
        write(self.repo_root / "wiki" / "log.md", "# Log\n")
        write(self.repo_root / "wiki" / "index.md", "# Index\n")
        write(
            self.repo_root / "wiki" / "concepts" / "llm-wiki.md",
            """---
page_type: concept
status: active
last_updated: 2026-04-10
---

# LLM Wiki

An LLM-managed markdown wiki that compounds over time.
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

This is the seed source summary for the wiki.
""",
        )
        write(self.repo_root / "raw" / "sources" / "seed.md", "# Seed\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_build_index_markdown_groups_pages(self) -> None:
        content = build_index_markdown(self.repo_root)
        self.assertIn("## Concepts", content)
        self.assertIn("[llm-wiki](concepts/llm-wiki.md)", content)
        self.assertIn("[seed](sources/seed.md)", content)
        self.assertNotIn("[index]", content)

    def test_search_prefers_title_match(self) -> None:
        results = search_pages(self.repo_root, query="llm wiki", limit=5)
        self.assertGreaterEqual(len(results), 1)
        self.assertEqual(results[0].page.path.name, "llm-wiki.md")

    def test_cli_reindex_stdout(self) -> None:
        env = {
            **__import__("os").environ,
            "PYTHONPATH": str(Path(__file__).resolve().parents[1] / "src"),
        }
        command = [
            sys.executable,
            "-m",
            "llm_wiki.cli",
            "--repo-root",
            str(self.repo_root),
            "reindex",
            "--stdout",
        ]
        completed = subprocess.run(command, check=True, capture_output=True, text=True, env=env)
        self.assertIn("# Index", completed.stdout)


if __name__ == "__main__":
    unittest.main()
