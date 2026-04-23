# rive-assistant Product Upgrade Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Upgrade rive-assistant across three dimensions: eliminate structural redundancy, add native multi-tool context files, add a recipe library, deepen reference coverage, and upgrade the GitHub Action to detect content drift.

**Architecture:** Pure Markdown repo with no build step. Changes are file additions and edits. The GitHub Action extension adds a second YAML workflow and a new tracked file. All tasks are independent except: Tasks 5–8 (multi-tool files) depend on Task 1 (CLAUDE.md restructure) completing first.

**Tech Stack:** Markdown, YAML, Python (GitHub Actions), bash

---

## Phase 1: Structural Fixes

---

### Task 1: Restructure CLAUDE.md — replace routing table with directive

**Files:**
- Modify: `CLAUDE.md` (lines 59–147, the "How to Use the Reference System" section)

- [ ] **Step 1: Open `CLAUDE.md` and locate the section to replace**

The section to replace runs from `## How to Use the Reference System` through `### Important: Always verify code against source docs`. Find it and replace the full section with the content below.

- [ ] **Step 2: Replace the "How to Use the Reference System" section**

Replace everything from line `## How to Use the Reference System` to the end of the file with:

```markdown
## How to Use the Reference System

### Curated reference files

`rive-reference/` contains curated summaries — one file per domain, 150–300 lines each. These cover concepts, patterns, and common API shapes. **Start here for every question.**

### Recipes

For common task patterns ("how do I build a scrolling list?", "how do I trigger audio from Luau?"), check `rive-recipes/` before answering. Each recipe is a complete, code-first worked example.

### Full source documentation

When you need exact API signatures or details not in the reference files, read the full docs. Two modes are supported:

**Default — fetch on demand:**
Fetch pages directly from the official Rive docs repository on GitHub:
```
https://raw.githubusercontent.com/rive-app/rive-docs/main/<path>
```
Example: to read `editor/state-machine/listeners.mdx`, fetch:
```
https://raw.githubusercontent.com/rive-app/rive-docs/main/editor/state-machine/listeners.mdx
```

**Offline opt-in:**
If the user cloned this repo with `--recurse-submodules`, the full docs are available locally at `rive-docs/`. Check for the existence of `rive-docs/` before fetching remotely — if it exists, read from there instead.

The directory structure is the same in both cases:
```
editor/           — Editor docs (fundamentals, state-machine, data-binding, layouts, constraints, text, events)
runtimes/         — App runtimes (web/, react/, react-native/, flutter/, apple/, android/)
game-runtimes/    — Game engines (unity/, unreal/, defold.mdx)
scripting/        — Scripting API (protocols/, api-reference/, debugging/)
getting-started/  — Introduction and best practices
docs.json         — Full navigation structure
```

### Navigation rules

For topic lookup, start with `rive-reference/00-concept-map.md`. It maps every Rive topic to the relevant reference file and official documentation path.

**Navigation principles:**
- Check `rive-reference/` files before fetching remotely
- For task patterns, check `rive-recipes/` first
- Verify API signatures against source docs before writing code
- For cross-platform questions, cover the general pattern first, then platform specifics

### If a fetch returns 404

Fetch `docs.json` from the root to discover the correct path:
```
https://raw.githubusercontent.com/rive-app/rive-docs/main/docs.json
```
Search the `pages` arrays for the topic, then construct the correct URL with the path found there.

If **3 or more** fetches in a session return 404 (even after consulting `docs.json`), warn the user:

> Several documentation paths couldn't be found. The routing table in this repo may be out of date with the current Rive docs structure. Consider running `git pull` in your `rive-assistant` folder to get the latest version.

### Important: Always verify code against source docs

The reference files contain concepts and patterns but may not have exact, up-to-date API signatures. When writing code, read the relevant source file to confirm current API details.
```

- [ ] **Step 3: Verify the file**

Read `CLAUDE.md` and confirm:
- The 35-row routing table is gone
- The new section is present with the directive to use `00-concept-map.md`
- The `rive-recipes/` note is present
- The 404 fallback and code verification notes are preserved
- The line count target now says 150–300 (not 250–400)

- [ ] **Step 4: Commit**

```bash
git add CLAUDE.md
git commit -m "Restructure CLAUDE.md: replace routing table with concept-map directive"
```

---

### Task 2: Update 00-concept-map.md — add preamble and "Then if needed" guidance

**Files:**
- Modify: `rive-reference/00-concept-map.md`

The concept map already has all the topic→path mappings. This task adds a preamble that explains how to use the file (since CLAUDE.md now defers to it), and renames "Source MDX" to "Source path(s)" with a note about what "then if needed" means.

- [ ] **Step 1: Add preamble below the title**

After `# Rive Concept Map` and before `Master lookup table. Use this to find where information lives.`, insert:

```markdown
> **How to use this file:** When asked about a Rive topic, find the row matching your topic. Read the **Reference File** first — it covers the concept. If you need exact API signatures or deeper detail, fetch the **Source path(s)** from the official Rive docs at `https://raw.githubusercontent.com/rive-app/rive-docs/main/<path>.mdx` (or read from `rive-docs/` if available locally).
```

- [ ] **Step 2: Rename the "Source MDX" column header to "Source path(s) — fetch for full API detail"**

In each table header row, change:
```
| Topic | Reference File | Source MDX |
```
to:
```
| Topic | Reference File | Source path(s) — fetch for full API detail |
```

There are 6 tables in the file. Apply the rename to all of them.

- [ ] **Step 3: Verify**

Read `rive-reference/00-concept-map.md` and confirm:
- Preamble is present at the top
- All 6 table headers use the new column name
- No content rows were changed

- [ ] **Step 4: Commit**

```bash
git add rive-reference/00-concept-map.md
git commit -m "Update concept map: add usage preamble, clarify source path column"
```

---

### Task 3: Add "Last verified" metadata to all reference files

**Files:**
- Modify: all 11 files in `rive-reference/` (including `00-concept-map.md`)

- [ ] **Step 1: Add the metadata line to each file**

For each file listed below, insert this line immediately after the `# Title` line (before `## Overview` or any other content):

```markdown
> Last verified: 2026-04-23
```

Files to update (add the line after the `#` title in each):
- `rive-reference/00-concept-map.md`
- `rive-reference/01-editor-fundamentals.md`
- `rive-reference/02-state-machines-and-events.md`
- `rive-reference/03-data-binding.md`
- `rive-reference/04-layouts.md`
- `rive-reference/05-scripting.md`
- `rive-reference/06-runtimes-overview.md`
- `rive-reference/07-web-react-runtime.md`
- `rive-reference/08-mobile-runtimes.md`
- `rive-reference/09-game-runtimes.md`
- `rive-reference/10-best-practices.md`

- [ ] **Step 2: Verify one file as a spot check**

Read `rive-reference/03-data-binding.md` and confirm the second line reads `> Last verified: 2026-04-23`.

- [ ] **Step 3: Commit**

```bash
git add rive-reference/
git commit -m "Add last-verified metadata to all reference files"
```

---

### Task 4: Add reference file template

**Files:**
- Create: `rive-reference/TEMPLATE.md`
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Create `rive-reference/TEMPLATE.md`**

