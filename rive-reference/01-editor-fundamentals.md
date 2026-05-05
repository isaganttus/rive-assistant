# Rive Editor Fundamentals Reference
> Last verified: 2026-04-23
> Source docs: `editor/fundamentals/`, `editor/interface-overview/`, `editor/constraints/`, `editor/text/`, `editor/manipulating-shapes/`, `editor/exporting/`, `editor/libraries.mdx`

## Overview

The Rive Editor is where all design and animation happens. This covers the core building blocks.

## Artboards

Foundation of every composition. Root of the hierarchy. Defines scene dimensions and background.

- **Multiple artboards per file** — only one "active" at a time in the editor
- **Default State Machine**: Sets which SM plays with toolbar play button; also sets default artboard for runtime
- **Creation**: Stage options or Artboard tool (A shortcut); drag to define bounds
- **Size types**: Fixed (defined dimensions) or Hug (auto-size to children)
- **Origin**: Determines measurement point (X:0% Y:0% = top-left). Best changed before animation.

## Components (Formerly Nested Artboards)

Reusable artboard instances. Toggle component mode on any artboard or use Shift+N.

**Placement**: Component Tool (N shortcut) or dropdown menu.

### Instance Modes
| Mode | Behavior |
|---|---|
| **Node** (default) | Content scaled via Scale property; non-responsive |
| **Leaf** | Positioned/resized relative to parent Layout; Fit types: Fill, Contain, Cover, Fit Width, Fit Height, None, Scale Down |
| **Layout** | Contains responsive Layouts; artboard size changes to reflow contents |

### Key Features
- **Expose Inputs/Events**: Right-click > "expose to main artboard" — accessible via listeners and Inputs panel
- **Animation playback**: Simple (key start + speed) or Remap (key time percent 0-100%)
- **Mix Value**: Default 100%; controls animation blending

## Groups & Solos

- **Groups**: G shortcut or Cmd+G to wrap. Unwrap: Cmd+Shift+G.
- **Target Style**: Always-visible icon; disables navigation into group. Useful with Constraints.
- **Solos**: Toggle visibility groups. **Faster than opacity** — skips computation/rendering for deactivated items. Use for skins/variants.

## Shapes & Paths

- **Shape Layer**: Renders vectors; defines fill/stroke styling
- **Path Layer**: Defines actual geometry; multiple paths per shape; drag-drop between shapes
- **Navigation**: Enter key = down hierarchy; Esc = up hierarchy

### Pen Tool (P shortcut)
- Click to place vertices; click+drag for Bezier handles; Esc to finish
- Alt+click on vertex = delete; Cmd+click = toggle mirrored/straight handles
- Boolean operations available for combining shapes

### Procedural Shapes
Rectangle, Ellipse, Polygon, Star — created via Create Tools menu. Press Enter to convert to custom path (loses procedural properties).

## Fill & Stroke

- **Fill types**: Solid, Linear Gradient, Radial Gradient
- **Fill Rule**: Non-Zero, Even-Odd, Clockwise (Rive-exclusive; enables manual path subtraction and vector feathering)
- **Feathering**: Direction (Outer/Inner), Space (World/Local), Offset
- **Stroke types**: Solid, Trim, Dashed
- **Stroke properties**: Cap (Butt/Round/Square), Join (Round/Bevel/Miter)
- **Effect Groups**: Apply effects to multiple fills/strokes without individual configuration

## Bones & Meshes

Skeletal rigging for deformation animation.

- **Bones**: Define skeleton structure; create parent-child chains
- **Meshes**: Vertex-based deformation linked to bones; bind mode for weight assignment
- **Constraints work with bones**: IK chains, rotation limits, etc.

## Text

- **Text Runs**: Individual text segments with independent styling
- **Styles**: Reusable text formatting (font, size, weight, color)
- **Modifiers**: Dynamic text effects
- **Fonts**: Custom OTF/TTF upload; glyph selection for optimization
- **Text is data-bindable**: Connect to view model string properties

## Constraints

8 types linking object properties:

| Constraint | Purpose |
|---|---|
| **IK** | Inverse kinematics for bone chains |
| **Distance** | Maintain distance between objects |
| **Scale** | Link scale between objects |
| **Rotation** | Link rotation |
| **Transform** | Link full transform (position + rotation + scale) |
| **Translation** | Link position |
| **Follow Path** | Move along a path |
| **Scroll** | Scroll constraint for layout scrolling |

## Joysticks

2D input mapped to animation parameters. Define X/Y axes linked to different animations.

## Importing Assets

- **Supported**: SVG, JSON (Lottie), PNG, PSD, JPG; drag-drop or Assets panel
- **Custom Fonts**: OTF/TTF files (Pro feature)
- **SVG tips**: Inline style preferred over CSS; retain IDs/names; presentation attributes work best
- **Known SVG limitations**: No embedded images, no gradient transforms, no mask/filter/skew support

## Exporting

- **.riv file**: Runtime-ready binary. Export via toolbar or File menu.
- **Video**: Export as MP4/GIF for sharing
- **Backup**: Download .rev file for full project backup
- **Embed URLs**: Generate shareable URLs for web embedding

## Libraries (Voyager/Enterprise)

Shared assets across files in a workspace.

- **Publish**: Export > Publish Library (file with components/view models)
- **Import**: Library icon in asset/data panels > Add to File
- **Update**: Republish library; host files show update badge
- **Detach**: Decouple from source (cannot re-attach)
- **Export options**: Automatic (if used), Force Export, Prevent Export

## Interface Components

- **Toolbar**: Tools, customization, artboard setting, export/share
- **Hierarchy**: Tree view of objects + Assets Panel + Data Panel tabs
- **Inspector**: Dynamic properties based on selection
- **Stage**: Infinite canvas; infinite nesting via groups/bones
- **Timeline**: Animation keyframes (bottom in Animate mode)
- **State Machine Graph**: Replaces Timeline when SM selected

### Stage Navigation
- Double-click to enter group; Cmd+click for deep select
- Right-click+drag or Spacebar to pan; Cmd+scroll to zoom
- F key to fit selection; Cmd+0 for 100%
