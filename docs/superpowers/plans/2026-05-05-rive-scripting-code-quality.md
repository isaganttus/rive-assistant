# Rive Scripting Code Quality Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Correct the assistant's Rive Luau scripting guidance so generated scripts use current protocol signatures, exact API names, and safer data-binding patterns.

**Architecture:** Update the existing assistant knowledge surfaces in place: the curated scripting reference, the scripting recipes, and eval cases. Add a narrow regression test that fails when stale scripting tokens return to those surfaces.

**Tech Stack:** Markdown reference docs, JSON eval cases, Python `unittest`/`pytest`, Rive Luau scripting source pack at `/Users/isadoradias/Documents/Archive/Working/Code/Rive Scripting/Rive Docs/reference`.

---

## File Structure

- Create `tests/test_scripting_code_quality_docs.py`: regression test for stale Luau scripting patterns in the assistant-facing docs and recipes.
- Modify `rive-reference/05-scripting.md`: authoritative scripting guidance for protocols, data binding, listener actions, vectors, pointer events, and the pre-code checklist.
- Modify `rive-recipes/custom-converter.md`: typed `Converter<T, DataValueNumber, DataValueString>` example.
- Modify `rive-recipes/transition-condition-script.md`: `Context` injection through `init`, `vm:getNumber(...)`, and property `.value`.
- Modify `rive-recipes/custom-layout.md`: accurate `Vector` naming and a supported layout lifecycle example without speculative child APIs.
- Modify `rive-recipes/audio-from-script.md`: `Audio` global playback and `performAction(self, listenerContext)` for listener actions.
- Modify `evals/cases/custom-converter-script.json`: stronger converter red flags.
- Modify `evals/cases/audio-from-luau-script.json`: stronger audio/listener-action red flags.
- Create `evals/cases/transition-condition-script.json`: eval coverage for the transition condition recipe.

---

### Task 1: Add A Failing Regression Test For Stale Scripting Patterns

**Files:**
- Create: `tests/test_scripting_code_quality_docs.py`

- [ ] **Step 1: Add the regression test**

Use `apply_patch` to create `tests/test_scripting_code_quality_docs.py` with this exact content:

