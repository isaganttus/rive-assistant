import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ReleaseDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_release_guide_exists_and_defines_date_tags(self):
        guide = self.read("docs/releasing.md")

        self.assertIn("# Releasing", guide)
        self.assertIn("vYYYY.MM.DD", guide)
        self.assertIn("git tag -a vYYYY.MM.DD", guide)
        self.assertIn("git push origin vYYYY.MM.DD", guide)

    def test_release_guide_lists_required_validation_commands(self):
        guide = self.read("docs/releasing.md")

        self.assertIn("python3 -m unittest discover -s tests", guide)
        self.assertIn("python3 scripts/validate_doc_paths.py", guide)
        self.assertIn("python3 scripts/validate_tool_context_sync.py", guide)
        self.assertIn("python3 scripts/validate_answer_evals.py", guide)

    def test_readme_explains_main_vs_tagged_releases(self):
        readme = self.read("README.md")

        self.assertIn("Use `main` for the freshest Rive docs tracking", readme)
        self.assertIn("Use tagged releases for stable assistant snapshots", readme)
        self.assertIn("docs/releasing.md", readme)

    def test_contributing_mentions_release_process(self):
        contributing = self.read("CONTRIBUTING.md")

        self.assertIn("docs/releasing.md", contributing)
        self.assertIn("release checklist", contributing)

    def test_pr_template_mentions_release_checklist_when_release_related(self):
        template = self.read(".github/PULL_REQUEST_TEMPLATE.md")

        self.assertIn("Release checklist reviewed if this PR prepares a release", template)


if __name__ == "__main__":
    unittest.main()
