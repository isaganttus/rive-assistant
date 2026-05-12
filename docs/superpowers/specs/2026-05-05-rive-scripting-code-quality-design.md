# Rive Scripting Code Quality Design

## Goal

Improve the assistant's Rive Luau scripting output by correcting stale API guidance in the focused scripting reference surfaces. The update uses a local Rive scripting reference pack as the source for API names, protocol shapes, and examples.

## Scope

This is a focused scripting-code-quality update only. It touches scripting reference material, scripting recipes, and eval criteria that directly influence generated Luau code.

In scope:

- `rive-reference/05-scripting.md`
- Existing scripting recipes that show stale or incorrect Luau patterns
- Eval cases that should prevent the same bad patterns from returning

Out of scope:

- Folding the broader generated Rive skill into the general assistant prompt
- Reworking non-scripting Rive concepts
- Runtime integration docs except where they directly cite scripting behavior

## Problems To Fix

Current guidance mixes newer and older scripting API shapes. The most important issues found during exploration:

- `Vec2D` appears in reference and recipes, while the source pack defines `Vector` and `Vector.xy(...)`.
- The transition condition recipe uses `vm:number("pressCount")` and `:get()`, while the source pack defines `vm:getNumber("pressCount")` and property `.value`.
- Listener action guidance still centers on `perform(self, pointerEvent)`, while the source pack marks `perform` deprecated and prefers `performAction(self, listenerContext)`.
- Converter examples use generic `DataInputs` / `DataOutput` in ways that are less precise than the source pack's typed `Converter<T, I, O>` pattern with `DataValueNumber`, `DataValueString`, and related types.
- The scripting reference lacks a compact code-generation checklist that forces exact protocol, constructor, property, and side-effect rules before producing code.

## Approach

Use the existing reference and recipe structure rather than adding a parallel guide. The assistant already checks `rive-reference/` and `rive-recipes/`; improving those files keeps the training path simple and reduces drift.

The implementation should:

- Treat the external source pack as authoritative when it conflicts with current scripting examples.
- Replace stale symbols with exact API names:
  - `Vec2D` -> `Vector`
  - `Vec2D.xy(...)` -> `Vector.xy(...)`
  - `vm:number(...)` -> `vm:getNumber(...)`
  - property reads via `.value`, not `:get()`
  - listener actions via `performAction(self, listenerContext)`
- Keep converter and transition condition examples side-effect free.
- Nil-check context and view model property access before reading values.
- Prefer typed converter signatures when the converter's input and output types are known.
- Add a "before writing Luau code" checklist to `rive-reference/05-scripting.md`.

## File Changes

Expected edits:

- `rive-reference/05-scripting.md`: update protocol summaries, math naming, context/view model examples, pointer event naming, and add the code-generation checklist.
- `rive-recipes/custom-converter.md`: use typed `DataValueNumber` and `DataValueString` converter signatures and keep type checks only where they are needed for defensive examples.
- `rive-recipes/transition-condition-script.md`: use `getNumber(...).value`, remove unsupported `context = late()` injection advice for protocol context, and keep `evaluate` pure.
- `rive-recipes/custom-layout.md`: replace `Vec2D` naming with `Vector` and mark any uncertain child-layout APIs as source-verification notes rather than asserted facts.
- Any listener-action recipe or reference mentions found during implementation: prefer `performAction` and `ListenerContext`.
- Relevant eval JSON files: add red flags for `Vec2D`, `vm:number`, `:get()` property reads, deprecated `perform`, and vague converter types where exact types are known.

## Testing And Verification

Run the repo's validation tests after editing:

- `pytest`
- If the full suite is too broad or blocked, run the targeted validation tests under `tests/test_validate_answer_evals.py`, `tests/test_validate_reference_metadata.py`, and recipe/doc tests affected by the changes.

Manual verification:

- Search the changed scripting surfaces for stale tokens: `Vec2D`, `vm:number`, `perform(self`, `DataInputs`, `DataOutput`, and `:get()`.
- Confirm any remaining occurrence is intentionally documented as legacy/deprecated or a source-path reference.
- Compare corrected examples against the external source pack files in `reference/ref_rive_interfaces`, `reference/ref_rive_base`, `reference/ref_rive_dataValue`, `reference/ref_rive_vec2d`, and related API files.

## Risks

The external folder is a scripting source pack, not the full Rive docs mirror. If an API is missing from that pack, the implementation should avoid overclaiming and keep a source-verification note rather than inventing a method signature.

Some current recipes may rely on speculative layout child APIs. Those should be tightened or caveated instead of expanded.
