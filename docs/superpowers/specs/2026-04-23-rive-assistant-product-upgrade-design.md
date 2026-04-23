# rive-assistant Product Upgrade — Design Spec

**Date:** 2026-04-23
**Scope:** Full product upgrade across adoption, answer quality, and maintainability

---

## Background

rive-assistant is a Rive expert AI assistant framework: a CLAUDE.md system prompt + 11 curated reference files that can be dropped into any AI coding environment. The core infrastructure is solid — routing table, dual-mode docs, automated drift detection, security hygiene. This upgrade addresses three coordinated dimensions:

- **Adoption** — the product claims multi-tool support but only ships CLAUDE.md
- **Answer quality** — reference files explain concepts but not how to accomplish tasks
- **Maintainability** — routing table is duplicated in two files; content drift goes undetected

---

## Section 1: Structural Fixes

### 1a. Eliminate routing table duplication

**Problem:** `CLAUDE.md` contains a 35-row routing table mapping topics → reference files → MDX paths. `rive-reference/00-concept-map.md` contains the same information in a different layout, plus a "Common Questions" section. Both must be updated whenever a topic is added or a doc path changes.

**Fix:** Make `00-concept-map.md` the single authoritative source for all topic-to-path mappings. Shorten the routing table in `CLAUDE.md` to a directive and navigation rules only:

- Replace the full table in CLAUDE.md with: "For topic lookup, read `rive-reference/00-concept-map.md` first."
- Keep navigation rules inline in CLAUDE.md (e.g., "check reference files before fetching remotely", "verify API signatures against source docs before writing code").
- All MDX paths live only in `00-concept-map.md`.
- Merge CLAUDE.md's "Then if needed" guidance into the concept map table as a new column.

**Result:** One file to update when topics or paths change.

### 1b. Add releases and changelog

**Problem:** Users who cloned months ago have no signal that reference files have been substantially updated. The 3-failed-fetches warning only catches doc path drift.

**Fix:**
- Add `CHANGELOG.md` to the repo root, tracking substantive reference file updates and structural changes.
- Cut GitHub Releases when reference files are meaningfully updated (not for every commit — for meaningful content changes or new recipes).
- Add a note to the README's "Staying up to date" section pointing to the GitHub Releases tab for a summary of what changed.

---

## Section 2: Multi-Tool Support

**Problem:** The README says the assistant supports Cursor, Windsurf, Copilot Workspace, and Gemini CLI. But users on those tools must manually figure out how to load CLAUDE.md — there is no native context file for any of them.

**Fix:** Add four files targeting each tool's native loading convention.

| File | Tool | Loading mechanism |
|---|---|---|
| `GEMINI.md` | Gemini CLI | Auto-loaded from project root |
| `.cursor/rules/rive.mdc` | Cursor | Auto-loaded rules with `alwaysApply: true` frontmatter |
| `.windsurfrules` | Windsurf | Auto-loaded from project root |
| `.github/copilot-instructions.md` | GitHub Copilot | Auto-loaded for Copilot Chat in repo context |

**Content:** Each file carries the same role definition, Rive vocabulary, deprecation notices, and routing rules as CLAUDE.md, adapted where the tool requires it. Claude Code and Gemini CLI can fetch remote URLs; Cursor, Windsurf, and Copilot cannot. For the three non-fetching tools, the routing section should note "read local reference files only" and omit the GitHub fetch instructions entirely.

**README update:** Replace the current vague "consult your tool's docs" sentence with a dedicated per-tool setup section — one subsection per tool, with exact steps.

**Maintenance:** When CLAUDE.md is updated for content (new deprecation notice, new routing rule), the same change is applied to all four tool files. This is documented in CONTRIBUTING.md.

---

## Section 3: Recipe Library

**Problem:** Reference files explain what Rive concepts are. They do not answer how to accomplish common tasks end-to-end. Questions like "how do I build a data-driven list in React?" get scattered concept coverage but no complete pattern.

**Fix:** Add a `rive-recipes/` directory. Each recipe is a focused Markdown file: problem statement → editor setup steps → runtime code → cross-platform notes. Approximately 60–100 lines each, code-first.

### Initial recipe set (10 files)

| File | Topic |
|---|---|
| `data-driven-list.md` | View model + Artboard List + runtime binding |
| `scroll-view-react.md` | Scroll constraint + React runtime wiring |
| `audio-from-script.md` | Audio Events + `Audio:play*()` from Luau |
| `custom-converter.md` | Converter script (number → formatted string) |
| `animated-button.md` | State machine with hover/press/disabled states |
| `dynamic-text.md` | Text run bound to a view model string property |
| `out-of-band-assets.md` | Loading .riv + images/fonts separately |
| `state-machine-control.md` | Cross-platform pattern for triggering state machine from code |
| `custom-layout.md` | Layout script implementing masonry/carousel |
| `transition-condition-script.md` | Custom Luau transition logic |

### Recipe format

