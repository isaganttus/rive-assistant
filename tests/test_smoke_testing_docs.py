import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SMOKE_GUIDE = ROOT / "docs" / "smoke-testing.md"
PROMPTS_DIR = ROOT / "examples" / "prompts"


class SmokeTestingDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_readme_links_to_smoke_testing_guide_and_prompt_examples(self):
        readme = self.read("README.md")

        self.assertIn("docs/smoke-testing.md", readme)
        self.assertIn("examples/prompts/", readme)
        self.assertIn("Test your setup", readme)

    def test_smoke_testing_guide_covers_supported_tools(self):
        guide = SMOKE_GUIDE.read_text(encoding="utf-8")

        for tool in ("Codex", "Claude Code", "Gemini CLI", "Cursor", "Windsurf", "GitHub Copilot"):
            self.assertIn(tool, guide)

    def test_smoke_testing_guide_checks_modern_rive_guidance(self):
        guide = SMOKE_GUIDE.read_text(encoding="utf-8")

        self.assertIn("Data Binding", guide)
        self.assertIn("View Models", guide)
        self.assertIn("Legacy Inputs", guide)
        self.assertIn("deprecated", guide)
        self.assertIn("exact API signatures", guide)

    def test_prompt_examples_have_review_rubrics(self):
        prompt_files = sorted(PROMPTS_DIR.glob("*.md"))

        self.assertGreaterEqual(len(prompt_files), 4)
        for prompt_path in prompt_files:
            content = prompt_path.read_text(encoding="utf-8")
            self.assertIn("## Prompt", content, prompt_path.name)
            self.assertIn("## Good Answer Should Mention", content, prompt_path.name)
            self.assertIn("## Red Flags", content, prompt_path.name)
            self.assertIn("rive-reference/", content, prompt_path.name)

    def test_smoke_testing_markdown_links_point_to_existing_repo_paths(self):
        markdown_files = [SMOKE_GUIDE, *sorted(PROMPTS_DIR.glob("*.md"))]
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

        for markdown_path in markdown_files:
            content = markdown_path.read_text(encoding="utf-8")
            for target in link_pattern.findall(content):
                if "://" in target or target.startswith("#"):
                    continue
                clean_target = target.split("#", 1)[0]
                resolved = (markdown_path.parent / clean_target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"{markdown_path.relative_to(ROOT)} links to missing path {target}",
                )


if __name__ == "__main__":
    unittest.main()
