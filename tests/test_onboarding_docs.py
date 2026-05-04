import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class OnboardingDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_codex_context_file_exists_and_routes_to_rive_references(self):
        agents = self.read("AGENTS.md")

        self.assertIn("# Rive Expert Assistant", agents)
        self.assertIn("Codex", agents)
        self.assertIn("rive-reference/", agents)
        self.assertIn("rive-recipes/", agents)
        self.assertIn("Legacy Inputs and Events are deprecated", agents)
        self.assertIn("Data Binding with View Models", agents)

    def test_readme_lists_codex_and_agent_context_file(self):
        readme = self.read("README.md")

        self.assertIn("**Codex**", readme)
        self.assertIn("`AGENTS.md`", readme)
        self.assertIn("What this repo is", readme)
        self.assertIn("What this repo is not", readme)
        self.assertIn("Example questions", readme)

    def test_readme_describes_building_scope_without_overclaiming_all_rive_domains(self):
        readme = self.read("README.md")

        self.assertIn("building with Rive", readme)
        self.assertNotIn("covering every Rive domain", readme)

    def test_contributing_mentions_agents_context_sync(self):
        contributing = self.read("CONTRIBUTING.md")

        self.assertIn("`AGENTS.md`", contributing)
        self.assertIn("Codex", contributing)
        self.assertIn("python3 scripts/validate_tool_context_sync.py", contributing)


if __name__ == "__main__":
    unittest.main()
