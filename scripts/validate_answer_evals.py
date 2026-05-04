#!/usr/bin/env python3
"""Validate static answer-quality eval case definitions."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Sequence

try:
    from scripts.validate_doc_paths import load_valid_paths
except ModuleNotFoundError:
    from validate_doc_paths import load_valid_paths


EVAL_CASE_GLOB = "evals/cases/*.json"

REQUIRED_LIST_FIELDS = (
    "tags",
    "expected_reference_files",
    "expected_source_paths",
    "required_concepts",
    "red_flags",
    "ideal_answer_shape",
)


@dataclass(frozen=True)
class EvalFinding:
    file: str
    message: str


def relative_name(repo_root: Path, path: Path) -> str:
    try:
        return path.relative_to(repo_root).as_posix()
    except ValueError:
        return path.name


def discover_eval_files(repo_root: Path) -> list[Path]:
    return sorted(repo_root.glob(EVAL_CASE_GLOB))


def read_eval_case(path: Path) -> tuple[dict[str, Any] | None, str | None]:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return None, f"invalid JSON: {exc.msg}"

    if not isinstance(data, dict):
        return None, "eval case must be a JSON object"
    return data, None


def is_non_empty_string_list(value: Any) -> bool:
    return isinstance(value, list) and bool(value) and all(
        isinstance(item, str) and bool(item.strip()) for item in value
    )


def source_path_exists(path: str, valid_paths: set[str]) -> bool:
    if path.endswith(".mdx"):
        candidate = path[:-4]
        return candidate in valid_paths
    if path.endswith("/"):
        prefix = path.rstrip("/") + "/"
        return any(valid_path.startswith(prefix) for valid_path in valid_paths)
    return path in valid_paths


def validate_eval_file(repo_root: Path, path: Path) -> list[EvalFinding]:
    name = relative_name(repo_root, path)
    findings: list[EvalFinding] = []
    data, error = read_eval_case(path)
    if error:
        return [EvalFinding(name, error)]
    assert data is not None

    case_id = data.get("id")
    if not isinstance(case_id, str) or not case_id.strip():
        findings.append(EvalFinding(name, "id must be a non-empty string"))

    question = data.get("question")
    if not isinstance(question, str) or len(question.strip()) < 20:
        findings.append(EvalFinding(name, "question must be at least 20 characters"))

    for field in REQUIRED_LIST_FIELDS:
        if not is_non_empty_string_list(data.get(field)):
            findings.append(EvalFinding(name, f"{field} must be a non-empty list of strings"))

    for reference in data.get("expected_reference_files", []):
        if isinstance(reference, str) and not (repo_root / reference).is_file():
            findings.append(
                EvalFinding(name, f"expected_reference_files entry does not exist: {reference}")
            )

    docs_paths = repo_root / "docs-paths.txt"
    valid_paths = load_valid_paths(docs_paths) if docs_paths.exists() else set()
    for source_path in data.get("expected_source_paths", []):
        if isinstance(source_path, str) and not source_path_exists(source_path, valid_paths):
            findings.append(
                EvalFinding(
                    name,
                    f"expected_source_paths entry is not in docs-paths.txt: {source_path}",
                )
            )

    return findings


def validate_eval_files(repo_root: Path, files: Sequence[Path]) -> list[EvalFinding]:
    findings: list[EvalFinding] = []
    seen_ids: dict[str, str] = {}

    if not files:
        return [EvalFinding("evals/cases", "no eval case files found")]

    for path in files:
        findings.extend(validate_eval_file(repo_root, path))
        data, error = read_eval_case(path)
        if error or data is None:
            continue
        case_id = data.get("id")
        if not isinstance(case_id, str) or not case_id.strip():
            continue

        name = relative_name(repo_root, path)
        if case_id in seen_ids:
            findings.append(
                EvalFinding(name, f"duplicate id also used by {seen_ids[case_id]}: {case_id}")
            )
        else:
            seen_ids[case_id] = name

    return findings


def parse_args(argv: Sequence[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "files",
        nargs="*",
        type=Path,
        help="Eval case JSON files to validate. Defaults to evals/cases/*.json.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(sys.argv[1:] if argv is None else argv)
    repo_root = Path.cwd()
    files = [
        path if path.is_absolute() else repo_root / path
        for path in (args.files or discover_eval_files(repo_root))
    ]
    findings = validate_eval_files(repo_root, files)

    if findings:
        print("Answer eval validation issues found:", file=sys.stderr)
        for finding in findings:
            print(f"{finding.file}: {finding.message}", file=sys.stderr)
        return 1

    print(f"Validated {len(files)} answer eval case files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
