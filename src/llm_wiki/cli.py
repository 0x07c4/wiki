from __future__ import annotations

import argparse
from pathlib import Path


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="llm-wiki",
        description="Operate a local markdown wiki with lightweight indexing, search, lint, and ingest scaffolding.",
    )
    parser.add_argument(
        "--repo-root",
        default=".",
        help="Repository root containing raw/ and wiki/ directories.",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    reindex = subparsers.add_parser("reindex", help="Rebuild wiki/index.md from current wiki pages.")
    reindex.add_argument("--check", action="store_true", help="Exit non-zero if wiki/index.md would change.")
    reindex.add_argument("--stdout", action="store_true", help="Print generated index content instead of writing it.")

    search = subparsers.add_parser("search", help="Search wiki pages using lightweight local scoring.")
    search.add_argument("query", help="Query string to search for.")
    search.add_argument("--limit", type=int, default=10, help="Maximum number of results to print.")

    lint = subparsers.add_parser("lint", help="Run structural checks against the wiki.")

    ingest = subparsers.add_parser(
        "ingest-init",
        help="Canonicalize a raw source and scaffold its source summary page.",
    )
    ingest.add_argument("source", help="Path to a source file, usually under raw/inbox/ or raw/sources/.")
    ingest.add_argument(
        "--copy",
        action="store_true",
        help="Keep the original source in place instead of moving it out of raw/inbox/.",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    repo_root = Path(args.repo_root).resolve()

    if args.command == "reindex":
        from llm_wiki.indexing import reindex_command

        return reindex_command(repo_root=repo_root, check=args.check, to_stdout=args.stdout)

    if args.command == "search":
        from llm_wiki.search import search_command

        return search_command(repo_root=repo_root, query=args.query, limit=args.limit)

    if args.command == "lint":
        from llm_wiki.linting import lint_command

        return lint_command(repo_root=repo_root)

    if args.command == "ingest-init":
        from llm_wiki.ingest import ingest_init_command

        return ingest_init_command(repo_root=repo_root, source=args.source, copy=args.copy)

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