```python
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCRIPTING_SURFACES = [
    "rive-reference/05-scripting.md",
    "rive-recipes/custom-converter.md",
    "rive-recipes/transition-condition-script.md",
    "rive-recipes/custom-layout.md",
    "rive-recipes/audio-from-script.md",
]

STALE_PATTERNS = {
    "Vec2D": "Use `Vector` and `Vector.xy(...)` in Rive Luau scripts.",
    "vm:number(": "Use `vm:getNumber(...)` and read the returned property's `.value`.",
    ":get()": "Read Rive ViewModel properties through `.value`.",
    "perform(self": "Use `performAction(self, listenerContext)` for ListenerAction scripts.",
    "context = late()": "Protocol context is passed to `init`; do not invent a `context` field.",
    "DataInputs": "Use exact DataValue input types when the converter type is known.",
    "DataOutput": "Use exact DataValue output types when the converter type is known.",
}


class ScriptingCodeQualityDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_scripting_surfaces_do_not_use_stale_luau_api_shapes(self):
        for relative_path in SCRIPTING_SURFACES:
            content = self.read(relative_path)
            for stale, guidance in STALE_PATTERNS.items():
                with self.subTest(path=relative_path, stale=stale):
                    self.assertNotIn(stale, content, guidance)

    def test_scripting_surfaces_teach_current_replacements(self):
        reference = self.read("rive-reference/05-scripting.md")
        self.assertIn("Before writing Luau code", reference)
        self.assertIn("Vector.xy", reference)
        self.assertIn("vm:getNumber", reference)
        self.assertIn("performAction", reference)

        converter = self.read("rive-recipes/custom-converter.md")
        self.assertIn("Converter<ScoreFormatter, DataValueNumber, DataValueString>", converter)

        transition = self.read("rive-recipes/transition-condition-script.md")
        self.assertIn("pressCount.value", transition)

        audio = self.read("rive-recipes/audio-from-script.md")
        self.assertIn("Audio.play", audio)
        self.assertIn("ListenerContext", audio)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the new test and verify it fails against the current docs**

Run:

```bash
pytest tests/test_scripting_code_quality_docs.py -q
```

Expected result: failure showing stale patterns in the current scripting reference and recipes, including `Vec2D`, `vm:number(`, `perform(self`, `DataInputs`, or `DataOutput`.

- [ ] **Step 3: Commit the failing test**

Run:

```bash
git add tests/test_scripting_code_quality_docs.py
git commit -m "test: add Rive scripting code quality checks"
```

---

### Task 2: Update The Main Scripting Reference

**Files:**
- Modify: `rive-reference/05-scripting.md`
- Test: `tests/test_scripting_code_quality_docs.py`

- [ ] **Step 1: Replace stale protocol and API guidance**

Use the source pack files `ref_rive_interfaces`, `ref_rive_base`, `ref_rive_dataValue`, `ref_rive_vec2d`, `ref_rive_mat2d`, `ref_rive_path`, `ref_rive_renderer`, and `ref_rive_artboards` as the authority.

Edit `rive-reference/05-scripting.md` so these sections contain the following facts:

```markdown
### Layout Scripts
**Purpose**: Custom layout measurement and resize behavior.

Extends Node (inherits all lifecycle). Additional:
- `measure(self) -> Vector`: Returns ideal size when the parent uses Hug sizing (optional)
- `resize(self, size: Vector)`: Required; called when layout receives a size

### Converter Scripts
**Purpose**: Transform data between view model and bound properties.

- `init(self, context) -> bool`: Optional setup
- `convert(self, input: InputType) -> OutputType`: Input to output (required)
- `reverseConvert(self, input: OutputType) -> InputType`: Output to input for 2-way binding
- `advance(self, seconds) -> bool`: Optional time-based converter updates

Factory: `Converter<MyConverter, DataValueNumber, DataValueString>` (choose exact `DataValue*` types for the binding).

### Listener Action Scripts
**Purpose**: Run side effects when state machine listeners fire.

- `init(self, context) -> bool`: Optional setup
- `performAction(self, listenerContext)`: Preferred listener callback
- `perform(self, pointerEvent)`: Deprecated; mention only when explaining legacy files

Use `ListenerContext` methods such as `isPointerEvent()` and `asPointerEvent()` to inspect what triggered the listener.
```

Update the Data Binding from Scripts section so the view model access examples use this exact shape:

```markdown
**Reading/writing view model properties**:
- `vmi:getNumber('propName')`, `getString`, `getBoolean`, `getColor`, `getList`, `getViewModel`, `getEnum`
- Read/write scalar properties through `.value`: `health.value = health.value - 1`
- Triggers: `getTrigger()` then `:fire()`
- Listeners: `property:addListener(callback)`; store the view model or use the anchor overload so listeners are not garbage collected
```

Update the Pointer Events and Drawing Essentials sections so they use:

```markdown
- `position: Vector` — local coordinates relative to the script

local localEvent = PointerEvent.new(event.id, Vector.xy(event.position.x - offset.x, event.position.y - offset.y))

**Vector**: `Vector.xy(x, y)` and `Vector.origin()`; fields: `x`, `y`
```

- [ ] **Step 2: Add the Luau code-generation checklist**

Add this section before `## Debugging`:

```markdown
## Before writing Luau code

1. Identify the protocol first: `Node`, `Layout`, `Converter`, `PathEffect`, `TransitionCondition`, `ListenerAction`, `Test`, or Util.
2. Use the protocol's exact lifecycle names and signatures. Protocol context is passed to `init(self, context)`; do not add `context = late()` to returned protocol tables.
3. Use exact source-pack type names: `Vector`, `Mat2D`, `Path`, `Paint`, `Renderer`, `DataValueNumber`, `DataValueString`, `ListenerContext`.
4. Use `Vector.xy(...)`, not legacy or invented vector constructors.
5. Access ViewModel properties with `vm:getNumber(...)`, `vm:getString(...)`, and the other `get*` methods. Nil-check the returned property before reading or writing `.value`.
6. Keep `convert` and `evaluate` side-effect free. Listener actions and Node scripts are the right place for side effects such as audio playback.
7. Use `performAction(self, listenerContext)` for new ListenerAction scripts. Only mention `perform(self, pointerEvent)` when explaining deprecated code.
8. Remove listeners when a script owns their lifecycle, or keep the listened ViewModel anchored on `self`.
9. If a method is not in the curated reference or source pack, do not invent it. State what must be verified in source docs instead.
```

- [ ] **Step 3: Run the targeted regression test**

Run:

```bash
pytest tests/test_scripting_code_quality_docs.py -q
```

Expected result: still failing because recipes and eval-facing examples have not been corrected yet.

- [ ] **Step 4: Commit the reference update**

Run:

```bash
git add rive-reference/05-scripting.md
git commit -m "docs: correct Rive scripting reference APIs"
```

---

### Task 3: Update Scripting Recipes

**Files:**
- Modify: `rive-recipes/custom-converter.md`
- Modify: `rive-recipes/transition-condition-script.md`
- Modify: `rive-recipes/custom-layout.md`
- Modify: `rive-recipes/audio-from-script.md`
- Test: `tests/test_scripting_code_quality_docs.py`

- [ ] **Step 1: Replace the converter script with typed DataValue signatures**

In `rive-recipes/custom-converter.md`, replace the code block with:

```lua
-- ScoreFormatter.lua
type ScoreFormatter = {}

local function commaFormat(n: number): string
  local sign = ""
  if n < 0 then
    sign = "-"
    n = math.abs(n)
  end

  local s = tostring(math.floor(n))
  local result = ""
  local count = 0

  for i = #s, 1, -1 do
    if count > 0 and count % 3 == 0 then
      result = "," .. result
    end
    result = s:sub(i, i) .. result
    count += 1
  end

  return sign .. result
end

function init(self: ScoreFormatter, context: Context): boolean
  return true
end

function convert(self: ScoreFormatter, input: DataValueNumber): DataValueString
  local output = DataValue.string()
  output.value = commaFormat(input.value) .. " pts"
  return output
end

function reverseConvert(self: ScoreFormatter, input: DataValueString): DataValueNumber
  local output = DataValue.number()
  local digits = input.value:gsub("[^%d%-]", "")
  output.value = tonumber(digits) or 0
  return output
end

return function(): Converter<ScoreFormatter, DataValueNumber, DataValueString>
  return {
    init = init,
    convert = convert,
    reverseConvert = reverseConvert,
  }
end
```

Update the notes to say:

```markdown
- The converter type declares its exact input and output: `Converter<ScoreFormatter, DataValueNumber, DataValueString>`.
- `DataValue.number()` and `DataValue.string()` construct new typed values.
- `reverseConvert` enables bidirectional bindings. Omit it only for source-to-target bindings.
- Keep `convert` and `reverseConvert` side-effect free; they should not mutate view models, play audio, or call external services.
```

- [ ] **Step 2: Replace the transition condition script with `getNumber(...).value`**

In `rive-recipes/transition-condition-script.md`, replace the code block with:

```lua
-- ComboReadyCondition.lua
type ComboReadyCondition = {
  vm: ViewModel?,
}

function init(self: ComboReadyCondition, context: Context): boolean
  self.vm = context:viewModel()
  return self.vm ~= nil
end

function evaluate(self: ComboReadyCondition): boolean
  local vm = self.vm
  if vm == nil then
    return false
  end

  local pressCount = vm:getNumber("pressCount")
  if pressCount == nil then
    return false
  end

  return pressCount.value >= 3
end

return function(): TransitionCondition<ComboReadyCondition>
  return {
    init = init,
    evaluate = evaluate,
    vm = nil,
  }
end
```

Replace the API note with:

```markdown
> **API note:** Rive passes `Context` to `init(self, context)`. Store values you need later on `self`; do not add a synthetic `context = late()` field to the returned protocol table. ViewModel scalar properties are read through `vm:getNumber("name")` and `.value`.
```

- [ ] **Step 3: Replace the custom layout recipe with supported layout lifecycle code**

In `rive-recipes/custom-layout.md`, change the title to:

```markdown
# Custom Layout Script (measured panel)
```

Replace the script block with:

```lua
-- MeasuredPanel.lua
type MeasuredPanel = {
  minWidth: Input<number>,
  minHeight: Input<number>,
  currentSize: Vector,
}

function init(self: MeasuredPanel, context: Context): boolean
  return true
end

function resize(self: MeasuredPanel, size: Vector)
  self.currentSize = size
end

function measure(self: MeasuredPanel): Vector
  return Vector.xy(self.minWidth, self.minHeight)
end

return function(): Layout<MeasuredPanel>
  return {
    minWidth = 240,
    minHeight = 160,
    currentSize = Vector.origin(),
    init = init,
    resize = resize,
    measure = measure,
  }
end
```

Replace the API note with:

```markdown
> **API note:** The source pack defines layout sizing with `Vector`, `resize(self, size: Vector)`, and optional `measure(self): Vector`. Do not use child traversal or mutation methods unless you have verified those exact APIs in the current source docs.
```

- [ ] **Step 4: Replace the audio recipe with `Audio.play` and `performAction`**

In `rive-recipes/audio-from-script.md`, replace the Node script block with:

```lua
-- SoundController.lua
type SoundController = {
  source: AudioSource?,
  active: AudioSound?,
}

function init(self: SoundController, context: Context): boolean
  self.source = context:audio("explosion")
  return self.source ~= nil
end

function playOnce(self: SoundController)
  local source = self.source
  if source == nil then
    return
  end

  local sound = Audio.play(source)
  if sound ~= nil then
    sound.volume = 0.8
    self.active = sound
  end
end

return function(): Node<SoundController>
  return {
    source = nil,
    active = nil,
    init = init,
    playOnce = playOnce,
  }
end
```

Replace the Listener Action script block with:

```lua
-- TriggerOnClick.lua
type TriggerOnClick = {
  source: AudioSource?,
}

function init(self: TriggerOnClick, context: Context): boolean
  self.source = context:audio("explosion")
  return self.source ~= nil
end

function performAction(self: TriggerOnClick, listenerContext: ListenerContext)
  local pointer = listenerContext:asPointerEvent()
  if pointer ~= nil then
    pointer:hit()
  end

  local source = self.source
  if source == nil then
    return
  end

  local sound = Audio.play(source)
  if sound ~= nil then
    sound.volume = 0.8
  end
end

return function(): ListenerAction<TriggerOnClick>
  return {
    source = nil,
    init = init,
    performAction = performAction,
  }
end
```

Replace the play-method notes with:

```markdown
- `context:audio("name")` returns an `AudioSource?`; the name must match the asset in the Assets Panel exactly.
- `Audio.play(source)` and the other `Audio.play*` functions return an `AudioSound?`.
- `AudioSound` supports `pause()`, `resume()`, `stop(fadeToStopTime?)`, `seek(seconds)`, `seekFrame(frame)`, `time()`, `timeFrame()`, `completed()`, and writable `volume`.
- Use `performAction(self, listenerContext)` for new Listener Action scripts.
```

- [ ] **Step 5: Run the targeted regression test**

Run:

```bash
pytest tests/test_scripting_code_quality_docs.py -q
```

Expected result: pass.

- [ ] **Step 6: Commit the recipe updates**

Run:

```bash
git add rive-recipes/custom-converter.md rive-recipes/transition-condition-script.md rive-recipes/custom-layout.md rive-recipes/audio-from-script.md
git commit -m "docs: fix Rive Luau scripting recipes"
```

---

### Task 4: Update Eval Coverage

**Files:**
- Modify: `evals/cases/custom-converter-script.json`
- Modify: `evals/cases/audio-from-luau-script.json`
- Create: `evals/cases/transition-condition-script.json`
- Test: `tests/test_validate_answer_evals.py`

- [ ] **Step 1: Strengthen the custom converter eval**

Edit `evals/cases/custom-converter-script.json` so `required_concepts` includes these strings:

```json
"Use exact DataValue input and output types when the binding types are known",
"Return `Converter<ScoreFormatter, DataValueNumber, DataValueString>` for the shown number-to-string example"
```

Edit `red_flags` so it includes these strings:

```json
"Uses generic `DataInputs` or `DataOutput` in the production example when exact DataValue types are known",
"Mutates ViewModel properties, plays audio, or performs other side effects inside `convert`"
```

- [ ] **Step 2: Strengthen the audio eval**

Edit `evals/cases/audio-from-luau-script.json` so `required_concepts` includes these strings:

```json
"Use `Audio.play(source)` or another `Audio.play*` global function for scripted playback",
"Use `performAction(self, listenerContext)` for new Listener Action scripts"
```

Edit `red_flags` so it includes these strings:

```json
"Calls unsupported `AudioSource:play()` or `AudioSource:playOnce()` methods instead of the `Audio` global",
"Uses deprecated `perform(self, pointerEvent)` for a new Listener Action example"
```

- [ ] **Step 3: Add transition condition eval coverage**

Create `evals/cases/transition-condition-script.json` with this exact content:

```json
{
  "id": "transition-condition-script",
  "question": "Write a Rive transition condition script that allows a transition once a ViewModel number reaches 3.",
  "tags": ["scripting", "state-machines", "data-binding", "transition-conditions"],
  "expected_reference_files": [
    "rive-reference/02-state-machines-and-events.md",
    "rive-reference/03-data-binding.md",
    "rive-reference/05-scripting.md",
    "rive-recipes/transition-condition-script.md"
  ],
  "expected_source_paths": [
    "scripting/protocols/transition-condition-scripts.mdx",
    "scripting/data-binding.mdx",
    "scripting/api-reference/interfaces/view-model.mdx",
    "scripting/api-reference/data-value/property.mdx"
  ],
  "required_concepts": [
    "Use the TransitionCondition protocol for custom transition logic",
    "Store context-derived ViewModel references on `self` during `init(self, context)`",
    "Read ViewModel number properties with `vm:getNumber(\"name\")` and `.value`",
    "Keep `evaluate` fast and side-effect free"
  ],
  "red_flags": [
    "Uses `vm:number(\"name\")` or property `:get()` instead of `getNumber` and `.value`",
    "Adds `context = late()` to the returned protocol table",
    "Plays audio, mutates ViewModel data, or performs external side effects from `evaluate`",
    "Omits nil checks for the ViewModel or number property"
  ],
  "ideal_answer_shape": [
    "Briefly explain when a transition condition script is warranted",
    "Show a concise Luau `TransitionCondition` script",
    "Call out the editor setup and side-effect-free `evaluate` rule"
  ]
}
```

- [ ] **Step 4: Run eval validation**

Run:

```bash
pytest tests/test_validate_answer_evals.py -q
```

Expected result: pass.

- [ ] **Step 5: Commit eval updates**

Run:

```bash
git add evals/cases/custom-converter-script.json evals/cases/audio-from-luau-script.json evals/cases/transition-condition-script.json
git commit -m "evals: cover current Rive scripting APIs"
```

---

### Task 5: Run Full Verification

**Files:**
- No file edits expected unless a validation failure identifies a concrete issue in a file changed by this plan.

- [ ] **Step 1: Run stale-token audit**

Run:

```bash
rg -n "Vec2D|vm:number\\(|perform\\(self|context = late\\(\\)|DataInputs|DataOutput|:get\\(\\)" rive-reference/05-scripting.md rive-recipes/custom-converter.md rive-recipes/transition-condition-script.md rive-recipes/custom-layout.md rive-recipes/audio-from-script.md
```

Expected result: no matches and exit code `1`.

- [ ] **Step 2: Run reference metadata validation**

Run:

```bash
pytest tests/test_validate_reference_metadata.py -q
```

Expected result: pass.

- [ ] **Step 3: Run doc path validation**

Run:

```bash
pytest tests/test_validate_doc_paths.py -q
```

Expected result: pass.

- [ ] **Step 4: Run all tests**

Run:

```bash
pytest -q
```

Expected result: pass.

- [ ] **Step 5: Check git status**

Run:

```bash
git status --short
```

Expected result: clean working tree after the commits above, or only intentional files if the user chose not to commit during execution.

---

## Self-Review Notes

- Spec coverage: the plan updates the scripting reference, converter recipe, transition recipe, layout recipe, audio/listener action recipe, eval coverage, and verification commands called out in the approved design.
- Placeholder scan: no incomplete implementation markers are used.
- Type consistency: all replacement examples use `Vector`, `Context`, `ViewModel`, `DataValueNumber`, `DataValueString`, `ListenerContext`, `AudioSource`, `AudioSound`, and the protocol names from the source pack.
