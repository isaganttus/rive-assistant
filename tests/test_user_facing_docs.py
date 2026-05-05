import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SETUP_PAGES = {
    "Codex": "docs/setup/codex.md",
    "Claude Code": "docs/setup/claude-code.md",
    "Gemini CLI": "docs/setup/gemini-cli.md",
    "Cursor": "docs/setup/cursor.md",
    "Windsurf": "docs/setup/windsurf.md",
    "GitHub Copilot": "docs/setup/github-copilot.md",
}

GOAL_PROMPTS = {
    "confirm-context-loaded.md",
    "build-a-dynamic-ui.md",
    "choose-a-runtime.md",
    "fix-outdated-rive-advice.md",
    "write-a-converter-script.md",
}


class UserFacingDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_readme_has_start_here_paths_for_new_users(self):
        readme = self.read("README.md")

        self.assertIn("Start here", readme)
        self.assertIn("docs/quickstart.md", readme)
        self.assertIn("docs/troubleshooting.md", readme)
        for path in SETUP_PAGES.values():
            self.assertIn(path, readme)

    def test_quickstart_routes_to_setup_smoke_tests_and_examples(self):
        quickstart = self.read("docs/quickstart.md")

        for tool, path in SETUP_PAGES.items():
            self.assertIn(tool, quickstart)
            self.assertIn(path.replace("docs/", ""), quickstart)

        self.assertIn("docs/smoke-testing.md", quickstart)
        self.assertIn("examples/prompts/", quickstart)
        self.assertIn("examples/conversations/", quickstart)
        self.assertIn("Data Binding", quickstart)
        self.assertIn("View Models", quickstart)

    def test_setup_pages_exist_and_name_their_context_files(self):
        context_files = {
            "Codex": "AGENTS.md",
            "Claude Code": "CLAUDE.md",
            "Gemini CLI": "GEMINI.md",
            "Cursor": ".cursor/rules/rive.mdc",
            "Windsurf": ".windsurfrules",
            "GitHub Copilot": ".github/copilot-instructions.md",
        }

        for tool, path in SETUP_PAGES.items():
            content = self.read(path)
            self.assertIn(tool, content)
            self.assertIn(context_files[tool], content)
            self.assertIn("Smoke test", content)
            self.assertIn("Troubleshooting", content)

    def test_troubleshooting_covers_common_user_failures(self):
        troubleshooting = self.read("docs/troubleshooting.md")

        for phrase in (
            "generic answers",
            "deprecated Inputs",
            "cannot fetch",
            "does not seem to load",
            "outdated",
        ):
            self.assertIn(phrase, troubleshooting)

    def test_examples_are_organized_by_user_goal(self):
        prompt_names = {path.name for path in (ROOT / "examples" / "prompts").glob("*.md")}
        self.assertEqual(prompt_names, GOAL_PROMPTS)

        for prompt_name in GOAL_PROMPTS:
            content = self.read(f"examples/prompts/{prompt_name}")
            self.assertIn("## User Goal", content)
            self.assertIn("## Prompt", content)
            self.assertIn("## Good Answer Should Mention", content)
            self.assertIn("## Red Flags", content)

    def test_example_conversations_exist_for_core_user_workflows(self):
        conversation_files = sorted((ROOT / "examples" / "conversations").glob("*.md"))

        self.assertGreaterEqual(len(conversation_files), 4)
        for conversation_path in conversation_files:
            content = conversation_path.read_text(encoding="utf-8")
            self.assertIn("## User", content, conversation_path.name)
            self.assertIn("## Assistant", content, conversation_path.name)
            self.assertIn("## Why This Is Good", content, conversation_path.name)
            self.assertIn("rive-reference/", content, conversation_path.name)

    def test_user_facing_markdown_links_point_to_existing_repo_paths(self):
        markdown_files = [
            ROOT / "README.md",
            ROOT / "docs" / "quickstart.md",
            ROOT / "docs" / "smoke-testing.md",
            ROOT / "docs" / "troubleshooting.md",
            *sorted((ROOT / "docs" / "setup").glob("*.md")),
            *sorted((ROOT / "examples" / "prompts").glob("*.md")),
            *sorted((ROOT / "examples" / "conversations").glob("*.md")),
        ]
        link_pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")

        for markdown_path in markdown_files:
            content = markdown_path.read_text(encoding="utf-8")
            for target in link_pattern.findall(content):
                if "://" in target or target.startswith("#") or target.startswith("../../"):
                    continue
                clean_target = target.split("#", 1)[0]
                resolved = (markdown_path.parent / clean_target).resolve()
                self.assertTrue(
                    resolved.exists(),
                    f"{markdown_path.relative_to(ROOT)} links to missing path {target}",
                )


if __name__ == "__main__":
    unittest.main()
