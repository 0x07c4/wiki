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
        write(
            self.repo_root / "templates" / "source-page.md",
            """---
page_type: source
status: draft
last_updated: YYYY-MM-DD
source_count: 1
source_path: ../../raw/sources/example-source.md
---

# Source: Title

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

- [example-source.md](../../raw/sources/example-source.md)
""",
        )

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
        self.assertIn("- [article.md](../../raw/sources/article.md)", page_text)
        self.assertTrue((self.repo_root / "wiki" / "log.md").read_text(encoding="utf-8").count("ingest-init") >= 1)
        self.assertIn("[article](sources/article.md)", (self.repo_root / "wiki" / "index.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
