import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.validate_reference_metadata import (
    MetadataFinding,
    ReferenceMetadata,
    extract_metadata,
    validate_reference_file,
    validate_reference_files,
)


ROOT = Path(__file__).resolve().parents[1]


class ValidateReferenceMetadataTest(unittest.TestCase):
    def test_extracts_top_level_reference_metadata(self):
        markdown = textwrap.dedent(
            """\
            # Rive Example Reference
            > Last verified: 2026-04-23
            > Source docs: `editor/data-binding/overview.mdx`, `runtimes/react/data-binding.mdx`

            ## Overview
            Body.
            """
        )

        self.assertEqual(
            extract_metadata(markdown),
            ReferenceMetadata(
                last_verified="2026-04-23",
                source_docs=[
                    "editor/data-binding/overview.mdx",
                    "runtimes/react/data-binding.mdx",
                ],
            ),
        )

    def test_reports_missing_metadata_and_invalid_date(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs-paths.txt").write_text("", encoding="utf-8")
            path = root / "rive-reference" / "example.md"
            path.parent.mkdir()
            path.write_text(
                "# Rive Example Reference\n> Last verified: 04-23-2026\n",
                encoding="utf-8",
            )

            findings = validate_reference_file(root, path)

        self.assertIn(
            MetadataFinding("rive-reference/example.md", "Last verified must use YYYY-MM-DD"),
            findings,
        )
        self.assertIn(
            MetadataFinding("rive-reference/example.md", "Source docs metadata is required"),
            findings,
        )

    def test_reports_source_paths_missing_from_docs_paths(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "docs-paths.txt").write_text("editor/data-binding/overview\n", encoding="utf-8")
            path = root / "rive-reference" / "example.md"
            path.parent.mkdir()
            path.write_text(
                textwrap.dedent(
                    """\
                    # Rive Example Reference
                    > Last verified: 2026-04-23
                    > Source docs: `editor/data-binding/missing.mdx`, `runtimes/react/`
                    """
                ),
                encoding="utf-8",
            )

            findings = validate_reference_file(root, path)

        self.assertIn(
            MetadataFinding(
                "rive-reference/example.md",
                "Source docs entry is not in docs-paths.txt: editor/data-binding/missing.mdx",
            ),
            findings,
        )
        self.assertIn(
            MetadataFinding(
                "rive-reference/example.md",
                "Source docs entry is not in docs-paths.txt: runtimes/react/",
            ),
            findings,
        )

    def test_repo_reference_metadata_is_valid(self):
        findings = validate_reference_files(ROOT)

        self.assertEqual(findings, [])


if __name__ == "__main__":
    unittest.main()
