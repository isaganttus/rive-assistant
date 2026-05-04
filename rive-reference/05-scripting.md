# Rive Scripting Reference
> Last verified: 2026-04-23

## Overview

Rive Scripting uses **Luau** (Roblox's typed Lua variant) with type annotations. Scripts are assets saved in the Assets Panel. Naming convention: PascalCase matching the main type name.

**Source docs**: `scripting/` directory in the Rive docs.

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
**Purpose**: Custom layout algorithms (masonry, carousels).

Extends Node (inherits all lifecycle). Additional:
- `measure(self) -> Vec2D`: Returns ideal size (only for Hug fit type)
- `resize(self, size: Vec2D)`: Required; called when layout resizes

### Converter Scripts
**Purpose**: Transform data between view model and bound properties (2-way).

- `init(self) -> bool`: Setup
- `convert(self, input: DataInputs) -> output`: Input to output (required)
- `reverseConvert(self, input: DataOutput) -> input`: Output to input (for 2-way binding)

Factory: `Converter<MyConverter, InputType, OutputType>`

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

- `init(self, context) -> bool`: Setup
- `perform(self, pointerEvent)`: Called when listener fires (no return value)

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
- Write: `property.value = newValue`
- Triggers: `getTrigger()` then `:fire()`
- Listeners: `property:addListener(callback)` — always `removeListener` to prevent leaks

**Context utility methods**:
- `context:image(name)` — get image asset
- `context:blob(name)` — get raw binary data
- `context:audio(name)` — get audio source
- `context:markNeedsUpdate()` — re-trigger update function

## Pointer Events

Register callbacks in the return table: `pointerDown`, `pointerMove`, `pointerUp`, `pointerExit`

**PointerEvent properties**:
- `position: Vec2D` — local coordinates relative to script
- `id: number` — unique identifier for multi-touch
- `event:hit()` — mark as handled, prevent propagation
- `event:hit(true)` — handle but pass through

**Nested pointer forwarding**: Manually convert to local space and forward:
```lua
local localEvent = PointerEvent.new(event.id, Vec2D.xy(event.position.x - offset.x, ...))
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
| Math | Vec2D, Mat2D | Vector and matrix operations |
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

**Vec2D**: `Vec2D.xy(x, y)` — fields: `x, y`

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

## Debugging

- **Console Tab**: View `print()` output during playback
- **Problems Tab**: Type errors, syntax errors, missing bindings (pre-execution)
- **Keyboard shortcuts**: Undo (Cmd+Z), Format (F4), Find (Cmd+F), Go to Definition (Cmd+Click), Multi-cursor (Alt+Click)