Each recipe follows a consistent structure:

```markdown
# [Recipe title]

**What this covers:** one sentence.
**Rive features used:** comma-separated list.

## Editor setup
Step-by-step, numbered, minimal prose.

## Runtime code
Default: JavaScript/TypeScript. Note platform differences inline.

## Notes
- Cross-platform caveats
- Common mistakes
- Links to relevant reference files
```

### CLAUDE.md addition

Add one line to the "How to Use the Reference System" section:

> If the user asks how to accomplish a specific task, check `rive-recipes/` before answering.

### CONTRIBUTING.md addition

Document the recipe format and a note that new recipes should follow the template in the first existing recipe file.

---

## Section 4: Reference File Improvements

### 4a. Consistency template

**Problem:** CONTRIBUTING.md says "match the existing tone and formatting" but provides no template. Contributors must infer structure from existing files, which themselves vary in structure and depth.

**Fix:** Add `rive-reference/TEMPLATE.md` with:
- Standard section headers and their purpose
- Tone guidance (technical, concise, no prose padding)
- Length target: 150–300 lines (revised down from the 250–400 stated in CLAUDE.md, which most files already fall short of; update CLAUDE.md's stated target to match)
- Code example conventions (minimal, illustrative, Luau or JS/TS)

Update CONTRIBUTING.md to reference the template explicitly.

### 4b. Depth pass on thin files

`09-game-runtimes.md` covers Unity, Unreal, and Defold in 102 lines. Unity and Unreal are major platforms with distinct APIs (RivePanel, RiveScreen, Blueprints, data binding integration). Expand coverage to match the depth of `07-web-react-runtime.md` (169 lines). Specifically, add:

- Unity: RivePanel vs RiveScreen use cases, data binding API, common setup patterns, StateMachine control
- Unreal: plugin setup, Blueprint vs C++ access, RiveActor, known limitations

Defold coverage can remain brief as it is a smaller platform.

### 4c. "Last verified" metadata

Add a single metadata line near the top of each reference file:

```markdown
> Last verified: 2026-04-23
```

This gives maintainers a staleness signal and gives the AI (and users) context when a reference file is cited. Update this line whenever the file's content is meaningfully reviewed against current Rive docs.

---

## Section 5: GitHub Action — Content Drift Detection

**Problem:** The existing Action detects when doc *paths* change (structural reorganization). It does not detect when the *content* of an existing doc page changes. If Rive rewrites an API without moving pages, reference files silently go stale.

**Fix:** Extend the existing `sync-docs-paths.yml` workflow (or add a second workflow) to hash the content of a curated list of ~15 critical-path doc pages — the pages most heavily referenced in the routing table.

### Critical path pages to monitor (initial list)

```
editor/data-binding/overview
editor/data-binding/lists
scripting/getting-started
scripting/protocols/node-scripts
scripting/protocols/converter-scripts
runtimes/web/web-js
runtimes/react/react
runtimes/flutter/flutter
runtimes/apple/apple
runtimes/android/android
editor/state-machine/state-machine
editor/state-machine/listeners
editor/state-machine/transitions
editor/layouts/overview
getting-started/best-practices
```

### Implementation

- Store current hashes in `docs-content-hashes.txt` (format: `<hash>  <path>`)
- Each Monday, re-fetch these pages and compare hashes
- When a hash changes, open a PR naming the specific changed page and which reference file it feeds, so the maintainer knows exactly what to review and update
- `docs-content-hashes.txt` is committed alongside path changes; the Action updates it automatically

### Scope discipline

Do not hash all ~200 docs pages. Keep the critical path list intentionally small. When a new reference file is added, its primary source pages are added to the list.

---

## Files Added / Changed

| Action | Path |
|---|---|
| Modified | `CLAUDE.md` — routing table replaced with directive + rules |
| Modified | `rive-reference/00-concept-map.md` — absorbs MDX paths from CLAUDE.md; new "Then if needed" column |
| Added | `CHANGELOG.md` |
| Added | `GEMINI.md` |
| Added | `.cursor/rules/rive.mdc` |
| Added | `.windsurfrules` |
| Added | `.github/copilot-instructions.md` |
| Added | `rive-recipes/` (10 files) |
| Added | `rive-reference/TEMPLATE.md` |
| Modified | `rive-reference/09-game-runtimes.md` — expanded Unity + Unreal sections |
| Modified | All `rive-reference/*.md` — add "Last verified" line |
| Modified | `CONTRIBUTING.md` — reference template, recipe format, multi-tool sync note |
| Modified | `README.md` — per-tool setup sections, changelog link |
| Modified | `.github/workflows/sync-docs-paths.yml` — add content hash monitoring |
| Added | `docs-content-hashes.txt` |

---

## Out of Scope

- Automated reference file updates (content is hand-curated by design)
- A web UI or hosted version of the assistant
- Support for tools beyond the four listed (can be added incrementally)
- More than 10 initial recipes (expand based on user questions over time)
