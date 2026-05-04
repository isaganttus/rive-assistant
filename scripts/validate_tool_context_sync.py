#!/usr/bin/env python3
"""Validate that AI tool context files stay behaviorally in sync."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence


TOOL_CONTEXT_FILES = (
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules/rive.mdc",
    ".windsurfrules",
    ".github/copilot-instructions.md",
)

REQUIRED_SHARED_HEADINGS = (
    "## Role",
    "## Communication Guidelines",
    "## Critical Deprecation Notice",
    "## Core Rive Vocabulary",
    "## How to Use the Reference System",
    "### Curated reference files",
    "### Recipes",
    "### Full source documentation",
    "### Navigation rules",
    "### Important: Always verify code against source docs",
)

REQUIRED_SHARED_PHRASES = (
    "You are a Rive expert assistant",
    "Project planning",
    "Scripting",
    "Cross-platform runtime guidance",
    "Legacy Inputs and Events are deprecated",
    "Data Binding with View Models",
    "rive-reference/",
    "rive-recipes/",
    "rive-reference/00-concept-map.md",
    "Verify API signatures against source docs before writing code",
)

HEADING_RE = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
VOCAB_TERM_RE = re.compile(r"^-\s+\*\*([^*]+)\*\*")


@dataclass(frozen=True)
class ValidationFinding:
    file: str
    message: str


def strip_frontmatter(markdown: str) -> str:
    lines = markdown.splitlines()
    if not lines or lines[0].strip() != "---":
        return markdown

    for index, line in enumerate(lines[1:], 1):
        if line.strip() == "---":
            return "\n".join(lines[index + 1 :])

    return markdown


def extract_heading_sequence(markdown: str) -> list[str]:
    text = strip_frontmatter(markdown)
    headings: list[str] = []
    for line in text.splitlines():
        match = HEADING_RE.match(line)
        if match:
            headings.append(f"{match.group(1)} {match.group(2)}")
    return headings


def extract_section(markdown: str, heading: str) -> str:
    text = strip_frontmatter(markdown)
    lines = text.splitlines()
    start = None
    heading_level = heading.count("#")

    for index, line in enumerate(lines):
        if line.strip() == heading:
            start = index + 1
            break

    if start is None:
        return ""

    section_lines: list[str] = []
    for line in lines[start:]:
        match = HEADING_RE.match(line)
        if match and len(match.group(1)) <= heading_level:
            break
        section_lines.append(line)
    return "\n".join(section_lines)


def extract_vocabulary_terms(markdown: str) -> list[str]:
    section = extract_section(markdown, "## Core Rive Vocabulary")
    terms: list[str] = []
    for line in section.splitlines():
        match = VOCAB_TERM_RE.match(line)
        if match:
            terms.append(match.group(1).strip())
    return terms


def has_heading_sequence(headings: Sequence[str], required: Sequence[str]) -> bool:
    position = 0
    for heading in headings:
        if position < len(required) and heading == required[position]:
            position += 1
    return position == len(required)


def describe_term_difference(baseline: Sequence[str], current: Sequence[str]) -> str:
    baseline_set = set(baseline)
    current_set = set(current)
    missing = sorted(baseline_set - current_set)
    extra = sorted(current_set - baseline_set)

    parts: list[str] = []
    if missing:
        parts.append("missing " + ", ".join(missing))
    if extra:
        parts.append("extra " + ", ".join(extra))
    if not parts and list(baseline) != list(current):
        parts.append("same terms but different order")
    return "; ".join(parts)


def validate_context_files(
    repo_root: Path,
    files: Sequence[str] = TOOL_CONTEXT_FILES,
) -> list[ValidationFinding]:
    findings: list[ValidationFinding] = []
    contents: dict[str, str] = {}

    for file in files:
        path = repo_root / file
        if not path.exists():
            findings.append(ValidationFinding(file, "file is missing"))
            continue
        contents[file] = path.read_text(encoding="utf-8")

    for file, markdown in contents.items():
        for phrase in REQUIRED_SHARED_PHRASES:
            if phrase not in markdown:
                findings.append(ValidationFinding(file, f"missing required phrase: {phrase}"))

        headings = extract_heading_sequence(markdown)
        if not has_heading_sequence(headings, REQUIRED_SHARED_HEADINGS):
            findings.append(ValidationFinding(file, "shared headings are missing or out of order"))

    baseline_file = None
    baseline_terms: list[str] = []
    for file, markdown in contents.items():
        terms = extract_vocabulary_terms(markdown)
        if terms:
            baseline_file = file
            baseline_terms = terms
            break

    if baseline_file is not None:
        for file, markdown in contents.items():
            terms = extract_vocabulary_terms(markdown)
            if terms != baseline_terms:
                difference = describe_term_difference(baseline_terms, terms)
                findings.append(
                    ValidationFinding(
                        file,
                        f"vocabulary terms differ from {baseline_file}: {difference}",
                    )
                )

    return findings


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="*",
        help="Tool context files to validate. Defaults to all supported tool context files.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path.cwd()
    files = tuple(args.files) if args.files else TOOL_CONTEXT_FILES
    findings = validate_context_files(repo_root, files)

    if findings:
        print("Tool context sync issues found:", file=sys.stderr)
        for finding in findings:
            print(f"{finding.file}: {finding.message}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} tool context files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
