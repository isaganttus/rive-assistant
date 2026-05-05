# Roadmap

This roadmap describes the current direction for `rive-assistant`. It is intentionally pragmatic: keep the repo useful as a small AI context pack, make quality measurable, and avoid expanding into broad Rive product support or runtime-package territory.

## Now

- Keep stable releases flowing through release PRs and date-based tags.
- Keep repository validation healthy: docs paths, reference metadata, tool context sync, answer evals, and tests should pass before release.
- Maintain onboarding docs for supported AI tools so new users can confirm the Rive assistant context is loaded correctly.
- Keep the concept map and curated references aligned with upstream Rive docs changes.

## Next

- Expand answer-quality eval coverage for mobile runtimes, game runtimes, layouts, scripting data binding, and migration from legacy Inputs/Events.
- Add platform-specific recipes for Flutter, Apple, Android, React Native, Unity, and Unreal.
- Improve upstream docs drift PRs so they clearly identify affected references, recipes, and eval cases.
- Add small contributor guidance for choosing whether a change belongs in a reference file, recipe, eval, or tool context file.

## Later

- Make evals executable against real assistant responses, not only static rubrics.
- Generate tool context files from a shared source to reduce drift across Codex, Claude Code, Gemini, Cursor, Windsurf, and Copilot.
- Package `rive-assistant` for easier installation in AI tools where that ecosystem supports reusable context packs.
- Explore optional release automation for GitHub Releases once the manual release process is stable.

## Non-Goals

- Do not present this as an official Rive project unless Rive explicitly adopts it.
- Do not turn this repo into a Rive runtime package, app template, or `.riv` asset library.
- Do not broaden coverage into account, billing, marketplace, or general product-support docs unless the project scope changes.
