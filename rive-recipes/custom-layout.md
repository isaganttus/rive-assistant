# Custom Layout Script (masonry grid)

**What this covers:** A Luau Layout script implementing a masonry grid — columns of equal width, items placed in the shortest column.
**Rive features used:** Scripting (Layout protocol), Layouts.

## Editor setup

1. Create a Layout on your artboard as the masonry container. Set height to **Hug**.
2. Create a **Script** asset: Assets Panel → + → Script → **Layout** protocol. Name it `MasonryLayout`.
3. Add the script as a **child** of the container layout (Layout scripts are added as children, not attached separately).
4. Add child item layouts or Components inside the container.

## Script

```lua
-- MasonryLayout.lua
type MasonryLayout = {}

local COLS = 3
local GAP = 8

-- Called once when the script initializes.
function init(self: MasonryLayout): boolean
  return true
end

-- Called whenever the layout receives a new size from its parent.
-- All child positioning runs here.
function resize(self: MasonryLayout, size: Vec2D)
  local colW = (size.x - GAP * (COLS - 1)) / COLS
  local heights: {number} = {}
  for i = 1, COLS do heights[i] = 0 end

  for _, child in ipairs(self:children()) do
    -- Find the shortest column
    local minCol = 1
    for c = 2, COLS do
      if heights[c] < heights[minCol] then minCol = c end
    end

    local x = (minCol - 1) * (colW + GAP)
    local y = heights[minCol]
    child:setPosition(Vec2D.xy(x, y))
    child:setSize(Vec2D.xy(colW, child:intrinsicHeight()))
    heights[minCol] = heights[minCol] + child:intrinsicHeight() + GAP
  end
end

-- Only called when parent uses Hug sizing; propose the layout's ideal size.
function measure(self: MasonryLayout): Vec2D
  return Vec2D.xy(0, 0) -- runtime computes from the resize pass
end

return function(): Layout<MasonryLayout>
  return { init = init, resize = resize, measure = measure }
end
```

> **API note:** `Vec2D.xy(x, y)` is the constructor confirmed in `scripting/protocols/layout-scripts.mdx`. Verify `self:children()`, `child:setPosition()`, `child:setSize()`, and `child:intrinsicHeight()` against the same source — the docs example for `resize` covers size access but not child iteration directly.

## Notes

- `resize(size)` is called whenever the container resizes — all placement logic runs here.
- `measure()` is only called when the parent uses Hug sizing.
- Layout scripts extend Node, inheriting `init`, `advance`, `draw`, and pointer callbacks.
- `COLS` and `GAP` are hardcoded here — expose them as Script Inputs to make them configurable from the editor.
- Source docs: `scripting/protocols/layout-scripts.mdx`