```markdown
# [Domain Name] Reference

> Last verified: YYYY-MM-DD

## Overview

One paragraph covering what this domain does and its relationship to other Rive systems. Include the source docs path:

**Source docs**: `path/to/section/` directory in the Rive docs.

## [Main Concept or System]

### [Sub-concept]

Short description. Use tables for structured data. Use code blocks for API shapes.

```language
// Minimal illustrative example, not a full app
```

### [Another sub-concept]

...

## [Second Main Concept]

...

## Best Practices

Numbered list, 5–10 items. Actionable advice, not feature descriptions.

---

## Template notes (delete before committing)

- Target length: 150–300 lines
- Tone: technical, concise, no prose padding
- Code examples: minimal and illustrative; Luau or JS/TS by default
- One `## Overview` section; then domain-specific `##` sections; end with `## Best Practices`
- Tables for structured comparisons; code blocks for API shapes; prose only for concepts that resist tabular form
- Don't repeat information already in CLAUDE.md's vocabulary section
- Source every claim: if you're not sure, fetch the source doc and verify
```

- [ ] **Step 2: Add template reference to CONTRIBUTING.md**

In `CONTRIBUTING.md`, in the "Updating reference files" section, add after "When editing:" and its bullet list:

```markdown
See `rive-reference/TEMPLATE.md` for the standard file structure, tone guidance, and length target.
```

- [ ] **Step 3: Commit**

```bash
git add rive-reference/TEMPLATE.md CONTRIBUTING.md
git commit -m "Add reference file template and link from CONTRIBUTING"
```

---

### Task 5: Expand 09-game-runtimes.md — Unity and Unreal depth pass

**Files:**
- Modify: `rive-reference/09-game-runtimes.md`

- [ ] **Step 1: Fetch Unity and Unreal source docs**

Fetch these pages and read them before writing content:

```
https://raw.githubusercontent.com/rive-app/rive-docs/main/game-runtimes/unity/unity.mdx
https://raw.githubusercontent.com/rive-app/rive-docs/main/game-runtimes/unity/getting-started.mdx
https://raw.githubusercontent.com/rive-app/rive-docs/main/game-runtimes/unreal/unreal.mdx
https://raw.githubusercontent.com/rive-app/rive-docs/main/game-runtimes/unreal/getting-started.mdx
```

If any 404s, check `docs.json` for the correct paths.

- [ ] **Step 2: Expand the Unity section**

Replace the current Unity section (everything from `## Unity` to before `## Unreal Engine`) with a fuller version based on what the source docs contain. The expanded section should cover at minimum:

- Installation (UPM setup steps)
- RivePanel vs RiveScreen — when to use each, hierarchy setup
- Procedural rendering to texture — when to use, setup steps
- C# data binding API — how to get a view model instance, read/write properties, subscribe to changes (with code example)
- State machine control from C#
- Asset loading and runtime asset swapping
- Pointer/input forwarding behavior

Target length: 60–80 lines for the Unity section.

- [ ] **Step 3: Expand the Unreal section**

Replace the current Unreal section with a fuller version. Should cover at minimum:

- Installation (Marketplace vs GitHub)
- RiveActor and its role
- Blueprint integration — how to observe properties and fire triggers (with Blueprint node examples described in text)
- C++ integration — how to access view model, set properties, bind callbacks (with code example)
- In-world texture rendering — RiveTexture setup
- Known limitations or platform considerations

Target length: 50–70 lines for the Unreal section.

- [ ] **Step 4: Verify the file**

Read `rive-reference/09-game-runtimes.md`. Confirm:
- File is ≥ 160 lines (up from 102)
- Unity section has a C# code example
- Unreal section has either a Blueprint description or C++ code example
- `> Last verified: 2026-04-23` is present (from Task 3)
- The "Key Differences" and "Common Patterns" sections are preserved

- [ ] **Step 5: Commit**

```bash
git add rive-reference/09-game-runtimes.md
git commit -m "Expand game runtimes reference: deeper Unity and Unreal coverage"
```

---

## Phase 2: Multi-Tool Support

---

### Task 6: Add GEMINI.md

**Files:**
- Create: `GEMINI.md`

Gemini CLI auto-loads `GEMINI.md` from the project root and supports remote URL fetching. Content is identical to the restructured `CLAUDE.md`.

- [ ] **Step 1: Copy CLAUDE.md to GEMINI.md**

```bash
cp CLAUDE.md GEMINI.md
```

- [ ] **Step 2: Verify**

Read `GEMINI.md` and confirm it matches `CLAUDE.md` exactly.

- [ ] **Step 3: Commit**

```bash
git add GEMINI.md
git commit -m "Add GEMINI.md for Gemini CLI support"
```

---

### Task 7: Add .cursor/rules/rive.mdc

**Files:**
- Create: `.cursor/rules/rive.mdc`

Cursor auto-loads rules from `.cursor/rules/`. The `.mdc` format requires YAML frontmatter. Cursor cannot fetch remote URLs during a session, so the "Full source documentation" section is replaced with a note directing users to the official docs.

- [ ] **Step 1: Create the directory**

```bash
mkdir -p .cursor/rules
```

- [ ] **Step 2: Create `.cursor/rules/rive.mdc`**

The file content is: YAML frontmatter, then the full content of `CLAUDE.md` with one section replaced. Write the file as follows:

**Frontmatter (first 4 lines):**
```
---
description: Rive expert assistant — loaded for all sessions
alwaysApply: true
---
```

**Body:** Copy all sections from `CLAUDE.md` verbatim, except replace the entire "### Full source documentation" subsection (from that heading through the directory structure code block) with:

```markdown
### Full source documentation

Cursor cannot fetch remote URLs during a session. When the curated reference files do not contain sufficient detail, direct the user to the official Rive documentation at https://rive.app/docs, or ask them to paste the relevant page from https://github.com/rive-app/rive-docs into the conversation.

The docs are organized as:
```
editor/           — Editor docs (fundamentals, state-machine, data-binding, layouts, constraints, text, events)
runtimes/         — App runtimes (web/, react/, react-native/, flutter/, apple/, android/)
game-runtimes/    — Game engines (unity/, unreal/, defold.mdx)
scripting/        — Scripting API (protocols/, api-reference/, debugging/)
getting-started/  — Introduction and best practices
```
```

Also remove the "### If a fetch returns 404" subsection entirely (not applicable without fetching).

- [ ] **Step 3: Verify**

Read `.cursor/rules/rive.mdc` and confirm:
- YAML frontmatter is present with `alwaysApply: true`
- Role, vocabulary, deprecation notices are present
- "Full source documentation" section has the no-fetch variant
- "If a fetch returns 404" section is absent
- Navigation rules directive to `00-concept-map.md` is present
- Recipe note is present

- [ ] **Step 4: Commit**

```bash
git add .cursor/
git commit -m "Add Cursor rules file (.cursor/rules/rive.mdc)"
```

---

### Task 8: Add .windsurfrules

**Files:**
- Create: `.windsurfrules`

Windsurf auto-loads `.windsurfrules` from the project root. Same content as `.cursor/rules/rive.mdc` but without the YAML frontmatter (plain Markdown only).

- [ ] **Step 1: Create `.windsurfrules`**

Write the file with the same body as `.cursor/rules/rive.mdc` but without the YAML frontmatter block. The file starts directly with `# Rive Expert Assistant`.

Apply the same modifications as Task 7:
- No-fetch variant of "### Full source documentation"
- No "### If a fetch returns 404" section

- [ ] **Step 2: Verify**

Read `.windsurfrules` and confirm:
- No YAML frontmatter (file starts with `# Rive Expert Assistant`)
- Role, vocabulary, deprecation notices are present
- No-fetch "Full source documentation" section is present
- No "If a fetch returns 404" section

