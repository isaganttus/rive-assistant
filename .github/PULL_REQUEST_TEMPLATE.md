## What changed

<!-- Briefly describe what you updated and why -->

## Validation

<!-- Check the commands you ran. Leave unchecked if not applicable or not run, and explain why. -->

- [ ] `python3 -m unittest discover -s tests`
- [ ] `python3 scripts/validate_doc_paths.py`
- [ ] `python3 scripts/validate_reference_metadata.py`
- [ ] `python3 scripts/validate_tool_context_sync.py`
- [ ] `python3 scripts/validate_answer_evals.py`

## Checklist

Mark non-applicable items as `N/A`.

- [ ] Reference files edited are in `rive-reference/`, or N/A
- [ ] Information is sourced from official Rive docs, or N/A
- [ ] `rive-reference/00-concept-map.md` updated if new files were added or paths changed, or N/A
- [ ] Tool context files updated if assistant behavior changed (`AGENTS.md`, `CLAUDE.md`, `GEMINI.md`, Cursor, Windsurf, Copilot), or N/A
- [ ] `docs-paths.txt` not manually edited (it's auto-generated)
- [ ] Submodule pointer updated if `rive-docs/` was bumped, or N/A
- [ ] Release checklist reviewed if this PR prepares a release, or N/A
- [ ] Release PRs only: tag is created or moved after the PR is merged, not before, or N/A

## Source / References

<!-- Link official Rive docs, related issues, release checklist, or write N/A -->
