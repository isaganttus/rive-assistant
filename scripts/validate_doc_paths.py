#!/usr/bin/env python3
"""Validate Rive source documentation paths referenced by this repo."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


DOC_ROOTS = (
    "editor/",
    "runtimes/",
    "game-runtimes/",
    "getting-started/",
    "scripting/",
)

DEFAULT_FILES = (
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules/rive.mdc",
    ".windsurfrules",
    ".github/copilot-instructions.md",
    "README.md",
    "CONTRIBUTING.md",
    ".github/PULL_REQUEST_TEMPLATE.md",
    ".github/ISSUE_TEMPLATE/bug_report.md",
    ".github/ISSUE_TEMPLATE/feature_request.md",
)

DEFAULT_GLOBS = (
    "rive-reference/*.md",
    "rive-recipes/*.md",
)

CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")


@dataclass(frozen=True)
class DocReference:
    file: str
    line: int
    path: str


def load_valid_paths(path: Path) -> set[str]:
    return {
        line.strip()
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    }


def is_source_doc_reference(path: str) -> bool:
    if path.startswith(("http://", "https://", "<")):
        return False
    if path in {"feature-support", "feature-support.mdx"}:
        return True
    return path.startswith(DOC_ROOTS)


def extract_doc_references(markdown: str, file: str) -> list[DocReference]:
    refs: list[DocReference] = []
    for match in CODE_SPAN_RE.finditer(markdown):
        path = match.group(1).strip()
        if is_source_doc_reference(path):
            line = markdown.count("\n", 0, match.start()) + 1
            refs.append(DocReference(file, line, path))
    return refs


def find_missing_references(
    refs: Iterable[DocReference],
    valid_paths: set[str],
) -> list[DocReference]:
    missing: list[DocReference] = []
    for ref in refs:
        if ref.path.endswith(".mdx"):
            candidate = ref.path[:-4]
            exists = candidate in valid_paths
        elif ref.path.endswith("/"):
            prefix = ref.path.rstrip("/") + "/"
            exists = any(path.startswith(prefix) for path in valid_paths)
        else:
            exists = ref.path in valid_paths

        if not exists:
            missing.append(ref)
    return missing


def default_scan_files(repo_root: Path) -> list[Path]:
    files: list[Path] = []
    for relative in DEFAULT_FILES:
        path = repo_root / relative
        if path.exists():
            files.append(path)
    for pattern in DEFAULT_GLOBS:
        files.extend(sorted(repo_root.glob(pattern)))
    return files


def collect_references(repo_root: Path, files: Sequence[Path]) -> list[DocReference]:
    refs: list[DocReference] = []
    for path in files:
        text = path.read_text(encoding="utf-8")
        relative = path.relative_to(repo_root).as_posix()
        refs.extend(extract_doc_references(text, relative))
    return refs


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--docs-paths",
        type=Path,
        default=Path("docs-paths.txt"),
        help="Path to the generated docs path list.",
    )
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Files to scan. Defaults to repo markdown and assistant context files.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path.cwd()
    docs_paths = args.docs_paths if args.docs_paths.is_absolute() else repo_root / args.docs_paths
    files = args.files or default_scan_files(repo_root)
    files = [path if path.is_absolute() else repo_root / path for path in files]

    valid_paths = load_valid_paths(docs_paths)
    refs = collect_references(repo_root, files)
    missing = find_missing_references(refs, valid_paths)

    if missing:
        print("Invalid Rive docs source paths found:", file=sys.stderr)
        for ref in missing:
            print(f"{ref.file}:{ref.line}: {ref.path}", file=sys.stderr)
        return 1

    print(f"Validated {len(refs)} Rive docs source path references.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
