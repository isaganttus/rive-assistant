import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW_DIR = ROOT / ".github" / "workflows"

NODE24_ACTION_PINS = {
    "actions/checkout": {
        "ref": "de0fac2e4500dabe0009e67214ff5f5447ce83dd",
        "version_comment": "v6.0.2",
    },
    "peter-evans/create-pull-request": {
        "ref": "5f6978faf089d4d20b00c7766989d076bb2fc7f1",
        "version_comment": "v8.1.1",
    },
}


def workflow_uses_lines():
    pattern = re.compile(r"^\s*(?:-\s+)?uses:\s+([^@\s]+)@([a-f0-9]{40})(?:\s*#\s*(\S+))?")
    for workflow_path in sorted(WORKFLOW_DIR.glob("*.yml")):
        for line_number, line in enumerate(workflow_path.read_text(encoding="utf-8").splitlines(), 1):
            match = pattern.match(line)
            if match:
                yield workflow_path.relative_to(ROOT), line_number, match.groups()


class WorkflowActionsTest(unittest.TestCase):
    def test_workflow_names_describe_their_scope(self):
        expected_names = {
            "sync-docs-paths.yml": "name: Sync Rive docs paths",
            "sync-content-hashes.yml": "name: Sync Rive docs content hashes",
            "validate-doc-paths.yml": "name: Validate repository",
        }

        for workflow_name, expected_name in expected_names.items():
            workflow = (WORKFLOW_DIR / workflow_name).read_text(encoding="utf-8")
            self.assertIn(expected_name, workflow)

    def test_node_action_pins_use_node24_compatible_releases(self):
        checked_actions = set()

        for workflow_path, line_number, (action, ref, version_comment) in workflow_uses_lines():
            expected = NODE24_ACTION_PINS.get(action)
            if expected is None:
                continue

            checked_actions.add(action)
            location = f"{workflow_path}:{line_number}"
            self.assertEqual(ref, expected["ref"], location)
            self.assertEqual(version_comment, expected["version_comment"], location)

        self.assertEqual(checked_actions, set(NODE24_ACTION_PINS))

    def test_validate_workflow_runs_tool_context_sync_check(self):
        workflow = (WORKFLOW_DIR / "validate-doc-paths.yml").read_text(encoding="utf-8")

        self.assertIn("python3 scripts/validate_tool_context_sync.py", workflow)

    def test_validate_workflow_runs_answer_eval_check(self):
        workflow = (WORKFLOW_DIR / "validate-doc-paths.yml").read_text(encoding="utf-8")

        self.assertIn("python3 scripts/validate_answer_evals.py", workflow)

    def test_validate_workflow_runs_reference_metadata_check(self):
        workflow = (WORKFLOW_DIR / "validate-doc-paths.yml").read_text(encoding="utf-8")

        self.assertIn("python3 scripts/validate_reference_metadata.py", workflow)

    def test_content_hash_workflow_maps_changed_docs_to_local_files(self):
        workflow = (WORKFLOW_DIR / "sync-content-hashes.yml").read_text(encoding="utf-8")

        self.assertIn("python3 scripts/map_changed_docs_to_local_files.py", workflow)
        self.assertIn("Likely local files to review", workflow)

    def test_sync_workflows_use_bot_token_for_pull_requests(self):
        for workflow_name in ("sync-docs-paths.yml", "sync-content-hashes.yml"):
            workflow = (WORKFLOW_DIR / workflow_name).read_text(encoding="utf-8")

            self.assertIn("token: ${{ secrets.RIVE_ASSISTANT_BOT_TOKEN }}", workflow)
            self.assertNotIn("token: ${{ secrets.GITHUB_TOKEN }}", workflow)


if __name__ == "__main__":
    unittest.main()