- [ ] **Step 3: Commit**

```bash
git add .windsurfrules
git commit -m "Add Windsurf rules file (.windsurfrules)"
```

---

### Task 9: Add .github/copilot-instructions.md

**Files:**
- Create: `.github/copilot-instructions.md`

GitHub Copilot Chat auto-loads `.github/copilot-instructions.md` when working in the repo context. Same content as `.windsurfrules` (plain Markdown, no YAML frontmatter, no-fetch variant).

- [ ] **Step 1: Create `.github/copilot-instructions.md`**

Write the file with identical content to `.windsurfrules` (same no-fetch adaptations, no frontmatter).

- [ ] **Step 2: Verify**

Read `.github/copilot-instructions.md` and confirm it matches `.windsurfrules` exactly.

- [ ] **Step 3: Commit**

```bash
git add .github/copilot-instructions.md
git commit -m "Add GitHub Copilot instructions file"
```

---

### Task 10: Update README.md — per-tool setup and changelog link

**Files:**
- Modify: `README.md`

- [ ] **Step 1: Replace the "Usage" section**

Find the current `## Usage` section:
```markdown
## Usage

### AI coding tools

Open the cloned folder as your working directory. The `CLAUDE.md` file is picked up automatically as project context in Claude Code. For other tools (Cursor, Windsurf, Copilot Workspace, etc.), consult your tool's docs for how to load a custom rules or system prompt file, then point it at `CLAUDE.md`.

### Other AI tools

Use the contents of `CLAUDE.md` as a system prompt, and make the `rive-reference/` files available to your tool as context or attachments.
```

Replace it with:

```markdown
## Usage

Open the cloned folder as your working directory. Each supported tool picks up its context file automatically — no extra configuration needed.

| Tool | Context file | Notes |
|---|---|---|
| **Claude Code** | `CLAUDE.md` | Auto-loaded. Supports remote docs fetching. |
| **Gemini CLI** | `GEMINI.md` | Auto-loaded. Supports remote docs fetching. |
| **Cursor** | `.cursor/rules/rive.mdc` | Auto-loaded (`alwaysApply: true`). |
| **Windsurf** | `.windsurfrules` | Auto-loaded from project root. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Auto-loaded for Copilot Chat. |

**Claude Code and Gemini CLI** fetch official documentation pages on demand for exact API signatures. **Cursor, Windsurf, and Copilot** use the local `rive-reference/` files only — for exact API details, paste the relevant page from [rive-app/rive-docs](https://github.com/rive-app/rive-docs) into the conversation.

### Other tools

Copy the contents of `CLAUDE.md` as a system prompt and make the `rive-reference/` directory available as context or attachments.
```

- [ ] **Step 2: Update the "Staying up to date" section**

Find the current section and add a line about releases. After the `git pull` instruction, add:

```markdown
Check the [Releases](../../releases) tab on GitHub for a summary of what changed in each update.
```

- [ ] **Step 3: Update the "What's included" section**

In the `## What's included` section, add two new bullets:

```markdown
- **`rive-recipes/`** — 10 code-first recipes for common Rive tasks
- **`GEMINI.md`, `.cursor/rules/rive.mdc`, `.windsurfrules`, `.github/copilot-instructions.md`** — Native context files for Gemini CLI, Cursor, Windsurf, and GitHub Copilot
```

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "Update README: per-tool setup table, what's included, releases link"
```

---

## Phase 3: Recipe Library

The next 10 tasks each create one recipe file. All recipes go in `rive-recipes/`. Each task follows the same pattern: fetch source docs if needed, write the file, verify, commit.

---

### Task 11: Recipe — animated-button.md

**Files:**
- Create: `rive-recipes/animated-button.md`

This recipe uses only editor-side concepts (state machine + listeners + view model) well covered by existing reference files. No source doc fetch needed.

- [ ] **Step 1: Create `rive-recipes/animated-button.md`**

```markdown
# Animated Button (hover / press / disabled)

**What this covers:** A button artboard with idle, hover, pressed, and disabled visual states driven by a state machine, wired to pointer interaction via listeners.
**Rive features used:** State machine, animation states, transitions, listeners, view model (boolean properties).

## Editor setup

1. Create an artboard sized to your button (e.g. 200×56).
2. Create three timeline animations: `Idle`, `Hover`, `Pressed`. Animate fill/scale/shadow as needed.
3. Create a **View Model** named `ButtonVM` with two boolean properties: `isHovered`, `isDisabled`.
4. Create a **State Machine** named `ButtonSM`.
5. In the state machine graph, add animation states for `Idle`, `Hover`, `Pressed`.
6. Wire transitions:
   - `Idle → Hover`: condition `isHovered == true`
   - `Hover → Idle`: condition `isHovered == false`
   - `Hover → Pressed`: condition on Pointer Down (use a Listener instead — see step 8)
   - `Pressed → Hover`: on Pointer Up
   - `Any State → Idle`: condition `isDisabled == true` (use **Any State** connection)
7. Add a **View Model Instance** from `ButtonVM`, mark it **Exported**, name it `button`.
8. Add two **Listeners** on the button shape:
   - Pointer Enter → View Model Change → `isHovered = true`
   - Pointer Exit → View Model Change → `isHovered = false`
9. For the pressed state: add two more Listeners:
   - Pointer Down → add a Listener Action → View Model Change → trigger `Pressed` state by binding a trigger property, **or** wire directly via transition exit time to pointer events.
   - Pointer Up → return to Hover

> **Simpler press approach:** Add a boolean `isPressed` to `ButtonVM`. Listener Pointer Down sets `isPressed = true`, Pointer Up sets `isPressed = false`. Transition condition: `isPressed == true`.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";

function Button({ label, disabled }: { label: string; disabled?: boolean }) {
  const { rive, RiveComponent } = useRive({
    src: "button.riv",
    stateMachines: "ButtonSM",
    autoplay: true,
  });

  // Sync disabled state from React props to the view model
  useEffect(() => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (vm) {
      vm.boolean("isDisabled").value = !!disabled;
    }
  }, [rive, disabled]);

  return <RiveComponent style={{ width: 200, height: 56 }} />;
}
```

> **API note:** Verify `rive.viewModelInstance` and `.boolean(name).value` against `runtimes/data-binding.mdx` for your runtime version.

## Notes

- Pointer events (hover/press) are handled entirely inside the .riv via Listeners — no JS event handlers needed.
- `isDisabled` is the only property the developer controls from code; interaction state is self-contained.
- For a non-React runtime, get the view model instance from your artboard or state machine object.
- Add `isDisabled` logic to the Any State → Idle transition so pressing a disabled button has no effect.
```

- [ ] **Step 2: Commit**

```bash
git add rive-recipes/animated-button.md
git commit -m "Add recipe: animated button with hover/press/disabled states"
```

---

### Task 12: Recipe — dynamic-text.md

**Files:**
- Create: `rive-recipes/dynamic-text.md`

- [ ] **Step 1: Create `rive-recipes/dynamic-text.md`**

