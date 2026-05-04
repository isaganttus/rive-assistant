# Rive Layouts Reference
> Last verified: 2026-04-23
> Source docs: `editor/layouts/`

## Overview

Layouts build responsive UI in Rive using rules-based row/column containers instead of freeform positioning. They adapt to content size, text changes, and screen dimensions.

**Key insight**: Layouts only affect the position of other Layouts. Non-layout Rive objects inside a layout can animate independently.

## Absolute vs. Relative Positioning

Every layout child is either:
- **Absolute**: Positioned on artboard/parent freely (freeform)
- **Relative**: Position determined by parent's Row/Column, alignment, padding, gap rules

Toggle via icon in top-right of layout inspector.

## What Layouts Control

| Control Level | Object Types |
|---|---|
| **Position + Size** | Text, Images, Parametric shapes (rect/ellipse/triangle/polygon/star), Component instances (Leaf & Layout mode), other Layouts |
| **Position Only** | All other objects |

N-Slicing enables shape/group layout behavior for more complex cases.

## Parent Layout Parameters

### Direction & Flow
- **Row/Column**: Horizontal or Vertical layout; Reverse options available
- **Wrap**: No Wrap (extend beyond bounds), Wrap, Wrap Reverse
- **Left-to-Right / Right-to-Left**: Cascade to children; for language support

### Spacing
- **Gap**: Horizontal and Vertical spacing between children (points or percentages)
- **Padding**: Inner space between bounds and children (per-edge toggle available)

### Alignment
9-point grid (Center default): Top Left, Top Center, Top Right, etc. Click alignment to expand justify options.

## Child Layout Parameters

### Scale Types
| Type | Behavior |
|---|---|
| **Fixed** | Defined size in points or percentage of parent |
| **Hug** | Shrink to fit children content |
| **Fill** | Expand to fill available space (fr units); supports base size |

### Constraints
- **Min/Max Width/Height**: Limit dimensions (points or percentages)
- **Clip**: Hide content extending beyond bounds

### Spacing
- **Margin**: Outer space relative to parent (per-edge toggle)
- **Padding**: Inner space (when child is also a layout)

### Position (Absolute only)
- Pin edges (2+ required); distance from edges in points or %

## Layout Tools

- **Layout Tool**: Drag on artboard (Absolute) or existing Layout (Relative)
- **Row/Column Tools**: Create with initial children (number/arrow keys while dragging)
- **Wrap in Layout**: Right-click > Wrap in > Layout or Shift+L
- **Add Child Layout**: Button when Layout selected

## N-Slicing

Prevents corner distortion when resizing (inspired by 9-slice).

- **Applies to**: Images/Raster (select + add N-Slice) or Groups/Vectors (convert or wrap)
- **Edit Mode**: Press Enter or Edit N-Slice button
- **Axes**: Default 4 (2 vertical, 2 horizontal = 9 segments); click bounds to add more
- **Segments**: Alternate between fixed (solid borders) and scaling (dashed borders)
- **Tile Modes**: Stretch (default), Repeat, Hidden

## Scrolling

### Content Scrolling
Build a scroll view with this hierarchy:
```
Scroll View (Layout)
  └─ Scroll Content (Layout + Scroll Constraint)
       └─ Scroll Items (Layouts)
```

**Scroll Constraint Properties**:
- Direction: Vertical, Horizontal, or All
- Scroll Percent X/Y: Animatable, 0-100%
- Scroll Index: Animatable, 0-based item index
- Physics: Elastic (iOS-style deceleration + rubber banding) or Clamped (basic drag)
- Snap: Settle with whole item at top/left

**Advanced**:
- **Virtualize**: Performance optimization for large lists (only renders visible items)
- **Carousel**: Endless scroll with virtualization enabled

### Scroll Bar
```
Scroll Bar (Layout)
  └─ Scroll Thumb (Layout + Scroll Bar Thumb Constraint)
```
Connect thumb's target to the Layout with Scroll Constraint.

## Best Practices

1. Use Layouts for any UI that needs to adapt to content or screen size
2. Combine with Components (Leaf mode) for responsive reusable elements
3. Use Hug for content-driven sizing, Fill for space-filling
4. N-Slicing for any resizable graphics with corners/borders
5. Virtualize long scrolling lists for performance
6. Layouts + Data Binding Lists = dynamic responsive UI
