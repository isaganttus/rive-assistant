# Rive Concept Map

> **How to use this file:** When asked about a Rive topic, find the row matching your topic. Read the **Reference File** first — it covers the concept. If you need exact API signatures or deeper detail, fetch the **Source path(s)** from the official Rive docs at `https://raw.githubusercontent.com/rive-app/rive-docs/main/<path>.mdx` (or read from `rive-docs/` if available locally).

Master lookup table. Use this to find where information lives.

## Editor & Design

| Topic | Reference File | Source path(s) — fetch for full API detail |
|---|---|---|
| Artboards (creation, sizing, origin, components) | 01-editor-fundamentals | `editor/fundamentals/artboards.mdx`, `editor/fundamentals/components.mdx` |
| Components (nested artboards, instances, modes) | 01-editor-fundamentals | `editor/fundamentals/components.mdx` |
| Groups, Solos, Draw Order | 01-editor-fundamentals | `editor/fundamentals/groups.mdx`, `editor/fundamentals/solos.mdx` |
| Shapes, Paths, Pen Tool | 01-editor-fundamentals | `editor/fundamentals/shapes-and-paths.mdx`, `editor/manipulating-shapes/pen-tool.mdx` |
| Fill, Stroke, Gradients, Feathering | 01-editor-fundamentals | `editor/fundamentals/fill-and-stroke.mdx` |
| Procedural Shapes (rect, ellipse, polygon, star) | 01-editor-fundamentals | `editor/manipulating-shapes/procedural-shapes.mdx` |
| Boolean Operations | 01-editor-fundamentals | `editor/manipulating-shapes/boolean-operations.mdx` |
| Bones & Meshes (skeletal rigging) | 01-editor-fundamentals | `editor/fundamentals/bones.mdx` |
| Text (runs, styles, modifiers, fonts) | 01-editor-fundamentals | `editor/text/overview.mdx`, `editor/text/` |
| Constraints (IK, distance, transform, follow-path, scroll) | 01-editor-fundamentals | `editor/constraints/` |
| Joysticks | 01-editor-fundamentals | `editor/fundamentals/joysticks.mdx` |
| Importing Assets (SVG, images, Lottie) | 01-editor-fundamentals | `editor/fundamentals/importing-assets.mdx` |
| Exporting (.riv, video, backup) | 01-editor-fundamentals | `editor/exporting/` |
| Libraries (shared assets across files) | 01-editor-fundamentals | `editor/libraries.mdx` |
| Interface (toolbar, hierarchy, inspector, stage) | 01-editor-fundamentals | `editor/interface-overview/` |

## Animation & Logic

| Topic | Reference File | Source path(s) — fetch for full API detail |
|---|---|---|
| State Machines (graph, states, transitions) | 02-state-machines-and-events | `editor/state-machine/state-machine.mdx` |
| States (entry, exit, any-state, animation, blend) | 02-state-machines-and-events | `editor/state-machine/states.mdx` |
| Transitions (conditions, duration, exit time) | 02-state-machines-and-events | `editor/state-machine/transitions.mdx` |
| Layers (parallel animations) | 02-state-machines-and-events | `editor/state-machine/layers.mdx` |
| Listeners (clicks, hovers, actions) | 02-state-machines-and-events | `editor/state-machine/listeners.mdx` |
| Events (general, URL, audio) — DEPRECATED except audio | 02-state-machines-and-events | `editor/events/overview.mdx`, `editor/events/audio-events.mdx` |
| Audio Events (sound triggers) | 02-state-machines-and-events | `editor/events/audio-events.mdx` |
| Inputs — DEPRECATED, use Data Binding | 02-state-machines-and-events | `editor/state-machine/inputs.mdx` |
| Animate Mode (timeline, keys, interpolation) | 02-state-machines-and-events | `editor/animate-mode/` |
| 1D Blend States | 02-state-machines-and-events | `editor/state-machine/states.mdx` |
| Additive Blend States | 02-state-machines-and-events | `editor/state-machine/states.mdx` |

## Data & Scripting