```markdown
# Dynamic Text via Data Binding

**What this covers:** Binding a text object's content to a view model string property so it can be updated from code at runtime.
**Rive features used:** Text, view model (string property), data binding.

## Editor setup

1. Add a **Text** object to your artboard.
2. In the Data panel, create a **View Model** named `CardVM` with a string property `title` (default value: `"Placeholder"`).
3. Create a **View Model Instance**, mark it **Exported**, name it `card`.
4. Select the Text object. In the Inspector, find the **Text Run** (usually named `run`).
5. Click the binding icon next to the text run's value. Bind it to `card.title` (source-to-target, default direction).
6. Optionally bind `fontSize`, `fillColor`, or other properties to additional view model properties.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";

function Card({ title }: { title: string }) {
  const { rive, RiveComponent } = useRive({
    src: "card.riv",
    stateMachines: "CardSM",
    autoplay: true,
  });

  useEffect(() => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (vm) {
      vm.string("title").value = title;
    }
  }, [rive, title]);

  return <RiveComponent />;
}
```

**Web JS (no React):**
```javascript
const r = new rive.Rive({
  src: "card.riv",
  canvas: document.getElementById("canvas"),
  stateMachines: "CardSM",
  autoplay: true,
  onLoad: () => {
    r.resizeDrawingSurfaceToCanvas();
    r.viewModelInstance.string("title").value = "Hello World";
  },
});
```

> **API note:** Verify `viewModelInstance`, `.string(name).value` against `runtimes/data-binding.mdx`.

## Notes

- The binding updates on the next render frame — changes take effect immediately on the next animation tick.
- To bind multiple text runs (e.g. title + subtitle), add multiple string properties to the view model.
- For formatted numbers, use a **Converter** (number → string) instead of a raw string property. See the `custom-converter` recipe.
- The `run` name in the Rive editor is the Text Run name — check the hierarchy panel to confirm the exact name if multiple runs exist.
```

- [ ] **Step 2: Commit**

```bash
git add rive-recipes/dynamic-text.md
git commit -m "Add recipe: dynamic text via data binding"
```

---

### Task 13: Recipe — state-machine-control.md

**Files:**
- Create: `rive-recipes/state-machine-control.md`

- [ ] **Step 1: Fetch the runtime data binding docs**

```
https://raw.githubusercontent.com/rive-app/rive-docs/main/runtimes/data-binding.mdx
```

Read it to verify the API methods for getting view model instances and working with boolean/trigger properties. Use the actual method names from the docs in the recipe below.

- [ ] **Step 2: Create `rive-recipes/state-machine-control.md`** (update API calls based on Step 1)

```markdown
# State Machine Control from Code

**What this covers:** Driving state machine transitions from runtime code using view model properties — the modern replacement for legacy Inputs.
**Rive features used:** State machine, view model (boolean + trigger properties), data binding.

## Editor setup

1. Create a **View Model** named `PlayerVM` with:
   - Boolean `isRunning`
   - Trigger `jump`
2. Create a **View Model Instance**, mark **Exported**, name it `player`.
3. In the state machine, add transition conditions bound to these properties:
   - `Idle → Run`: condition `isRunning == true`
   - `Run → Idle`: condition `isRunning == false`
   - `Any State → Jump`: condition on `jump` trigger

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";
import { useEffect, useRef } from "react";

function Player() {
  const { rive, RiveComponent } = useRive({
    src: "player.riv",
    stateMachines: "PlayerSM",
    autoplay: true,
  });

  const vmRef = useRef<any>(null);

  useEffect(() => {
    if (!rive) return;
    vmRef.current = rive.viewModelInstance;
  }, [rive]);

  const setRunning = (running: boolean) => {
    vmRef.current?.boolean("isRunning").value = running;
  };

  const triggerJump = () => {
    vmRef.current?.trigger("jump").fire();
  };

  return (
    <>
      <RiveComponent />
      <button onMouseDown={() => setRunning(true)} onMouseUp={() => setRunning(false)}>
        Run
      </button>
      <button onClick={triggerJump}>Jump</button>
    </>
  );
}
```

**Cross-platform pattern:**

All runtimes expose the view model instance from the artboard or Rive object. The property access pattern is consistent:
- Boolean: `vm.boolean("name").value = true`
- Number: `vm.number("name").value = 42`
- String: `vm.string("name").value = "hello"`
- Trigger: `vm.trigger("name").fire()`

> **API note:** Verify exact method names against `runtimes/data-binding.mdx` and your platform's runtime docs.

## Notes

- **Do not use legacy Inputs** (`rive.stateMachineInputs()`). They are deprecated and have limited type support. Use view model properties instead.
- Triggers fire once then reset — use them for one-shot events (jump, attack). Use booleans for sustained states (running, hovered).
- View model properties can also be observed: subscribe to change events instead of polling.
- For listening to view model changes from code, see `runtimes/data-binding.mdx` for the subscribe API.
```

- [ ] **Step 3: Commit**

```bash
git add rive-recipes/state-machine-control.md
git commit -m "Add recipe: state machine control from runtime code"
```

---

### Task 14: Recipe — out-of-band-assets.md

**Files:**
- Create: `rive-recipes/out-of-band-assets.md`

- [ ] **Step 1: Create `rive-recipes/out-of-band-assets.md`**

```markdown
# Out-of-Band Asset Loading

**What this covers:** Loading images and fonts separately from the .riv file to reduce bundle size and enable asset reuse or dynamic swapping.
**Rive features used:** Asset loading, `assetLoader` callback.

## Editor setup

1. Import your image or font into the Rive file as usual.
2. In the Assets panel, select the asset.
3. In the Inspector, under **Export Options**, set the asset to **Referenced** (not embedded). This removes it from the .riv and marks it as externally provided.
4. Note the asset's **name** — you'll use it to match assets at runtime.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";

const { rive, RiveComponent } = useRive({
  src: "file.riv",
  stateMachines: "SM",
  autoplay: true,
  assetLoader: (asset, bytes) => {
    // Return true if you handle this asset; false to use embedded fallback.
    if (asset.isImage && asset.name === "hero-image") {
      fetch("/images/hero.webp")
        .then((res) => res.arrayBuffer())
        .then((buffer) => {
          asset.decode(new Uint8Array(buffer));
        });
      return true;
    }
    if (asset.isFont && asset.name === "Inter") {
      fetch("/fonts/Inter.ttf")
        .then((res) => res.arrayBuffer())
        .then((buffer) => {
          asset.decode(new Uint8Array(buffer));
        });
      return true;
    }
    return false; // use embedded fallback for anything not handled
  },
});
```

**Asset swapping at runtime:**
```javascript
// Swap to a different image after load
const imageAsset = rive.assets.find((a) => a.name === "hero-image");
fetch("/images/hero-v2.webp")
  .then((res) => res.arrayBuffer())
  .then((buf) => imageAsset.decode(new Uint8Array(buf)));
```

> **API note:** Verify `asset.decode()`, `rive.assets`, and `assetLoader` callback signature against `runtimes/web/web-js.mdx` and `runtimes/loading-assets.mdx`.

## Notes

- **Referenced vs Embedded**: Referenced = asset stripped from .riv, must be provided at runtime. Embedded = asset baked in (default).
- The `assetLoader` callback fires synchronously during Rive initialization — start the fetch immediately and call `asset.decode()` when data arrives.
- Out-of-band assets can be shared across multiple .riv files, reducing total network payload.
- For locale-based swapping (e.g. different flag images per region), use `assetLoader` to pick the correct asset based on `asset.name` and current locale.
- Flutter, iOS, Android, Unity, and Unreal all have equivalent asset loader APIs. See platform runtime docs.
```

- [ ] **Step 2: Commit**

```bash
git add rive-recipes/out-of-band-assets.md
git commit -m "Add recipe: out-of-band asset loading"
```

---

### Task 15: Recipe — data-driven-list.md

**Files:**
- Create: `rive-recipes/data-driven-list.md`

- [ ] **Step 1: Fetch source docs for lists**

```
https://raw.githubusercontent.com/rive-app/rive-docs/main/editor/data-binding/lists.mdx
https://raw.githubusercontent.com/rive-app/rive-docs/main/runtimes/data-binding.mdx
```

Read both to get the exact editor steps and runtime API for list manipulation.

- [ ] **Step 2: Create `rive-recipes/data-driven-list.md`** (update API details based on Step 1)

```markdown
# Data-Driven List

