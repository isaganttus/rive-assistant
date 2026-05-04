import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.validate_doc_paths import (
    DocReference,
    extract_doc_references,
    find_missing_references,
    load_valid_paths,
)


class ValidateDocPathsTest(unittest.TestCase):
    def test_extracts_only_rive_source_doc_references(self):
        markdown = textwrap.dedent(
            """
            Use `editor/layouts/layouts-overview.mdx` for layouts.
            Runtime pages can also be grouped as `runtimes/web/`.
            Bare source paths like `scripting/api-reference/interfaces/audio-source` are valid too.
            Ignore local docs like `README.md`, `rive-reference/`, and `https://example.com`.
            """
        )

        self.assertEqual(
            extract_doc_references(markdown, "example.md"),
            [
                DocReference("example.md", 2, "editor/layouts/layouts-overview.mdx"),
                DocReference("example.md", 3, "runtimes/web/"),
                DocReference("example.md", 4, "scripting/api-reference/interfaces/audio-source"),
            ],
        )

    def test_reports_missing_pages_and_prefixes(self):
        valid_paths = {
            "editor/layouts/layouts-overview",
            "scripting/api-reference/interfaces/audio-source",
            "runtimes/web/data-binding",
        }
        refs = [
            DocReference("example.md", 1, "editor/layouts/layouts-overview.mdx"),
            DocReference("example.md", 2, "editor/layouts/overview.mdx"),
            DocReference("example.md", 3, "runtimes/web/"),
            DocReference("example.md", 4, "runtimes/flutter/"),
            DocReference("example.md", 5, "scripting/api-reference/interfaces/audio-source"),
        ]

        self.assertEqual(
            find_missing_references(refs, valid_paths),
            [
                DocReference("example.md", 2, "editor/layouts/overview.mdx"),
                DocReference("example.md", 4, "runtimes/flutter/"),
            ],
        )

    def test_load_valid_paths_ignores_blank_lines(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "docs-paths.txt"
            path.write_text("editor/foo\n\nruntimes/bar\n", encoding="utf-8")

            self.assertEqual(load_valid_paths(path), {"editor/foo", "runtimes/bar"})


if __name__ == "__main__":
    unittest.main()
