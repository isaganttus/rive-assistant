import tempfile
import textwrap
import unittest
from pathlib import Path

from scripts.map_changed_docs_to_local_files import (
    ImpactMatch,
    collect_local_source_refs,
    map_changed_pages,
    normalize_changed_page,
    render_markdown,
    source_matches_changed_page,
)


ROOT = Path(__file__).resolve().parents[1]


class MapChangedDocsToLocalFilesTest(unittest.TestCase):
    def test_normalizes_changed_pages_from_diff_or_markdown_lines(self):
        self.assertEqual(normalize_changed_page("- runtimes/react/data-binding"), "runtimes/react/data-binding")
        self.assertEqual(normalize_changed_page("< abc123  editor/data-binding/overview"), "editor/data-binding/overview")
        self.assertEqual(normalize_changed_page("> def456  scripting/protocols/converter-scripts"), "scripting/protocols/converter-scripts")
        self.assertEqual(normalize_changed_page("runtimes/web/web-js.mdx"), "runtimes/web/web-js")

    def test_source_matches_changed_page_for_exact_pages_and_directories(self):
        self.assertTrue(source_matches_changed_page("runtimes/react/data-binding", "runtimes/react/data-binding.mdx"))
        self.assertTrue(source_matches_changed_page("runtimes/react/data-binding", "runtimes/react/"))
        self.assertFalse(source_matches_changed_page("runtimes/reactive/data-binding", "runtimes/react/"))
        self.assertFalse(source_matches_changed_page("runtimes/react/data-binding", "runtimes/web/"))

    def test_collects_reference_recipe_and_eval_source_refs(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            reference = root / "rive-reference" / "03-data-binding.md"
            reference.parent.mkdir(parents=True)
            reference.write_text(
                textwrap.dedent(
                    """\
                    # Data Binding
                    > Last verified: 2026-04-23
                    > Source docs: `editor/data-binding/`, `runtimes/react/data-binding.mdx`
                    """
                ),
                encoding="utf-8",
            )
            recipe = root / "rive-recipes" / "state-machine-control.md"
            recipe.parent.mkdir(parents=True)
            recipe.write_text(
                "Verify `runtimes/react/data-binding.mdx` and `editor/state-machine/transitions.mdx`.",
                encoding="utf-8",
            )
            eval_case = root / "evals" / "cases" / "state-machine-modern-control.json"
            eval_case.parent.mkdir(parents=True)
            eval_case.write_text(
                """{
                  "id": "state-machine-modern-control",
                  "expected_source_paths": ["runtimes/react/data-binding.mdx"]
                }""",
                encoding="utf-8",
            )

            refs = collect_local_source_refs(root)

        self.assertIn(
            ImpactMatch("reference", "rive-reference/03-data-binding.md", "editor/data-binding/"),
            refs,
        )
        self.assertIn(
            ImpactMatch("recipe", "rive-recipes/state-machine-control.md", "editor/state-machine/transitions.mdx"),
            refs,
        )
        self.assertIn(
            ImpactMatch("eval", "evals/cases/state-machine-modern-control.json", "runtimes/react/data-binding.mdx"),
            refs,
        )

    def test_maps_changed_pages_to_local_files(self):
        matches = [
            ImpactMatch("reference", "rive-reference/03-data-binding.md", "editor/data-binding/"),
            ImpactMatch("recipe", "rive-recipes/custom-converter.md", "scripting/protocols/converter-scripts.mdx"),
            ImpactMatch("eval", "evals/cases/custom-converter-script.json", "scripting/protocols/converter-scripts.mdx"),
        ]

        mapped = map_changed_pages(
            ["editor/data-binding/overview", "scripting/protocols/converter-scripts"],
            matches,
        )

        self.assertEqual(
            mapped["editor/data-binding/overview"],
            [ImpactMatch("reference", "rive-reference/03-data-binding.md", "editor/data-binding/")],
        )
        self.assertEqual(
            mapped["scripting/protocols/converter-scripts"],
            [
                ImpactMatch("eval", "evals/cases/custom-converter-script.json", "scripting/protocols/converter-scripts.mdx"),
                ImpactMatch("recipe", "rive-recipes/custom-converter.md", "scripting/protocols/converter-scripts.mdx"),
            ],
        )

    def test_render_markdown_groups_changed_pages_and_local_files(self):
        mapped = {
            "editor/data-binding/overview": [
                ImpactMatch("reference", "rive-reference/03-data-binding.md", "editor/data-binding/"),
                ImpactMatch("eval", "evals/cases/data-driven-list-react.json", "editor/data-binding/overview.mdx"),
            ],
            "runtimes/web/web-js": [],
        }

        markdown = render_markdown(mapped)

        self.assertIn("### `editor/data-binding/overview`", markdown)
        self.assertIn("- `rive-reference/03-data-binding.md` (reference, via `editor/data-binding/`)", markdown)
        self.assertIn("- `evals/cases/data-driven-list-react.json` (eval, via `editor/data-binding/overview.mdx`)", markdown)
        self.assertIn("### `runtimes/web/web-js`", markdown)
        self.assertIn("- No local files matched.", markdown)

    def test_repo_changed_docs_mapping_finds_real_files(self):
        refs = collect_local_source_refs(ROOT)
        mapped = map_changed_pages(
            [
                "editor/data-binding/overview",
                "runtimes/react/data-binding",
                "scripting/protocols/converter-scripts",
            ],
            refs,
        )

        flattened = {
            match.local_file
            for matches in mapped.values()
            for match in matches
        }

        self.assertIn("rive-reference/03-data-binding.md", flattened)
        self.assertIn("rive-reference/05-scripting.md", flattened)
        self.assertIn("rive-recipes/custom-converter.md", flattened)
        self.assertIn("evals/cases/custom-converter-script.json", flattened)


if __name__ == "__main__":
    unittest.main()