**What this covers:** A dynamically populated list in Rive driven by a view model List property, rendered via an Artboard List.
**Rive features used:** View model (List property), Artboard List, data binding, layouts.

## Editor setup

1. **Create the list item artboard** (e.g. `ListItem`, 360×64):
   - Add text and image objects for name, avatar, etc.
   - Create a View Model `ItemVM` with string `name`, string `subtitle`, etc.
   - Create an Exported View Model Instance `item`.
   - Bind text runs and image properties to `item.*`.

2. **Create the main artboard** (e.g. `FeedView`):
   - Add a Layout container for the scroll area (Hug width, Fill height or fixed height).
   - Inside the layout, add a child Layout for scroll content with a **Scroll Constraint** (direction: Vertical).
   - Inside the scroll content layout, add an **Artboard List** component.
   - Set the Artboard List's artboard template to `ListItem`.

3. **Create the feed view model**:
   - Create View Model `FeedVM` with a **List** property `items`, typed to `ItemVM`.
   - Create an Exported View Model Instance `feed`.
   - Bind the Artboard List to `feed.items`.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";

interface FeedItem {
  name: string;
  subtitle: string;
}

function Feed({ items }: { items: FeedItem[] }) {
  const { rive, RiveComponent } = useRive({
    src: "feed.riv",
    stateMachines: "FeedSM",
    autoplay: true,
  });

  useEffect(() => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (!vm) return;

    const list = vm.list("items");
    list.clear();

    for (const item of items) {
      const instance = list.createInstance();
      instance.string("name").value = item.name;
      instance.string("subtitle").value = item.subtitle;
      list.addInstance(instance);
    }
  }, [rive, items]);

  return <RiveComponent />;
}
```

> **API note:** `list.clear()`, `list.createInstance()`, `list.addInstance()` — verify exact method names against `runtimes/data-binding.mdx`. The list API may differ between runtime versions.

## Notes

- Artboard Lists inherit layout properties from their parent — wrapping, gap, padding, and scroll all come from the containing layout.
- For performance with large lists (100+ items), enable **Virtualize** on the Artboard List — only visible items are rendered.
- List instances are created from the view model template (`ItemVM`) — each instance is independent.
- To update a single item, get it by index via `list.getInstance(index)` and update its properties directly.
- The `items` React prop change triggers a full list rebuild here — for incremental updates in production, use `list.getInstance(i)` to update specific items rather than rebuilding the whole list.
```

- [ ] **Step 3: Commit**

```bash
git add rive-recipes/data-driven-list.md
git commit -m "Add recipe: data-driven list with Artboard List"
```

---

### Task 16: Recipe — scroll-view-react.md

**Files:**
- Create: `rive-recipes/scroll-view-react.md`

- [ ] **Step 1: Fetch scroll source docs**

```
https://raw.githubusercontent.com/rive-app/rive-docs/main/editor/layouts/scrolling.mdx
```

- [ ] **Step 2: Create `rive-recipes/scroll-view-react.md`**

```markdown
# Scroll View in React

**What this covers:** Building a vertical scroll view in Rive and controlling or reading the scroll position from React.
**Rive features used:** Layouts, Scroll Constraint, view model (optionally), data binding.

## Editor setup

Build this layout hierarchy:

```
Scroll View (Layout, fixed height e.g. 600)
  └─ Scroll Content (Layout + Scroll Constraint — direction: Vertical, physics: Elastic)
       ├─ Item 1 (Layout or Component)
       ├─ Item 2
       └─ Item N
```

1. Create the outer **Scroll View** layout: fixed width and height (the visible viewport).
2. Inside, add a **Scroll Content** layout: Hug height (grows to fit all items), same width as parent.
3. Add a **Scroll Constraint** to Scroll Content. Set:
   - Direction: Vertical
   - Physics: Elastic (iOS-style) or Clamped (basic)
4. Add your item layouts inside Scroll Content.
5. Optionally bind `Scroll Percent Y` (0–100) to a view model number property to expose scroll position to code.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";

function ScrollFeed() {
  const { rive, RiveComponent } = useRive({
    src: "feed.riv",
    stateMachines: "FeedSM",
    autoplay: true,
  });

  // Optional: programmatically scroll to top
  const scrollToTop = () => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (vm) {
      vm.number("scrollPercentY").value = 0;
    }
  };

  return (
    <>
      <RiveComponent style={{ width: 360, height: 600 }} />
      <button onClick={scrollToTop}>Back to top</button>
    </>
  );
}
```

> Pointer/touch events are forwarded to the Rive instance automatically by the React runtime — user scrolling works without any extra event wiring.

## Notes

- Rive handles scroll physics and pointer tracking natively — no JavaScript scroll event listeners needed.
- `Scroll Percent Y` (0 = top, 100 = bottom) is animatable and can be bound to a view model property for programmatic control.
- `Scroll Index` snaps to a specific item by 0-based index — useful for carousels and paginated lists.
- For large lists, enable **Virtualize** on the Artboard List inside the scroll content — only visible rows are rendered.
- **Carousel** (endless looping scroll): enable Virtualize + Carousel mode on the Artboard List.
- On web, ensure the canvas element captures pointer events and doesn't conflict with page scrolling (set `touch-action: none` on the canvas if needed).
```

- [ ] **Step 3: Commit**

```bash
git add rive-recipes/scroll-view-react.md
git commit -m "Add recipe: scroll view in React"
```

---

### Task 17: Recipe — audio-from-script.md

**Files:**
- Create: `rive-recipes/audio-from-script.md`

- [ ] **Step 1: Create `rive-recipes/audio-from-script.md`**

The Audio scripting API is documented in `rive-reference/02-state-machines-and-events.md` — no additional fetch needed.

```markdown
# Audio Triggered from Luau Script

**What this covers:** Playing audio programmatically from a Rive Luau script using the `Audio` global API, as an alternative to Audio Events on timelines or transitions.
**Rive features used:** Scripting (Node protocol), Audio API, Audio Events (imported assets).

## Editor setup

1. Import an audio file into the **Assets Panel** (drag in or use the + button). Rive accepts WAV, MP3, OGG.
2. Create a **Script** asset: Assets Panel → + → Script → Node protocol. Name it `SoundController`.
3. Attach the script to your artboard: right-click artboard → Add Script → `SoundController`.

## Script

```lua
-- SoundController.lua
return function(): Node<SoundController>
  local sound: AudioSource
  local isPlaying = false

  local function init(self, context): boolean
    -- Get a handle to the audio asset by name
    sound = context:audio("explosion")
    return sound ~= nil
  end

  local function advance(self, seconds): boolean
    return false -- no continuous work needed
  end

  -- Called by the runtime or another script to play the sound
  local function playSound(self)
    if sound and not isPlaying then
      local instance: AudioSound = sound:playOnce()
      instance.volume = 0.8
      isPlaying = false -- reset (playOnce fires and forgets)
    end
  end

  return { init = init, advance = advance, playSound = playSound }
end
```

