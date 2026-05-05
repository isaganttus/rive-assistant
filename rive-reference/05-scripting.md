# Rive Scripting Reference
> Last verified: 2026-04-23
> Source docs: `scripting/`

## Overview

Rive Scripting uses **Luau** (Roblox's typed Lua variant) with type annotations. Scripts are assets saved in the Assets Panel. Naming convention: PascalCase matching the main type name.

## Creating Scripts

Two methods:
1. **Assets Panel**: + button > Script > choose protocol type
2. **Script Tool**: Click on artboard to create and attach in one step

**Adding to scene**: Right-click artboard > Add Script. Position in hierarchy determines render order for Node scripts.

## Editor Configuration

Access via Ctrl/Cmd + comma:
- `config.theme`: Set via `require('theme/<name>')`
- `config.code.fontSize`: 8-20 (default 12)
- `config.code.lineHeight`: default 18
- `config.code.executionTimeoutMs`: max 2000ms

## Protocols

All scripts follow a factory pattern returning a typed table:

```lua
return function(): Protocol<MyType>
  return { init = init, draw = draw, ... }
end
```

### Node Scripts
**Purpose**: Render custom graphics, handle simulation and interaction.

Lifecycle:
- `init(self, context) -> bool`: Called once at startup
- `advance(self, seconds) -> bool`: Called every frame for updates (optional)
- `update(self)`: Fires when any input changes (optional)
- `draw(self, renderer)`: Called every frame to render (optional)

Pointer callbacks: `pointerDown`, `pointerMove`, `pointerUp`, `pointerExit`

Must implement at least `init` and `draw`.

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

Created via Data Panel > Converters > Script.

### Path Effect Scripts
**Purpose**: Modify path geometry in real-time (warping, distortion).

- `init(self, context) -> bool`: Optional setup
- `update(self, inPath: PathData) -> PathData`: Required; transforms path
- `advance(self, seconds) -> bool`: Optional for animated effects

Applied to strokes via Options menu > Effects.

### Transition Condition Scripts
**Purpose**: Custom state machine transition logic.

- `init(self, context) -> bool`: Setup
- `evaluate(self) -> bool`: Every frame while active; must be fast, side-effect free

### Listener Action Scripts
**Purpose**: Run side effects when state machine listeners fire.

- `init(self, context) -> bool`: Optional setup
- `performAction(self, listenerContext)`: Preferred listener callback
- `perform(self, pointerEvent)`: Deprecated; mention only when explaining legacy files

Use `ListenerContext` methods such as `isPointerEvent()` and `asPointerEvent()` to inspect what triggered the listener.

### Test Scripts
**Purpose**: Unit test Util Scripts.

Single export: `setup(test: Tester)`.
- `test.case(name, fn)`: Single test
- `test.group(name, fn)`: Organize tests (nestable)
- `expect(value)`: Assertion with `.is()`, `.greaterThan()`, `.lessThan()`, `.never`

Run via: Right-click test > Run Tests.

### Util Scripts
**Purpose**: Reusable helper modules.

Export pattern: `return { functionName = function, ... }`
Import: `local MyUtil = require("MyUtil")`
Custom types: `export type` to share types with parent scripts.

## Script Inputs

Define inputs with `Input<T>` wrapper in the type definition:

```lua
type MyNode = {
  myNumber: Input<number>,
  myColor: Input<Color>,
  myViewModel: Input<Data.PointsVM>,
  myArtboard: Input<Artboard<Data.Enemy>>,
  myString: string,  -- Not an input (no wrapper)
}
```

**Default values in factory**:
- Static: `myNumber = 0`
- Runtime binding: `myViewModel = late()` (bound in editor)
- Non-input fields: set normally

**Input types**: `number`, `string`, `boolean`, `Color`, `Data.ViewModelName`, `Artboard<Data.ViewModelName>`

**Listening to changes**:
```lua
self.myNumber:addListener(function(value) print("Changed to", value) end)
```

The generic `update(self)` fires when any input changes.

## Data Binding from Scripts

Three access methods:

1. **Context** (most common):
   - `context:viewModel()` — node's immediate view model
   - `context:rootViewModel()` — root artboard view model
   - `context:dataContext()` — parent data context

2. **Script Inputs**: `character: Input<Data.Character>`

3. **Data Binding Inputs**: Bind property values directly

**Reading/writing view model properties**:
- `vmi:getNumber('propName')`, `getString`, `getBoolean`, `getColor`, `getList`, `getViewModel`, `getEnum`
- Read/write scalar properties through `.value`: `health.value = health.value - 1`
- Triggers: `getTrigger()` then `:fire()`
- Listeners: `property:addListener(callback)`; store the view model or use the anchor overload so listeners are not garbage collected

**Context utility methods**:
- `context:image(name)` — get image asset
- `context:blob(name)` — get raw binary data
- `context:audio(name)` — get audio source
- `context:markNeedsUpdate()` — re-trigger update function

## Pointer Events

Register callbacks in the return table: `pointerDown`, `pointerMove`, `pointerUp`, `pointerExit`

**PointerEvent properties**:
- `position: Vector` — local coordinates relative to the script
- `id: number` — unique identifier for multi-touch
- `event:hit()` — mark as handled, prevent propagation
- `event:hit(true)` — handle but pass through

**Nested pointer forwarding**: Manually convert to local space and forward:
```lua
local localEvent = PointerEvent.new(event.id, Vector.xy(event.position.x - offset.x, event.position.y - offset.y))
self.enemy:pointerDown(localEvent)
```

## Key API Classes

| Category | Classes | Purpose |
|---|---|---|
| Scene | Artboard, Animation, Context | Scene access and control |
| Scene Graph | Node | Object manipulation |
| Rendering | Renderer | Drawing API (drawPath, drawImage, clipPath, save/restore, transform) |
| Geometry | Path, PathCommand, PathData, ContourMeasure, PathMeasure | Path creation and measurement |
| Styling | Paint, PaintDefinition, BlendMode, StrokeCap, StrokeJoin | Fill/stroke configuration |
| Color | Color, Gradient, GradientStop | Color and gradient creation |
| Math | Vector, Mat2D | Vector and matrix operations |
| Images | Image, ImageFilter, ImageSampler, ImageWrap | Image handling |
| Data | DataValue (Boolean, Color, Number, String) | Data binding values |
| Reactive | Property, PropertyTrigger, Listener | Reactive data and events |
| Collections | PropertyList, PropertyEnum | Lists and enumerations |

**For exact method signatures**: Read the relevant page under `scripting/api-reference/` in source docs.

## Drawing Essentials

**Path**: `Path.new()` with `moveTo()`, `lineTo()`, `quadTo()`, `cubicTo()`, `close()`, `reset()`, `add(otherPath, transform)`

**Paint**: Set `color` (via `Color.rgba(r,g,b,a)` or `Color.hex()`), `stroke` width, `blendMode`, `strokeCap`, `strokeJoin`

**Renderer**: `drawPath(path, paint)`, `drawImage(image, sampler, blendMode, opacity)`, `clipPath(path)`, `save()/restore()`, `transform(mat2d)`

**Mat2D**: `Mat2D.withScale(sx, sy)` — fields: `xx, xy, yx, yy, tx, ty`

**Vector**: `Vector.xy(x, y)` and `Vector.origin()`; fields: `x`, `y`

**Important**: Don't mutate a path after drawing it in the same frame. Wait for next frame or create a new path.

## Common Patterns

**Fixed-step advance** (frame-independent movement):
```lua
self.accumulator += seconds
while self.accumulator >= dt and steps < MAX_STEPS do
  -- simulate at fixed dt
  self.accumulator -= dt
  steps += 1
end
```

**Memory management**: Always remove listeners to prevent leaks.

**Artboard instantiation**: `self.enemy:instance(viewModel?)` — creates independent copy.

## Before writing Luau code

1. Identify the protocol first: `Node`, `Layout`, `Converter`, `PathEffect`, `TransitionCondition`, `ListenerAction`, `Test`, or Util.
2. Use the protocol's exact lifecycle names and signatures. Protocol context is passed to `init(self, context)`; do not add a `context` field initialized with `late()` to returned protocol tables.
3. Use exact source-pack type names: `Vector`, `Mat2D`, `Path`, `Paint`, `Renderer`, `DataValueNumber`, `DataValueString`, `ListenerContext`.
4. Use `Vector.xy(...)`, not legacy or invented vector constructors.
5. Access ViewModel properties with `vm:getNumber(...)`, `vm:getString(...)`, and the other `get*` methods. Nil-check the returned property before reading or writing `.value`.
6. Keep `convert` and `evaluate` side-effect free. Listener actions and Node scripts are the right place for side effects such as audio playback.
7. Use `performAction(self, listenerContext)` for new ListenerAction scripts. Only mention `perform(self, pointerEvent)` when explaining deprecated code.
8. Remove listeners when a script owns their lifecycle, or keep the listened ViewModel anchored on `self`.
9. If a method is not in the curated reference or source pack, do not invent it. State what must be verified in source docs instead.

## Debugging

- **Console Tab**: View `print()` output during playback
- **Problems Tab**: Type errors, syntax errors, missing bindings (pre-execution)
- **Keyboard shortcuts**: Undo (Cmd+Z), Format (F4), Find (Cmd+F), Go to Definition (Cmd+Click), Multi-cursor (Alt+Click)
