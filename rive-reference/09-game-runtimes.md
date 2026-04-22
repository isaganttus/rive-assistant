# Rive Game Runtimes Reference

## Overview

Game runtimes integrate Rive into game engines. Key difference from app runtimes: game engines have their own render pipelines and game loops, so integration points differ.

**Source docs**: `game-runtimes/unity/`, `game-runtimes/unreal/`, `game-runtimes/defold.mdx`

## Unity

### Installation
Via Unity Package Manager using the Rive Unity package.

### Key Components

**RivePanel**: UI component for rendering Rive in Unity's UI system.
- Add to Canvas hierarchy
- Configure artboard, state machine
- Handles input forwarding automatically

**RiveScreen**: Renders Rive to a full-screen overlay or camera texture.
- Useful for HUDs, splash screens, overlays

**Procedural Rendering**: Render Rive to textures for use on 3D objects.
- Create RenderTexture target
- Apply to materials for in-world Rive animations

### Fundamentals
- Load .riv files as Unity assets (drag into project)
- Artboard selection and state machine setup
- Animation playback control
- Input handling (pointer events forwarded automatically for UI)

### Data Binding
- Access view model instances from C# code
- Get/set properties programmatically
- Subscribe to property change events
- Work with lists

### Runtime Asset Swapping
Replace images, fonts, and other assets at runtime from Unity's asset pipeline.

### Listeners
Unity forwards pointer events to Rive listeners automatically when using RivePanel/RiveScreen.

**For detailed Unity API**: See `game-runtimes/unity/` source docs.

## Unreal Engine

### Installation
Install the Rive plugin from Unreal Marketplace or GitHub.

### Key Features

**Blueprint Integration**:
- Observe view model property changes from Blueprints
- Use triggers from Blueprints
- Set up data binding visually

**C++ Integration**:
- Full API access for view model manipulation
- Property change callbacks
- Trigger firing

**In-World Textures**:
- Render Rive to textures for use on 3D meshes
- Apply to materials for in-world interactive animations

### Data Binding
- Access view model instances from Blueprints or C++
- Observe property changes
- Fire triggers
- Update property values

**For detailed Unreal API**: See `game-runtimes/unreal/` source docs.

## Defold

Community-maintained runtime for the Defold game engine.

- Basic .riv loading and rendering
- State machine playback
- Input handling

**For Defold details**: See `game-runtimes/defold.mdx` in source docs.

## Key Differences from App Runtimes

| Aspect | App Runtimes | Game Runtimes |
|---|---|---|
| Render loop | Runtime manages draw cycle | Engine manages draw cycle |
| Input | DOM/native touch events | Engine input system forwarded |
| UI integration | Native view/component | Canvas/Widget/Overlay system |
| 3D usage | Not applicable | Render to texture for in-world use |
| Asset pipeline | Load from URL/bundle | Engine asset import system |

## Common Patterns

1. **UI overlays**: Use RivePanel (Unity) or Widget (Unreal) for HUD elements
2. **In-world animation**: Render to texture, apply to material
3. **Data binding**: Same view model pattern as app runtimes, different API surface
4. **Performance**: Game engines handle frame timing; Rive advances within engine's update loop