> `context:audio("name")` gets an `AudioSource` for the asset named `"explosion"`.
> `AudioSource:playOnce()` returns an `AudioSound` instance with full playback control.

## Triggering from a Listener Action Script

```lua
-- TriggerOnClick.lua (Listener Action protocol)
return function(): ListenerAction<TriggerOnClick>
  local function perform(self, context)
    -- Trigger sound via the SoundController script
    local controller = context:node("SoundController")
    if controller then
      controller:playSound()
    end
  end

  return { perform = perform }
end
```

## AudioSound control

```lua
local s: AudioSound = sound:play()
s:pause()
s:resume()
s:stop()
s:seek(1.5)   -- jump to 1.5 seconds
s.volume = 0.5
```

## Notes

- `Audio:play*()` methods: `play()` (loops), `playOnce()` (fires once, auto-releases), `playFrom(seconds)`.
- Source docs: `scripting/api-reference/interfaces/audio-source` and `scripting/api-reference/interfaces/audio-sound`.
- **Audio Events** (non-scripting): add an Audio Event to a timeline keyframe or state machine transition — simpler for static sound cues that don't need code control.
- Audio playback requires browser user interaction to start (Web Audio API autoplay policy). Ensure the first audio call happens in response to a user gesture.
- Not all runtimes support all audio features — check `runtimes/feature-support.mdx` for your platform.
```

- [ ] **Step 2: Commit**

```bash
git add rive-recipes/audio-from-script.md
git commit -m "Add recipe: audio triggered from Luau script"
```

---

### Task 18: Recipe — custom-converter.md

**Files:**
- Create: `rive-recipes/custom-converter.md`

- [ ] **Step 1: Fetch converter script docs**

```
https://raw.githubusercontent.com/rive-app/rive-docs/main/scripting/protocols/converter-scripts.mdx
```

Verify the `Converter<T, InputType, OutputType>` protocol signature and creation steps.

- [ ] **Step 2: Create `rive-recipes/custom-converter.md`**

```markdown
# Custom Converter Script (number → formatted string)

**What this covers:** A Luau Converter script that transforms a number into a formatted display string (e.g. score `1500` → `"1,500 pts"`), used in a data binding.
**Rive features used:** Scripting (Converter protocol), data binding, view model.

## Editor setup

1. Create a **Script** asset: Assets Panel → + → Script → **Converter** protocol. Name it `ScoreFormatter`.
2. In the Data panel, create a View Model with a number property `score`.
3. Create a text object and bind its text run to `score` using the `ScoreFormatter` converter.

## Script

```lua
-- ScoreFormatter.lua
return function(): Converter<ScoreFormatter, number, string>
  local function init(self): boolean
    return true
  end

  local function convert(self, inputs): string
    local n = inputs[1] or 0
    -- Format with thousands separator
    local formatted = tostring(math.floor(n))
    local result = ""
    local count = 0
    for i = #formatted, 1, -1 do
      if count > 0 and count % 3 == 0 then
        result = "," .. result
      end
      result = formatted:sub(i, i) .. result
      count = count + 1
    end
    return result .. " pts"
  end

  -- reverseConvert is optional — only needed for bidirectional bindings
  local function reverseConvert(self, output): number
    local digits = output:gsub("[^%d]", "")
    return tonumber(digits) or 0
  end

  return { init = init, convert = convert, reverseConvert = reverseConvert }
end
```

## Usage in data binding

After creating the script asset:
1. Select the text run binding.
2. In the binding inspector, add the `ScoreFormatter` converter.
3. The converter automatically transforms the number before it reaches the text run.

## Notes

- The `inputs` table contains the bound property values. For a single-input converter, `inputs[1]` is the value.
- `reverseConvert` enables bidirectional bindings (e.g. a text input → number). Omit it if you only need source-to-target.
- Built-in converters (add, multiply, to-string) handle simple cases — use a script only for logic that built-ins can't express.
- Converter scripts run every frame when the bound value changes — keep `convert` fast (no allocations in tight loops).
- Source docs: `scripting/protocols/converter-scripts.mdx`
```

- [ ] **Step 3: Commit**

```bash
git add rive-recipes/custom-converter.md
git commit -m "Add recipe: custom converter script (number to formatted string)"
```

---

### Task 19: Recipe — custom-layout.md

**Files:**
- Create: `rive-recipes/custom-layout.md`

- [ ] **Step 1: Fetch layout script docs**

```
https://raw.githubusercontent.com/rive-app/rive-docs/main/scripting/protocols/layout-scripts.mdx
```

Verify the `Layout<T>` protocol — especially `measure`, `resize`, and available child APIs.

- [ ] **Step 2: Create `rive-recipes/custom-layout.md`**

```markdown
# Custom Layout Script (masonry grid)

**What this covers:** A Luau Layout script implementing a masonry-style grid — columns of equal width, items placed in the shortest column, variable row heights.
**Rive features used:** Scripting (Layout protocol), Layouts.

## Editor setup

1. Create a Layout object on your artboard to serve as the masonry container.
2. Set its scale type to **Hug** (height grows to fit content).
3. Create a **Script** asset: Assets Panel → + → Script → **Layout** protocol. Name it `MasonryLayout`.
4. Attach the script to the container layout: right-click layout → Add Script.
5. Add child items (Layouts or Components) inside the container — the script will position them.

## Script

```lua
-- MasonryLayout.lua
return function(): Layout<MasonryLayout>
  local columnCount = 3
  local gap = 8
  local containerWidth = 0

  local function init(self, context): boolean
    return true
  end

  local function resize(self, size: Vec2D)
    containerWidth = size.x
    local colWidth = (containerWidth - gap * (columnCount - 1)) / columnCount
    local colHeights: {number} = {}
    for i = 1, columnCount do colHeights[i] = 0 end

    for i, child in ipairs(self:children()) do
      -- Find shortest column
      local minCol = 1
      for c = 2, columnCount do
        if colHeights[c] < colHeights[minCol] then minCol = c end
      end
      local x = (minCol - 1) * (colWidth + gap)
      local y = colHeights[minCol]
      child:setPosition(Vec2D.new(x, y))
      child:setSize(Vec2D.new(colWidth, child:intrinsicHeight()))
      colHeights[minCol] = colHeights[minCol] + child:intrinsicHeight() + gap
    end
  end

  local function measure(self): Vec2D
    -- Return ideal size for Hug parent
    local colWidth = (containerWidth - gap * (columnCount - 1)) / columnCount
    local colHeights: {number} = {}
    for i = 1, columnCount do colHeights[i] = 0 end
    for _, child in ipairs(self:children()) do
      local minCol = 1
      for c = 2, columnCount do
        if colHeights[c] < colHeights[minCol] then minCol = c end
      end
      colHeights[minCol] = colHeights[minCol] + child:intrinsicHeight() + gap
    end
    local maxH = 0
    for _, h in ipairs(colHeights) do if h > maxH then maxH = h end end
    return Vec2D.new(containerWidth, maxH)
  end

  return { init = init, resize = resize, measure = measure }
end
```

> **API note:** `self:children()`, `child:setPosition()`, `child:setSize()`, `child:intrinsicHeight()` — verify these against `scripting/protocols/layout-scripts.mdx`. The child layout API surface may differ.

## Notes

