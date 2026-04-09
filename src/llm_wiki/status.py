from __future__ import annotations

from collections import Counter, defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from llm_wiki.indexing import Page, scan_wiki_pages


ENTRY_POINT_NAMES = {"overview.md", "index.md", "log.md"}
IGNORED_RAW_FILENAMES = {"README.md"}


@dataclass(slots=True)
class GraphNode:
    page: Page
    inbound: int = 0
    outbound: int = 0
    outbound_targets: list[str] = field(default_factory=list)

    @property
    def label(self) -> str:
        return self.page.display_path


@dataclass(slots=True)
class StatusSnapshot:
    repo_root: Path
    raw_inbox_files: list[Path]
    raw_source_files: list[Path]
    wiki_pages: list[Page]
    page_type_counts: dict[str, int]
    graph_nodes: dict[Path, GraphNode]

    @property
    def raw_markdown_count(self) -> int:
        return len(self.raw_inbox_files) + len(self.raw_source_files)

    @property
    def wiki_count(self) -> int:
        return len(self.wiki_pages)

    @property
    def page_count(self) -> int:
        return self.raw_markdown_count + self.wiki_count

    @property
    def orphans(self) -> list[GraphNode]:
        return [
            node
            for node in self.graph_nodes.values()
            if node.inbound == 0 and node.page.path.name not in ENTRY_POINT_NAMES
        ]

    @property
    def hubs(self) -> list[GraphNode]:
        return sorted(
            (node for node in self.graph_nodes.values() if node.inbound > 0),
            key=lambda node: (-node.inbound, -node.outbound, node.page.display_path),
        )


def iter_markdown_files(root: Path) -> list[Path]:
    if not root.exists():
        return []
    return sorted(
        path
        for path in root.rglob("*.md")
        if path.is_file() and path.name not in IGNORED_RAW_FILENAMES
    )


def scan_raw_markdown_files(repo_root: Path) -> tuple[list[Path], list[Path]]:
    raw_root = repo_root / "raw"
    inbox = iter_markdown_files(raw_root / "inbox")
    sources = iter_markdown_files(raw_root / "sources")
    return inbox, sources


def scan_graph_nodes(wiki_pages: list[Page]) -> dict[Path, GraphNode]:
    wiki_paths = {page.path.resolve(): page for page in wiki_pages}
    nodes = {page.path.resolve(): GraphNode(page=page) for page in wiki_pages}

    for page in wiki_pages:
        node = nodes[page.path.resolve()]
        outbound_targets: list[str] = []
        for target in page.links:
            target_page = wiki_paths.get(target)
            if target_page is None:
                continue
            target_node = nodes[target_page.path.resolve()]
            target_node.inbound += 1
            node.outbound += 1
            outbound_targets.append(target_page.display_path)
        node.outbound_targets = sorted(dict.fromkeys(outbound_targets))

    return nodes


def build_status_snapshot(repo_root: Path) -> StatusSnapshot:
    raw_inbox_files, raw_source_files = scan_raw_markdown_files(repo_root)
    wiki_pages = scan_wiki_pages(repo_root)
    page_type_counts = Counter(page.page_type for page in wiki_pages)
    graph_nodes = scan_graph_nodes(wiki_pages)
    return StatusSnapshot(
        repo_root=repo_root,
        raw_inbox_files=raw_inbox_files,
        raw_source_files=raw_source_files,
        wiki_pages=wiki_pages,
        page_type_counts=dict(sorted(page_type_counts.items())),
        graph_nodes=graph_nodes,
    )


def format_page_type_distribution(page_type_counts: dict[str, int]) -> str:
    if not page_type_counts:
        return "none"
    return ", ".join(f"{page_type}={count}" for page_type, count in page_type_counts.items())


def format_status_summary(snapshot: StatusSnapshot) -> str:
    lines = [
        "# Wiki Status",
        "",
        "## Counts",
        "",
        f"- raw/inbox: {len(snapshot.raw_inbox_files)}",
        f"- raw/sources: {len(snapshot.raw_source_files)}",
        f"- raw/markdown total: {snapshot.raw_markdown_count}",
        f"- wiki pages: {snapshot.wiki_count}",
        f"- all markdown pages tracked: {snapshot.page_count}",
        "",
        "## Page Types",
        "",
        f"- {format_page_type_distribution(snapshot.page_type_counts)}",
        "",
        "## Backlinks",
        "",
    ]

    hubs = snapshot.hubs[:5]
    if hubs:
        for node in hubs:
            lines.append(
                f"- {node.label}: backlinks={node.inbound}, outbound={node.outbound}"
            )
    else:
        lines.append("- none")

    lines.extend(["", "## Orphans", ""])
    orphans = snapshot.orphans
    if orphans:
        for node in orphans:
            lines.append(f"- {node.label}")
    else:
        lines.append("- none")

    lines.extend(["", "## Graph", ""])
    lines.extend(format_graph_adjacency(snapshot).splitlines())

    return "\n".join(lines).rstrip() + "\n"


def format_graph_adjacency(snapshot: StatusSnapshot) -> str:
    lines: list[str] = []
    for node in sorted(snapshot.graph_nodes.values(), key=lambda item: item.page.display_path):
        targets = ", ".join(node.outbound_targets) if node.outbound_targets else "[]"
        lines.append(f"{node.label} -> {targets}")
    return "\n".join(lines)


def status_command(repo_root: Path) -> int:
    snapshot = build_status_snapshot(repo_root)
    print(format_status_summary(snapshot), end="")
    return 0