| Topic | Reference File | Source path(s) — fetch for full API detail |
|---|---|---|
| Data Binding Overview (MVVM, view models) | 03-data-binding | `editor/data-binding/overview.mdx` |
| View Model Properties (types, directions) | 03-data-binding | `editor/data-binding/overview.mdx` |
| View Model Instances (exported, internal) | 03-data-binding | `editor/data-binding/overview.mdx` |
| Lists (dynamic content, artboard lists) | 03-data-binding | `editor/data-binding/lists.mdx` |
| Converters (type transformation) | 03-data-binding | `editor/data-binding/overview.mdx` |
| Enumerations | 03-data-binding | `editor/data-binding/overview.mdx` |
| Data Binding at Runtime | 03-data-binding | `runtimes/data-binding.mdx` |
| Scripting Overview (Luau, getting started) | 05-scripting | `scripting/getting-started.mdx` |
| Creating Scripts | 05-scripting | `scripting/creating-scripts.mdx` |
| Node Scripts (draw, advance, init) | 05-scripting | `scripting/protocols/node-scripts.mdx` |
| Layout Scripts (measure, resize) | 05-scripting | `scripting/protocols/layout-scripts.mdx` |
| Converter Scripts (convert, reverseConvert) | 05-scripting | `scripting/protocols/converter-scripts.mdx` |
| Path Effect Scripts | 05-scripting | `scripting/protocols/path-effect-scripts.mdx` |
| Transition Condition Scripts | 05-scripting | `scripting/protocols/transition-condition-scripts.mdx` |
| Listener Action Scripts | 05-scripting | `scripting/protocols/listener-action-scripts.mdx` |
| Test Scripts (unit testing) | 05-scripting | `scripting/protocols/test-scripts.mdx` |
| Util Scripts (reusable modules) | 05-scripting | `scripting/protocols/util-scripts.mdx` |
| Script Inputs (Input<T>, late()) | 05-scripting | `scripting/script-inputs.mdx` |
| Pointer Events in Scripts | 05-scripting | `scripting/pointer-events.mdx` |
| Scripting Data Binding (context, view models) | 05-scripting | `scripting/data-binding.mdx` |
| Script API Reference | 05-scripting | `scripting/api-reference/` |
| Debugging (console, problems panel) | 05-scripting | `scripting/debugging/debug-panel.mdx` |

## Layouts

| Topic | Reference File | Source path(s) — fetch for full API detail |
|---|---|---|
| Layouts Overview (responsive containers) | 04-layouts | `editor/layouts/overview.mdx` |
| Layout Parameters (row/column, gap, alignment) | 04-layouts | `editor/layouts/layout-parameters.mdx` |
| Scale Types (fixed, hug, fill) | 04-layouts | `editor/layouts/layout-parameters.mdx` |
| N-Slicing (corner preservation) | 04-layouts | `editor/layouts/n-slicing.mdx` |
| Scrolling (scroll view, scroll bar, physics) | 04-layouts | `editor/layouts/scrolling.mdx` |
| Layout Styles | 04-layouts | `editor/layouts/styles.mdx` |

## App Runtimes

| Topic | Reference File | Source path(s) — fetch for full API detail |
|---|---|---|
| Runtime Architecture (overview, renderer choice) | 06-runtimes-overview | `runtimes/getting-started.mdx`, `runtimes/choose-a-renderer/` |
| Loading Assets (embedded, out-of-band) | 06-runtimes-overview | `runtimes/loading-assets.mdx` |
| Caching .riv files | 06-runtimes-overview | `runtimes/caching.mdx` |
| Feature Support Matrix | 06-runtimes-overview | `runtimes/feature-support.mdx` |
| Web JS Runtime | 07-web-react-runtime | `runtimes/web/` |
| React Runtime (useRive, RiveComponent) | 07-web-react-runtime | `runtimes/react/` |
| Flutter Runtime | 08-mobile-runtimes | `runtimes/flutter/` |
| Apple/iOS Runtime (SwiftUI, UIKit) | 08-mobile-runtimes | `runtimes/apple/` |
| Android Runtime (Kotlin, Compose) | 08-mobile-runtimes | `runtimes/android/` |
| React Native Runtime | 08-mobile-runtimes | `runtimes/react-native/` |
| Runtime Data Binding API | 06-runtimes-overview | `runtimes/data-binding.mdx` |
| Runtime State Machine Control | 06-runtimes-overview | `runtimes/state-machines.mdx` |

## Game Runtimes

| Topic | Reference File | Source path(s) — fetch for full API detail |
|---|---|---|
| Unity (RivePanel, RiveScreen, data binding) | 09-game-runtimes | `game-runtimes/unity/` |
| Unreal (plugin, Blueprints, data binding) | 09-game-runtimes | `game-runtimes/unreal/` |
| Defold | 09-game-runtimes | `game-runtimes/defold.mdx` |

## Cross-Cutting

| Topic | Reference File | Source path(s) — fetch for full API detail |
|---|---|---|
| Best Practices (performance, assets, optimization) | 10-best-practices | `getting-started/best-practices.mdx` |
| Getting Started / Introduction | 10-best-practices | `getting-started/introduction.mdx` |

## Common Questions Quick-Lookup

| Question | Start Here |
|---|---|
| How do I make responsive UI? | 04-layouts |
| How do I pass data between designer and developer? | 03-data-binding |
| How do I make something interactive? | 02-state-machines-and-events (Listeners section) |
| How do I write custom logic? | 05-scripting |
| How do I integrate Rive in my app? | 06-runtimes-overview, then platform-specific file |
| How do I optimize performance? | 10-best-practices |
| How do I play sounds? | 02-state-machines-and-events (Audio Events section) |
| How do I create reusable components? | 01-editor-fundamentals (Components section) |
| How do I create dynamic lists? | 03-data-binding (Lists section) |
| How do I animate between states? | 02-state-machines-and-events |
| What's deprecated and what should I use instead? | CLAUDE.md deprecation notice + 03-data-binding |
