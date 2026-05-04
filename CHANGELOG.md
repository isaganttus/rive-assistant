# Changelog

All notable changes to rive-assistant are listed here. Updated when reference files or structural components change meaningfully.

Format: `[Unreleased]` at top, then dated entries in reverse chronological order.

---

## [Unreleased]

### Added
- Docs path validation script and GitHub Action to catch stale official Rive docs references.
- `AGENTS.md` for native Codex repo instructions.
- Onboarding documentation tests for supported AI tool setup.
- Tool context sync validator to catch drift across Codex, Claude Code, Gemini, Cursor, Windsurf, and Copilot instructions.
- Answer-quality eval cases and validator for representative Rive assistant questions.
- Release process documentation for date-based tags and validation requirements.
- Source traceability metadata and validation for curated reference files.

### Changed
- Updated concept-map and recipe source links to match current `docs-paths.txt`.
- Offline docs instructions now require initialized submodule content (`rive-docs/docs.json`) before using local docs.
- Content hash workflow now fails on fetch errors instead of opening partial update PRs.
- README now clarifies project scope, Codex setup, and example questions.

---

## [2026-04-23]

### Added
- `rive-recipes/` — 10 code-first recipes: animated button, dynamic text, state machine control, out-of-band assets, data-driven list, scroll view, audio from script, custom converter, custom layout, transition condition script
- `GEMINI.md` — native Gemini CLI context file
- `.cursor/rules/rive.mdc` — native Cursor rules file
- `.windsurfrules` — native Windsurf rules file
- `.github/copilot-instructions.md` — native GitHub Copilot instructions
- `rive-reference/TEMPLATE.md` — contributor template for new reference files
- `docs-content-hashes.txt` — tracked hashes for critical docs pages (content drift detection)
- GitHub Action for content drift detection (`.github/workflows/sync-content-hashes.yml`)

### Changed
- `CLAUDE.md` — replaced 35-row routing table with directive to `00-concept-map.md`; added recipe library pointer; updated line count target to 150–300
- `rive-reference/00-concept-map.md` — added usage preamble; clarified source path column
- `rive-reference/09-game-runtimes.md` — expanded Unity and Unreal sections with setup patterns and code examples
- All `rive-reference/*.md` — added "Last verified" date
- `README.md` — per-tool setup table; changelog link; updated what's included
- `CONTRIBUTING.md` — added template reference, recipe format, multi-tool sync note
