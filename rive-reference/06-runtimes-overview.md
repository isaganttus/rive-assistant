# Rive Runtimes Overview Reference

## Overview

Runtimes are platform-specific libraries that load .riv files and render them natively. All runtimes share a common pattern: load file, select artboard, set up state machine, bind data, handle events.

**Source docs**: `runtimes/getting-started.mdx`, `runtimes/choose-a-renderer/`, `runtimes/loading-assets.mdx`, `runtimes/caching.mdx`, `runtimes/state-machines.mdx`, `runtimes/data-binding.mdx`

## Official Runtimes

| Platform | Package / Source | Install Method |
|---|---|---|
| Web JS | `@rive-app/canvas`, `@rive-app/webgl2` | npm |
| React | `@rive-app/react-canvas`, `@rive-app/react-webgl2` | npm |
| React Native | `rive-react-native` | npm |
| Flutter | `rive` | pub.dev |
| Apple (iOS/macOS) | `RiveRuntime` | SPM, CocoaPods |
| Android | `app.rive:rive-android` | Maven |
| C++ | GitHub source | Build from source |
| Unity | Rive package | Unity Package Manager |
| Unreal | Rive plugin | Unreal Marketplace / GitHub |
| Defold | Community runtime | Defold dependency |

## Renderer Choice

Each platform has a default renderer and optionally supports the Rive Renderer.

| Platform | Default Renderer | Rive Renderer Available? |
|---|---|---|
| Android | Rive | Yes (default) |
| Apple | Rive | Yes (default) |
| React Native | Rive (platform-dependent) | Yes |
| Web Canvas | Canvas2D | No (use WebGL2 package) |
| Web WebGL2 | Rive | Yes (default) |
| Flutter | Choose explicitly | Yes (or Flutter/Skia/Impeller) |

**Rive Renderer**: New high-performance engine for best quality and performance. Required for:
- Vector Feathering
- Advanced blend modes
- Best rendering fidelity

## Common Runtime Pattern

All platforms follow this flow:
1. **Load** the .riv file (URL, local path, or ArrayBuffer)
2. **Select artboard** (by name or use default)
3. **Set up state machine** (by name)
4. **Bind data** — get/set view model properties, subscribe to changes
5. **Handle events** — listen for reported events
6. **Render** — platform handles draw loop (or custom render loop for advanced use)

## Loading Assets

Assets can be embedded in .riv or loaded out-of-band at runtime.

**Out-of-band benefits**:
- Reduce .riv file size
- Reuse assets across multiple .riv files
- Preload and cache assets
- Swap based on resolution/locale

**Asset types**: Images, Fonts, Audio

Each runtime has platform-specific APIs for asset loading callbacks.

## Caching .riv Files

Parse a .riv file once and reuse for multiple artboard instances.

**Benefits**: Significantly faster instantiation; reduced memory; efficient for repeated use (lists, grids).

## State Machine Control at Runtime

All runtimes provide APIs for:
- Starting/stopping state machines
- Reading and setting inputs (legacy) or view model properties (modern)
- Subscribing to state changes
- Handling reported events

## Data Binding at Runtime

Modern runtimes provide APIs for the Data Binding system:
- **Get view model instances** from artboard
- **Read properties**: numbers, strings, booleans, colors, enums, lists, nested view models
- **Write properties**: set values programmatically
- **Subscribe to changes**: listen for property updates
- **Work with lists**: add, remove, update items dynamically

**For platform-specific API details**: See the platform runtime reference files (07, 08, 09) and `runtimes/data-binding.mdx`.

## Web Package Variants

| Package | Renderer | Notes |
|---|---|---|
| `@rive-app/canvas` | Canvas2D | Smaller, no Rive Renderer features |
| `@rive-app/webgl2` | Rive Renderer | Best quality, supports feathering |
| `*-lite` variants | Same | No text, layout, audio, scripting support |
| `*-single` variants | Same | WASM bundled in JS (fewer network requests, larger bundle) |

## Feature Support

Not all features are available on all platforms/renderers. Key things to check:
- Vector Feathering (requires Rive Renderer)
- Blend modes (some require Rive Renderer)
- Text rendering
- Audio playback
- Scripting support
- Layout support

**For the full matrix**: See `runtimes/feature-support.mdx` in source docs.
