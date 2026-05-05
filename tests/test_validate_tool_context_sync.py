import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.validate_tool_context_sync import (
    REQUIRED_SHARED_PHRASES,
    TOOL_CONTEXT_FILES,
    ValidationFinding,
    extract_heading_sequence,
    extract_vocabulary_terms,
    validate_context_files,
)


ROOT = Path(__file__).resolve().parents[1]


class ValidateToolContextSyncTest(unittest.TestCase):
    def test_extracts_markdown_headings_after_optional_frontmatter(self):
        markdown = textwrap.dedent(
            """\
            ---
            description: Example
            ---
            # Rive Expert Assistant

            ## Role
            ### Details
            """
        )

        self.assertEqual(
            extract_heading_sequence(markdown),
            ["# Rive Expert Assistant", "## Role", "### Details"],
        )

    def test_extracts_vocabulary_terms_from_bold_definition_bullets(self):
        markdown = textwrap.dedent(
            """\
            ## Core Rive Vocabulary

            - **Artboard**: Root canvas/scene.
            - **Component** (formerly Nested Artboard): Reusable artboard instance.
            - Not a definition bullet.

            ## How to Use the Reference System
            """
        )

        self.assertEqual(extract_vocabulary_terms(markdown), ["Artboard", "Component"])

    def test_reports_missing_required_shared_phrase(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            complete = "\n".join(REQUIRED_SHARED_PHRASES) + "\n"
            incomplete = complete.replace("rive-recipes/", "recipes/")
            (root / "one.md").write_text(complete, encoding="utf-8")
            (root / "two.md").write_text(incomplete, encoding="utf-8")

            findings = validate_context_files(root, ("one.md", "two.md"))

        self.assertIn(
            ValidationFinding("two.md", "missing required phrase: rive-recipes/"),
            findings,
        )

    def test_reports_vocabulary_term_drift(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            one = "## Core Rive Vocabulary\n- **Artboard**: Root.\n- **Layout**: Responsive.\n"
            two = "## Core Rive Vocabulary\n- **Artboard**: Root.\n"
            (root / "one.md").write_text(one, encoding="utf-8")
            (root / "two.md").write_text(two, encoding="utf-8")

            findings = validate_context_files(root, ("one.md", "two.md"))

        self.assertIn(
            ValidationFinding("two.md", "vocabulary terms differ from one.md: missing Layout"),
            findings,
        )

    def test_repo_tool_context_files_are_in_sync(self):
        self.assertEqual(validate_context_files(ROOT, TOOL_CONTEXT_FILES), [])


if __name__ == "__main__":
    unittest.main()
