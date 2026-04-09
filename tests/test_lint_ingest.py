from __future__ import annotations

from pathlib import Path
from tempfile import TemporaryDirectory
import sys
import unittest


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from llm_wiki.ingest import ingest_init
from llm_wiki.linting import lint_wiki


class LintAndIngestTests(unittest.TestCase):
    def test_lint_finds_frontmatter_links_orphans_source_path_and_index_drift(self) -> None:
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            (repo / "wiki" / "sources").mkdir(parents=True)
            (repo / "wiki" / "concepts").mkdir(parents=True)
            (repo / "wiki" / "entities").mkdir(parents=True)
            (repo / "wiki" / "synthesis").mkdir(parents=True)

            (repo / "raw" / "sources").mkdir(parents=True)
            (repo / "raw" / "sources" / "seed.md").write_text("# Seed\n", encoding="utf-8")

            (repo / "wiki" / "index.md").write_text(
                "# Index\n\n## Sources\n\n- [seed](sources/seed.md): seed\n",
                encoding="utf-8",
            )
            (repo / "wiki" / "log.md").write_text("# Log\n", encoding="utf-8")
            (repo / "wiki" / "overview.md").write_text(
                "---\npage_type: overview\nstatus: seed\nlast_updated: 2026-04-10\nsource_count: 1\n---\n\n# Overview\n\n[Missing](concepts/missing.md)\n",
                encoding="utf-8",
            )
            (repo / "wiki" / "sources" / "seed.md").write_text(
                "---\npage_type: source\nstatus: ingested\nlast_updated: 2026-04-10\nsource_count: 1\nsource_path: ../../raw/sources/seed.md\n---\n\n# Seed\n",
                encoding="utf-8",
            )
            (repo / "wiki" / "sources" / "broken-source.md").write_text(
                "---\npage_type: source\nstatus: draft\nlast_updated: 2026-04-10\nsource_count: 1\n---\n\n# Broken Source\n",
                encoding="utf-8",
            )
            (repo / "wiki" / "concepts" / "orphan.md").write_text(
                "---\npage_type: concept\nstatus: draft\nlast_updated: 2026-04-10\nsource_count: 0\n---\n\n# Orphan\n",
                encoding="utf-8",
            )
            (repo / "wiki" / "entities" / "broken.md").write_text(
                "---\npage_type: entity\nstatus: draft\nlast_updated: 2026-04-10\n---\n\n# Broken\n",
                encoding="utf-8",
            )

            issues = lint_wiki(repo)

            self.assertTrue(any(issue.code == "broken-link" and issue.path == "wiki/overview.md" for issue in issues))
            self.assertTrue(any(issue.code == "source-page-missing-source-path" and issue.path == "wiki/sources/broken-source.md" for issue in issues))
            self.assertTrue(any(issue.code == "frontmatter-missing-keys" and issue.path == "wiki/entities/broken.md" for issue in issues))
            self.assertTrue(any(issue.code == "orphan-page" and issue.path == "wiki/concepts/orphan.md" for issue in issues))
            self.assertTrue(any(issue.code == "index-missing-page" and issue.detail == "wiki/overview.md" for issue in issues))
            self.assertTrue(any(issue.code == "index-missing-page" and issue.detail == "wiki/sources/broken-source.md" for issue in issues))
            self.assertTrue(any(issue.code == "index-missing-page" and issue.detail == "wiki/concepts/orphan.md" for issue in issues))
            self.assertTrue(any(issue.code == "index-missing-page" and issue.detail == "wiki/entities/broken.md" for issue in issues))

    def test_ingest_init_canonicalizes_inbox_source_and_writes_draft(self) -> None:
        with TemporaryDirectory() as tmp:
            repo = Path(tmp)
            inbox = repo / "raw" / "inbox"
            inbox.mkdir(parents=True)
            (repo / "raw" / "sources").mkdir(parents=True)
            (repo / "wiki" / "sources").mkdir(parents=True)

            source_file = inbox / "My Article.md"
            source_file.write_text("# My Article\n\nBody.\n", encoding="utf-8")

            result = ingest_init(repo, source_file)

            self.assertEqual(result.canonical_source_path, repo / "raw" / "sources" / "my-article.md")
            self.assertEqual(result.draft_page_path, repo / "wiki" / "sources" / "my-article.md")
            self.assertEqual(result.canonical_source_path.read_text(encoding="utf-8"), source_file.read_text(encoding="utf-8"))
            draft = result.draft_page_path.read_text(encoding="utf-8")
            self.assertIn("page_type: source", draft)
            self.assertIn("source_path: ../../raw/sources/my-article.md", draft)
            self.assertIn("# Source: My Article", draft)


if __name__ == "__main__":
    unittest.main()