- `resize(size)` is called whenever the container is resized — this is where placement logic runs.
- `measure()` is only called when the parent is Hug — return the ideal size.
- Layout scripts extend Node, inheriting `init`, `advance`, `draw`, and pointer callbacks.
- For a simpler custom layout, start with `advance` only (no `resize`) and animate positions directly.
- Source docs: `scripting/protocols/layout-scripts.mdx`
```

- [ ] **Step 3: Commit**

```bash
git add rive-recipes/custom-layout.md
git commit -m "Add recipe: custom layout script (masonry grid)"
```

---

### Task 20: Recipe — transition-condition-script.md

**Files:**
- Create: `rive-recipes/transition-condition-script.md`

- [ ] **Step 1: Fetch transition condition docs**

```
https://raw.githubusercontent.com/rive-app/rive-docs/main/scripting/protocols/transition-condition-scripts.mdx
```

Verify the `TransitionCondition<T>` protocol, `evaluate` signature, and how to attach to a transition.

- [ ] **Step 2: Create `rive-recipes/transition-condition-script.md`**

```markdown
# Custom Transition Condition Script

**What this covers:** A Luau Transition Condition script that controls when a state machine transition fires using custom logic — useful when built-in view model property conditions aren't expressive enough.
**Rive features used:** Scripting (TransitionCondition protocol), state machine transitions.

## When to use this

Use a Transition Condition script when:
- The condition combines multiple values with complex logic
- The condition uses external state not available as a view model property
- You need time-based or probabilistic transitions

For simple conditions (boolean equals, number greater-than), bind a view model property directly — no script needed.

## Editor setup

1. Create a **Script** asset: Assets Panel → + → Script → **Transition Condition** protocol. Name it `ComboReadyCondition`.
2. In the state machine, select the transition where the condition should apply.
3. In the transition inspector, add a condition → choose **Script** → select `ComboReadyCondition`.

## Script

```lua
-- ComboReadyCondition.lua
-- Fires when the player has pressed the button 3 times within 2 seconds

return function(): TransitionCondition<ComboReadyCondition>
  local pressCount: number = Script.Input<number>("pressCount", 0)
  local windowSeconds: number = Script.Input<number>("windowSeconds", 2.0)
  local lastResetTime = 0
  local elapsed = 0

  local function init(self, context): boolean
    return true
  end

  local function evaluate(self): boolean
    -- pressCount and windowSeconds are updated externally via Script Inputs
    -- Return true to allow the transition
    return pressCount:get() >= 3
  end

  return { init = init, evaluate = evaluate }
end
```

> `Script.Input<T>` declares a script input that can receive values from the Rive editor or from runtime code. Verify the `Script.Input` API against `scripting/script-inputs.mdx`.

## Notes

- `evaluate()` is called every frame while the transition is a candidate — keep it fast and side-effect free. Do not trigger sounds, update state, or call external APIs from `evaluate`.
- To pass values into the condition from the state machine: use `Script.Input<T>` for properties that come from the editor, or bind view model properties to Script Inputs.
- Multiple Transition Condition scripts on one transition create "AND" logic — all must return `true`.
- For "OR" logic, add multiple transitions between the same states.
- Source docs: `scripting/protocols/transition-condition-scripts.mdx`, `scripting/script-inputs.mdx`
```

- [ ] **Step 3: Commit**

```bash
git add rive-recipes/transition-condition-script.md
git commit -m "Add recipe: custom transition condition script"
```

---

### Task 21: Add recipe pointer to all tool context files

**Files:**
- Verify `CLAUDE.md` (already updated in Task 1)
- Verify `GEMINI.md` (already updated as copy of CLAUDE.md)
- Modify: `.cursor/rules/rive.mdc`
- Modify: `.windsurfrules`
- Modify: `.github/copilot-instructions.md`

The recipe note was added to CLAUDE.md in Task 1 and propagated to GEMINI.md in Task 6. Confirm the Cursor, Windsurf, and Copilot files have the recipe note (they should if they were copied from CLAUDE.md in Tasks 7–9). If any are missing it, add the `### Recipes` subsection.

- [ ] **Step 1: Verify recipe section in each file**

Read `.cursor/rules/rive.mdc`, `.windsurfrules`, `.github/copilot-instructions.md` and check that each contains:

```markdown
### Recipes

For common task patterns ("how do I build a scrolling list?", "how do I trigger audio from Luau?"), check `rive-recipes/` before answering. Each recipe is a complete, code-first worked example.
```

- [ ] **Step 2: Add missing sections if needed**

For any file missing the section, insert it after `### Curated reference files` and before `### Full source documentation`.

- [ ] **Step 3: Commit (only if changes were needed)**

```bash
git add .cursor/ .windsurfrules .github/copilot-instructions.md
git commit -m "Ensure recipe pointer is present in all tool context files"
```

---

## Phase 4: Maintenance Improvements

---

### Task 22: Add CHANGELOG.md

**Files:**
- Create: `CHANGELOG.md`

- [ ] **Step 1: Create `CHANGELOG.md`**

