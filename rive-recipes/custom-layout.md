# Custom Layout Script (measured panel)

**What this covers:** A Luau Layout script that reports a minimum measured size and stores the latest size assigned by its parent.
**Rive features used:** Scripting (Layout protocol), Layouts.

## Editor setup

1. Create a Layout on your artboard as the measured panel. Set width or height to **Hug** when you want the script's `measure` result to drive sizing.
2. Create a **Script** asset: Assets Panel → + → Script → **Layout** protocol. Name it `MeasuredPanel`.
3. Add the script as a **child** of the container layout (Layout scripts are added as children, not attached separately).
4. Set `minWidth` and `minHeight` as Script Inputs if you want designers to configure the measured size in the editor.

## Script

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

> **API note:** The source pack defines layout sizing with `Vector`, `resize(self, size: Vector)`, and optional `measure(self): Vector`. Do not use child traversal or mutation methods unless you have verified those exact APIs in the current source docs.

## Notes

- `resize(size)` is called whenever the container receives a size from its parent.
- `measure()` is only called when the parent uses Hug sizing.
- Layout scripts extend Node, inheriting `init`, `advance`, `draw`, and pointer callbacks.
- `minWidth` and `minHeight` are Script Inputs, so the measured size can be configured from the editor.
- Source docs: `scripting/protocols/layout-scripts.mdx`
