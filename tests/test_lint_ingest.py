from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm_wiki.ingest import ingest_init
from llm_wiki.linting import collect_findings


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class LintAndIngestTests(unittest.TestCase):
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

[Concept](concepts/topic.md)
""",
        )
        write(self.repo_root / "wiki" / "index.md", "# stale index\n")
        write(self.repo_root / "wiki" / "log.md", "# Log\n")
        write(
            self.repo_root / "wiki" / "concepts" / "topic.md",
            """---
page_type: concept
status: active
last_updated: 2026-04-10
---

# Topic

This concept points to a [missing page](missing.md).
""",
        )
        write(self.repo_root / "raw" / "inbox" / "article.md", "# Article Title\n\nBody.\n")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_lint_reports_broken_link_and_index_drift(self) -> None:
        findings = collect_findings(self.repo_root)
        codes = {finding.code for finding in findings}
        self.assertIn("broken-link", codes)
        self.assertIn("index-drift", codes)

    def test_ingest_init_creates_raw_source_copy_and_source_page(self) -> None:
        raw_source, source_page = ingest_init(self.repo_root, "raw/inbox/article.md", copy=True)
        self.assertTrue(raw_source.exists())
        self.assertTrue(source_page.exists())
        page_text = source_page.read_text(encoding="utf-8")
        self.assertIn("source_path: ../../raw/sources/article.md", page_text)
        self.assertIn("# Source: Article Title", page_text)
        self.assertTrue((self.repo_root / "wiki" / "log.md").read_text(encoding="utf-8").count("ingest-init") >= 1)


if __name__ == "__main__":
    unittest.main()
