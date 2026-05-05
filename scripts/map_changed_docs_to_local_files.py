#!/usr/bin/env python3
"""Map changed upstream Rive docs pages to local files that likely need review."""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence

try:
    from scripts.validate_answer_evals import discover_eval_files, read_eval_case
    from scripts.validate_doc_paths import extract_doc_references
    from scripts.validate_reference_metadata import discover_reference_files, extract_metadata
except ModuleNotFoundError:
    from validate_answer_evals import discover_eval_files, read_eval_case
    from validate_doc_paths import extract_doc_references
    from validate_reference_metadata import discover_reference_files, extract_metadata


RECIPE_GLOB = "rive-recipes/*.md"
DIFF_LINE_RE = re.compile(r"^[<>]\s+\S+\s+(.+?)\s*$")


@dataclass(frozen=True)
class ImpactMatch:
    kind: str
    local_file: str
    source_path: str


def relative_name(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.as_posix()


def normalize_source_path(path: str) -> str:
    path = path.strip()
    if path.endswith(".mdx"):
        return path[:-4]
    return path.rstrip("/") if path.endswith("/") else path


def normalize_changed_page(line: str) -> str:
    text = line.strip()
    if text.startswith("- "):
        text = text[2:].strip()

    diff_match = DIFF_LINE_RE.match(text)
    if diff_match:
        text = diff_match.group(1).strip()

    return normalize_source_path(text)


def source_matches_changed_page(changed_page: str, source_path: str) -> bool:
    changed = normalize_source_path(changed_page)
    source = source_path.strip()

    if source.endswith("/"):
        prefix = source.rstrip("/") + "/"
        return changed.startswith(prefix)

    return changed == normalize_source_path(source)


def collect_reference_refs(repo_root: Path) -> list[ImpactMatch]:
    matches: list[ImpactMatch] = []
    for path in discover_reference_files(repo_root):
        metadata = extract_metadata(path.read_text(encoding="utf-8"))
        relative = relative_name(repo_root, path)
        for source_doc in metadata.source_docs:
            matches.append(ImpactMatch("reference", relative, source_doc))
    return matches


def collect_recipe_refs(repo_root: Path) -> list[ImpactMatch]:
    matches: list[ImpactMatch] = []
    for path in sorted(repo_root.glob(RECIPE_GLOB)):
        relative = relative_name(repo_root, path)
        markdown = path.read_text(encoding="utf-8")
        for ref in extract_doc_references(markdown, relative):
            matches.append(ImpactMatch("recipe", relative, ref.path))
    return matches


def collect_eval_refs(repo_root: Path) -> list[ImpactMatch]:
    matches: list[ImpactMatch] = []
    for path in discover_eval_files(repo_root):
        relative = relative_name(repo_root, path)
        data, error = read_eval_case(path)
        if error or data is None:
            continue
        for source_path in data.get("expected_source_paths", []):
            if isinstance(source_path, str):
                matches.append(ImpactMatch("eval", relative, source_path))
    return matches


def collect_local_source_refs(repo_root: Path) -> list[ImpactMatch]:
    matches = [
        *collect_reference_refs(repo_root),
        *collect_recipe_refs(repo_root),
        *collect_eval_refs(repo_root),
    ]
    return sorted(set(matches), key=lambda match: (match.local_file, match.kind, match.source_path))


def map_changed_pages(
    changed_pages: Sequence[str],
    local_refs: Sequence[ImpactMatch],
) -> dict[str, list[ImpactMatch]]:
    mapped: dict[str, list[ImpactMatch]] = {}
    for raw_page in changed_pages:
        changed_page = normalize_changed_page(raw_page)
        if not changed_page:
            continue
        matches = [
            match
            for match in local_refs
            if source_matches_changed_page(changed_page, match.source_path)
        ]
        mapped[changed_page] = sorted(matches, key=lambda match: (match.local_file, match.kind, match.source_path))
    return mapped


def render_markdown(mapped: dict[str, list[ImpactMatch]]) -> str:
    lines = ["## Likely local files to review", ""]

    if not mapped:
        lines.append("- No changed upstream docs pages were provided.")
        return "\n".join(lines)

    for changed_page in sorted(mapped):
        lines.append(f"### `{changed_page}`")
        matches = mapped[changed_page]
        if not matches:
            lines.append("- No local files matched.")
        else:
            for match in matches:
                lines.append(
                    f"- `{match.local_file}` ({match.kind}, via `{match.source_path}`)"
                )
        lines.append("")

    return "\n".join(lines).rstrip()


def read_changed_pages_from_file(path: Path) -> list[str]:
    return [
        normalize_changed_page(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if normalize_changed_page(line)
    ]


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--changed-pages-file",
        type=Path,
        help="File containing changed upstream docs paths, one per line.",
    )
    parser.add_argument(
        "--json",
        action="store_true",
        help="Emit JSON instead of Markdown.",
    )
    parser.add_argument(
        "changed_pages",
        nargs="*",
        help="Changed upstream docs paths, with or without .mdx.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path.cwd()

    changed_pages: list[str] = []
    if args.changed_pages_file:
        changed_pages.extend(read_changed_pages_from_file(args.changed_pages_file))
    changed_pages.extend(normalize_changed_page(page) for page in args.changed_pages)
    changed_pages = sorted({page for page in changed_pages if page})

    mapped = map_changed_pages(changed_pages, collect_local_source_refs(repo_root))
    if args.json:
        output = {
            changed_page: [
                {
                    "kind": match.kind,
                    "local_file": match.local_file,
                    "source_path": match.source_path,
                }
                for match in matches
            ]
            for changed_page, matches in mapped.items()
        }
        print(json.dumps(output, indent=2, sort_keys=True))
    else:
        print(render_markdown(mapped))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
