from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import sys
import json

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from llm_wiki.status import (
    build_status_snapshot,
    format_graph_adjacency,
    format_graph_json,
    format_status_json,
    format_status_summary,
)


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


class StatusTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.repo_root = Path(self.temp_dir.name)

        write(self.repo_root / "raw" / "inbox" / "draft.md", "# Draft\n")
        write(self.repo_root / "raw" / "sources" / "source-one.md", "# Source One\n")

        write(
            self.repo_root / "wiki" / "overview.md",
            """---
page_type: overview
status: active
last_updated: 2026-04-10
---

# Overview

Links to the [LLM Wiki](concepts/llm-wiki.md) and [Source One](sources/source-one.md).
""",
        )
        write(self.repo_root / "wiki" / "index.md", "# Index\n")
        write(self.repo_root / "wiki" / "log.md", "# Log\n")
        write(
            self.repo_root / "wiki" / "index.md",
            """# Index

- [overview](overview.md)
- [llm-wiki](concepts/llm-wiki.md)
- [source-one](sources/source-one.md)
""",
        )
        write(
            self.repo_root / "wiki" / "concepts" / "llm-wiki.md",
            """---
page_type: concept
status: active
last_updated: 2026-04-10
---

# LLM Wiki

An LLM Wiki links back to [Source One](../sources/source-one.md) and [Persistent Wiki](../synthesis/persistent-wiki.md).
""",
        )
        write(
            self.repo_root / "wiki" / "sources" / "source-one.md",
            """---
page_type: source
status: active
last_updated: 2026-04-10
source_count: 1
source_path: ../../raw/sources/source-one.md
---

# Source One

This source points at [LLM Wiki](../concepts/llm-wiki.md).
""",
        )
        write(
            self.repo_root / "wiki" / "synthesis" / "persistent-wiki.md",
            """---
page_type: synthesis
status: draft
last_updated: 2026-04-10
---

# Persistent Wiki

This synthesis references [LLM Wiki](../concepts/llm-wiki.md).
""",
        )
        write(
            self.repo_root / "wiki" / "entities" / "obsidian.md",
            """---
page_type: entity
status: active
last_updated: 2026-04-10
---

# Obsidian

No inbound links yet.
""",
        )

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_status_snapshot_counts_and_types(self) -> None:
        snapshot = build_status_snapshot(self.repo_root)

        self.assertEqual(snapshot.raw_inbox_files, [self.repo_root / "raw" / "inbox" / "draft.md"])
        self.assertEqual(snapshot.raw_source_files, [self.repo_root / "raw" / "sources" / "source-one.md"])
        self.assertEqual(snapshot.raw_markdown_count, 2)
        self.assertEqual(snapshot.wiki_count, 7)
        self.assertEqual(snapshot.page_type_counts["concept"], 1)
        self.assertEqual(snapshot.page_type_counts["entity"], 1)
        self.assertEqual(snapshot.page_type_counts["overview"], 1)
        self.assertEqual(snapshot.page_type_counts["source"], 1)
        self.assertEqual(snapshot.page_type_counts["synthesis"], 1)

    def test_backlinks_orphans_and_hubs(self) -> None:
        snapshot = build_status_snapshot(self.repo_root)

        concept = snapshot.graph_nodes[self.repo_root / "wiki" / "concepts" / "llm-wiki.md"]
        source = snapshot.graph_nodes[self.repo_root / "wiki" / "sources" / "source-one.md"]
        orphan = snapshot.graph_nodes[self.repo_root / "wiki" / "entities" / "obsidian.md"]

        self.assertEqual(concept.inbound, 3)
        self.assertEqual(source.inbound, 2)
        self.assertIn(orphan, snapshot.orphans)
        self.assertEqual(snapshot.hubs[0].page.path.name, "llm-wiki.md")
        index = snapshot.graph_nodes[self.repo_root / "wiki" / "index.md"]
        self.assertEqual(index.outbound, 0)

    def test_renderers_include_summary_and_adjacency(self) -> None:
        snapshot = build_status_snapshot(self.repo_root)
        summary = format_status_summary(snapshot)
        adjacency = format_graph_adjacency(snapshot)

        self.assertIn("raw/inbox: 1", summary)
        self.assertIn("raw/sources: 1", summary)
        self.assertIn("page types", summary.lower())
        self.assertIn("wiki/concepts/llm-wiki.md ->", adjacency)
        self.assertIn("wiki/sources/source-one.md -> wiki/concepts/llm-wiki.md", adjacency)

    def test_json_renderers_are_machine_readable(self) -> None:
        snapshot = build_status_snapshot(self.repo_root)
        status = json.loads(format_status_json(snapshot))
        graph = json.loads(format_graph_json(snapshot))

        self.assertEqual(status["schema_version"], "1")
        self.assertEqual(status["command"], "status")
        self.assertEqual(status["counts"]["raw_inbox"], 1)
        self.assertEqual(status["counts"]["wiki_pages"], 7)
        self.assertEqual(status["page_types"]["concept"], 1)
        self.assertIn("raw/sources/source-one.md", status["raw"]["sources"])
        self.assertEqual(status["hubs"][0]["path"], "wiki/concepts/llm-wiki.md")
        self.assertEqual(graph["schema_version"], "1")
        self.assertEqual(graph["command"], "graph")
        self.assertIn(
            {"source": "wiki/sources/source-one.md", "target": "wiki/concepts/llm-wiki.md"},
            graph["edges"],
        )
        self.assertEqual(
            graph["adjacency"]["wiki/sources/source-one.md"],
            ["wiki/concepts/llm-wiki.md"],
        )


if __name__ == "__main__":
    unittest.main()
