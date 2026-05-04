#!/usr/bin/env python3
"""Validate source traceability metadata in curated Rive reference files."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

try:
    from scripts.validate_doc_paths import find_missing_references, load_valid_paths, DocReference
except ModuleNotFoundError:
    from validate_doc_paths import find_missing_references, load_valid_paths, DocReference


REFERENCE_GLOB = "rive-reference/*.md"
EXCLUDED_REFERENCE_FILES = {"rive-reference/TEMPLATE.md"}

LAST_VERIFIED_RE = re.compile(r"^>\s+Last verified:\s*(.+?)\s*$", re.MULTILINE)
SOURCE_DOCS_RE = re.compile(r"^>\s+Source docs:\s*(.+?)\s*$", re.MULTILINE)
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
CODE_SPAN_RE = re.compile(r"`([^`\n]+)`")


@dataclass(frozen=True)
class ReferenceMetadata:
    last_verified: str | None
    source_docs: list[str]


@dataclass(frozen=True)
class MetadataFinding:
    file: str
    message: str


def relative_name(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def discover_reference_files(repo_root: Path) -> list[Path]:
    return [
        path
        for path in sorted(repo_root.glob(REFERENCE_GLOB))
        if relative_name(repo_root, path) not in EXCLUDED_REFERENCE_FILES
    ]


def extract_metadata(markdown: str) -> ReferenceMetadata:
    last_verified_match = LAST_VERIFIED_RE.search(markdown)
    source_docs_match = SOURCE_DOCS_RE.search(markdown)
    source_docs: list[str] = []

    if source_docs_match:
        source_docs = [
            match.group(1).strip()
            for match in CODE_SPAN_RE.finditer(source_docs_match.group(1))
            if match.group(1).strip()
        ]

    return ReferenceMetadata(
        last_verified=last_verified_match.group(1).strip() if last_verified_match else None,
        source_docs=source_docs,
    )


def validate_reference_file(repo_root: Path, path: Path) -> list[MetadataFinding]:
    name = relative_name(repo_root, path)
    markdown = path.read_text(encoding="utf-8")
    metadata = extract_metadata(markdown)
    findings: list[MetadataFinding] = []

    if metadata.last_verified is None:
        findings.append(MetadataFinding(name, "Last verified metadata is required"))
    elif not DATE_RE.match(metadata.last_verified):
        findings.append(MetadataFinding(name, "Last verified must use YYYY-MM-DD"))

    if not metadata.source_docs:
        findings.append(MetadataFinding(name, "Source docs metadata is required"))
    else:
        docs_paths = repo_root / "docs-paths.txt"
        valid_paths = load_valid_paths(docs_paths) if docs_paths.exists() else set()
        refs = [
            DocReference(name, 0, source_doc)
            for source_doc in metadata.source_docs
        ]
        for missing in find_missing_references(refs, valid_paths):
            findings.append(
                MetadataFinding(
                    name,
                    f"Source docs entry is not in docs-paths.txt: {missing.path}",
                )
            )

    return findings


def validate_reference_files(
    repo_root: Path,
    files: Sequence[Path] | None = None,
) -> list[MetadataFinding]:
    paths = list(files) if files is not None else discover_reference_files(repo_root)
    findings: list[MetadataFinding] = []

    for path in paths:
        findings.extend(validate_reference_file(repo_root, path))

    return findings


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Reference files to validate. Defaults to rive-reference/*.md except TEMPLATE.md.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path.cwd()
    files = [
        path if path.is_absolute() else repo_root / path
        for path in args.files
    ] if args.files else None
    findings = validate_reference_files(repo_root, files)

    if findings:
        print("Reference metadata issues found:", file=sys.stderr)
        for finding in findings:
            print(f"{finding.file}: {finding.message}", file=sys.stderr)
        return 1

    count = len(files) if files is not None else len(discover_reference_files(repo_root))
    print(f"Validated {count} Rive reference metadata blocks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
