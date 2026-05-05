import tempfile
import unittest
from pathlib import Path

from scripts.validate_answer_evals import (
    EvalFinding,
    discover_eval_files,
    validate_eval_file,
    validate_eval_files,
)


ROOT = Path(__file__).resolve().parents[1]


VALID_CASE = """{
  "id": "state-machine-modern-control",
  "question": "How should I drive a Rive state machine from React for a new project?",
  "tags": ["state-machines", "react", "data-binding"],
  "expected_reference_files": [
    "rive-reference/02-state-machines-and-events.md",
    "rive-reference/03-data-binding.md",
    "rive-recipes/state-machine-control.md"
  ],
  "expected_source_paths": [
    "editor/state-machine/transitions.mdx",
    "runtimes/react/data-binding.mdx"
  ],
  "required_concepts": [
    "Recommend Data Binding with View Models for new work",
    "Mention legacy Inputs are deprecated"
  ],
  "red_flags": [
    "Recommends legacy Inputs for new work",
    "Omits Data Binding"
  ],
  "ideal_answer_shape": [
    "Start with the modern cross-platform pattern",
    "Then show the React-specific API shape"
  ]
}
"""


class ValidateAnswerEvalsTest(unittest.TestCase):
    def test_discovers_json_eval_cases_in_sorted_order(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "evals" / "cases").mkdir(parents=True)
            (root / "evals" / "cases" / "b.json").write_text(VALID_CASE, encoding="utf-8")
            (root / "evals" / "cases" / "a.json").write_text(VALID_CASE, encoding="utf-8")

            self.assertEqual(
                [path.name for path in discover_eval_files(root)],
                ["a.json", "b.json"],
            )

    def test_valid_case_has_no_findings(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs-paths.txt").write_text(
                "editor/state-machine/transitions\nruntimes/react/data-binding\n",
                encoding="utf-8",
            )
            for relative in (
                "rive-reference/02-state-machines-and-events.md",
                "rive-reference/03-data-binding.md",
                "rive-recipes/state-machine-control.md",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# placeholder\n", encoding="utf-8")

            eval_path = root / "case.json"
            eval_path.write_text(VALID_CASE, encoding="utf-8")

            self.assertEqual(validate_eval_file(root, eval_path), [])

    def test_reports_schema_and_reference_errors(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs-paths.txt").write_text("", encoding="utf-8")
            eval_path = root / "bad.json"
            eval_path.write_text(
                """{
                  "id": "",
                  "question": "Too short",
                  "tags": [],
                  "expected_reference_files": ["missing.md"],
                  "expected_source_paths": ["editor/missing-page.mdx"],
                  "required_concepts": [],
                  "red_flags": [],
                  "ideal_answer_shape": []
                }
                """,
                encoding="utf-8",
            )

            findings = validate_eval_file(root, eval_path)

        self.assertIn(EvalFinding("bad.json", "id must be a non-empty string"), findings)
        self.assertIn(EvalFinding("bad.json", "question must be at least 20 characters"), findings)
        self.assertIn(EvalFinding("bad.json", "tags must be a non-empty list of strings"), findings)
        self.assertIn(EvalFinding("bad.json", "expected_reference_files entry does not exist: missing.md"), findings)
        self.assertIn(EvalFinding("bad.json", "expected_source_paths entry is not in docs-paths.txt: editor/missing-page.mdx"), findings)
        self.assertIn(EvalFinding("bad.json", "required_concepts must be a non-empty list of strings"), findings)
        self.assertIn(EvalFinding("bad.json", "red_flags must be a non-empty list of strings"), findings)
        self.assertIn(EvalFinding("bad.json", "ideal_answer_shape must be a non-empty list of strings"), findings)

    def test_reports_duplicate_ids_across_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs-paths.txt").write_text(
                "editor/state-machine/transitions\nruntimes/react/data-binding\n",
                encoding="utf-8",
            )
            for relative in (
                "rive-reference/02-state-machines-and-events.md",
                "rive-reference/03-data-binding.md",
                "rive-recipes/state-machine-control.md",
            ):
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text("# placeholder\n", encoding="utf-8")
            cases = root / "evals" / "cases"
            cases.mkdir(parents=True)
            (cases / "a.json").write_text(VALID_CASE, encoding="utf-8")
            (cases / "b.json").write_text(VALID_CASE, encoding="utf-8")

            findings = validate_eval_files(root, discover_eval_files(root))

        self.assertIn(
            EvalFinding("evals/cases/b.json", "duplicate id also used by evals/cases/a.json: state-machine-modern-control"),
            findings,
        )

    def test_repo_answer_eval_cases_are_valid(self):
        files = discover_eval_files(ROOT)

        self.assertGreaterEqual(len(files), 5)
        self.assertEqual(validate_eval_files(ROOT, files), [])


if __name__ == "__main__":
    unittest.main()