```markdown
# Changelog

All notable changes to rive-assistant are listed here. This file is updated when reference files or structural components change meaningfully.

Format: [Unreleased] at top, then dated entries in reverse chronological order.

---

## [Unreleased]

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
- GitHub Action for content drift detection (`sync-content-hashes.yml`)

### Changed
- `CLAUDE.md` — replaced 35-row routing table with directive to `00-concept-map.md`; added recipe library pointer; updated line count target to 150–300
- `rive-reference/00-concept-map.md` — added usage preamble; renamed "Source MDX" column for clarity
- `rive-reference/09-game-runtimes.md` — expanded Unity and Unreal sections with setup patterns and code examples
- All `rive-reference/*.md` — added "Last verified" date
- `README.md` — per-tool setup table; changelog link; updated what's included
- `CONTRIBUTING.md` — added template reference, recipe format, multi-tool sync note
```

- [ ] **Step 2: Commit**

```bash
git add CHANGELOG.md
git commit -m "Add CHANGELOG.md with initial entry"
```

---

### Task 23: Update CONTRIBUTING.md with all new sections

**Files:**
- Modify: `CONTRIBUTING.md`

- [ ] **Step 1: Add multi-tool sync note**

At the end of the `## Updating the routing table in CLAUDE.md` section, add:

```markdown
## Keeping tool context files in sync

When `CLAUDE.md` is updated with new content (deprecation notices, routing rules, vocabulary), apply the same change to all tool context files:
- `GEMINI.md` — identical to `CLAUDE.md`
- `.cursor/rules/rive.mdc` — same content, no URL fetch instructions, add YAML frontmatter
- `.windsurfrules` — same as Cursor file minus the frontmatter
- `.github/copilot-instructions.md` — identical to `.windsurfrules`

The four tool files share all content except the "Full source documentation" fetch instructions and the "If a fetch returns 404" section (omitted from non-fetching tools).
```

- [ ] **Step 2: Add recipe contribution section**

At the end of the file, add:

```markdown
## Adding recipes

Recipes live in `rive-recipes/`. Each recipe covers one common task pattern end-to-end.

When adding a recipe:
- Follow the format in any existing recipe file (problem → editor setup → runtime code → notes)
- Verify all API calls against current source docs before committing
- Default runtime code to JavaScript/TypeScript; note cross-platform differences inline
- Keep it under 100 lines — if it's growing larger, it's probably two recipes
- Update `CLAUDE.md` (and all tool files) if you add a new recipe category not covered by the existing pointer
```

- [ ] **Step 3: Commit**

```bash
git add CONTRIBUTING.md
git commit -m "Update CONTRIBUTING: multi-tool sync note, recipe contribution section"
```

---

### Task 24: GitHub Action — content hash monitoring

**Files:**
- Create: `.github/workflows/sync-content-hashes.yml`
- Create: `docs-content-hashes.txt` (initial snapshot)

- [ ] **Step 1: Create `.github/workflows/sync-content-hashes.yml`**

```yaml
name: Sync content hashes

on:
  schedule:
    - cron: '0 9 * * 1'  # Every Monday at 9am UTC
  workflow_dispatch:

jobs:
  check-content:
    runs-on: ubuntu-latest
    permissions:
      contents: write
      pull-requests: write
    steps:
      - uses: actions/checkout@11bd71901bbe5b1630ceea73d27597364c9af683  # v4.2.2

      - name: Fetch and hash critical docs pages
        run: |
          python3 - <<'EOF' > /tmp/hashes-latest.txt
          import hashlib
          import subprocess
          import sys

          BASE = "https://raw.githubusercontent.com/rive-app/rive-docs/main/"
          PAGES = sorted([
              "editor/data-binding/overview",
              "editor/data-binding/lists",
              "editor/layouts/overview",
              "editor/state-machine/listeners",
              "editor/state-machine/state-machine",
              "editor/state-machine/transitions",
              "getting-started/best-practices",
              "runtimes/android/android",
              "runtimes/apple/apple",
              "runtimes/flutter/flutter",
              "runtimes/react/react",
              "runtimes/web/web-js",
              "scripting/getting-started",
              "scripting/protocols/converter-scripts",
              "scripting/protocols/node-scripts",
          ])

          lines = []
          for page in PAGES:
              url = BASE + page + ".mdx"
              result = subprocess.run(
                  ["curl", "-sf", "--max-time", "30", url],
                  capture_output=True,
              )
              if result.returncode != 0:
                  print(f"WARNING: Failed to fetch {url}", file=sys.stderr)
                  continue
              h = hashlib.sha256(result.stdout).hexdigest()
              lines.append(f"{h}  {page}")

          print("\n".join(lines))
          EOF

      - name: Compare with stored hashes
        id: compare
        run: |
          if diff docs-content-hashes.txt /tmp/hashes-latest.txt > /tmp/hashes-diff.txt 2>&1; then
            echo "changed=false" >> $GITHUB_OUTPUT
            echo "No content changes detected."
          else
            echo "changed=true" >> $GITHUB_OUTPUT
            echo "Content changes detected:"
            cat /tmp/hashes-diff.txt
          fi

      - name: Update stored hashes file
        if: steps.compare.outputs.changed == 'true'
        run: cp /tmp/hashes-latest.txt docs-content-hashes.txt

      - name: Build list of changed pages
        if: steps.compare.outputs.changed == 'true'
        id: changes
        run: |
          CHANGED=$(grep '^[<>]' /tmp/hashes-diff.txt | awk '{print $3}' | sort -u | sed 's/^/- /')
          echo "pages<<EOF" >> $GITHUB_OUTPUT
          echo "$CHANGED" >> $GITHUB_OUTPUT
          echo "EOF" >> $GITHUB_OUTPUT

      - name: Open PR
        if: steps.compare.outputs.changed == 'true'
        uses: peter-evans/create-pull-request@5e914681df9dc83aa4e4905692ca88beb2f9e91f  # v7.0.5
        with:
          token: ${{ secrets.GITHUB_TOKEN }}
          branch: sync/content-hashes
          base: main
          commit-message: "Update docs-content-hashes.txt"
          title: "Rive docs content changed — review reference files"
          body: |
            The content of one or more monitored Rive documentation pages has changed. Review the curated reference files that cover these pages and update them if needed.

            **Changed pages:**
            ${{ steps.changes.outputs.pages }}

            To find which reference file covers a changed page, look it up in `rive-reference/00-concept-map.md`.
```

- [ ] **Step 2: Generate the initial `docs-content-hashes.txt`**

Run the hash script locally to generate the initial snapshot. From the repo root:

```bash
python3 - <<'EOF' > docs-content-hashes.txt
import hashlib
import subprocess

BASE = "https://raw.githubusercontent.com/rive-app/rive-docs/main/"
PAGES = sorted([
    "editor/data-binding/overview",
    "editor/data-binding/lists",
    "editor/layouts/overview",
    "editor/state-machine/listeners",
    "editor/state-machine/state-machine",
    "editor/state-machine/transitions",
    "getting-started/best-practices",
    "runtimes/android/android",
    "runtimes/apple/apple",
    "runtimes/flutter/flutter",
    "runtimes/react/react",
    "runtimes/web/web-js",
    "scripting/getting-started",
    "scripting/protocols/converter-scripts",
    "scripting/protocols/node-scripts",
])

lines = []
for page in PAGES:
    url = BASE + page + ".mdx"
    result = subprocess.run(["curl", "-sf", "--max-time", "30", url], capture_output=True)
    if result.returncode != 0:
        print(f"WARNING: Failed to fetch {url}")
        continue
    h = hashlib.sha256(result.stdout).hexdigest()
    lines.append(f"{h}  {page}")

print("\n".join(lines))
EOF
```

- [ ] **Step 3: Verify `docs-content-hashes.txt`**

Read `docs-content-hashes.txt` and confirm:
- It has 15 lines (one per page)
- Each line follows the format `<64-char hex hash>  <path>`
- Lines are sorted alphabetically by path

- [ ] **Step 4: Commit both files**

```bash
git add .github/workflows/sync-content-hashes.yml docs-content-hashes.txt
git commit -m "Add content hash monitoring workflow and initial hash snapshot"
```

---

## Self-Review

### Spec coverage check

| Spec section | Covered by |
|---|---|
| 1a. Eliminate routing table duplication | Tasks 1, 2 |
| 1b. Releases and changelog | Task 22 |
| 2. Multi-tool support (GEMINI.md) | Task 6 |
| 2. Multi-tool support (Cursor) | Task 7 |
| 2. Multi-tool support (Windsurf) | Task 8 |
| 2. Multi-tool support (Copilot) | Task 9 |
| 2. README per-tool setup | Task 10 |
| 2. CONTRIBUTING multi-tool sync | Task 23 |
| 3. Recipe library (10 recipes) | Tasks 11–20 |
| 3. CLAUDE.md recipe pointer | Task 1 |
| 3. Tool files recipe pointer | Task 21 |
| 3. CONTRIBUTING recipe format | Task 23 |
| 4a. Reference file template | Task 4 |
| 4b. Expand game runtimes | Task 5 |
| 4c. Last verified metadata | Task 3 |
| 5. Content hash monitoring workflow | Task 24 |

All spec sections are covered. One spec item not reflected above: "Update CLAUDE.md's stated length target to 150–300" — this is included in Task 1's CLAUDE.md edit (the reference files section says "150–300 lines each").

### Placeholder scan

Tasks 5, 13, 15, 16, 18, 19, 20 include "fetch source docs first" steps. These are deliberate and valid — the plan's job for content tasks is to specify what to fetch, not to hallucinate API signatures. The fetch step + content step together are complete instructions.

Tasks 7–9 say "copy content from CLAUDE.md with these specific modifications." Not a placeholder — the modifications are fully specified.

### Type consistency

No code-level types across tasks. Recipe API calls use consistent patterns (`vm.boolean()`, `vm.string()`, `vm.trigger().fire()`, `vm.list()`) throughout Tasks 11–20. The note "verify against `runtimes/data-binding.mdx`" appears wherever runtime API calls are made.
