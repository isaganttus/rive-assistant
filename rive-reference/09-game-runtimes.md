# Rive Game Runtimes Reference
> Last verified: 2026-04-23

## Overview

Game runtimes integrate Rive into game engines. Key difference from app runtimes: game engines have their own render pipelines and game loops, so integration points differ.

**Source docs**: `game-runtimes/unity/`, `game-runtimes/unreal/`, `game-runtimes/defold.mdx`

## Unity

### Supported Versions

Unity LTS versions 2021 and above, including Unity 6. Rendering backends: Metal (Mac/iOS), D3D11/D3D12 (Windows), OpenGL (Windows/Android), Vulkan (Windows/Android/Ubuntu 24.04+), WebGL.

### Installation

Two options via the Unity Package Manager:

**Unity Asset Store (stable releases only)**
1. Open Window → Package Manager
2. Select My Assets
3. Find Rive and select Download / Import

**GitHub via UPM git URL (stable + canary releases)**

Add via Window → Package Manager → "Add package from git URL…":
```
https://github.com/rive-app/rive-unity.git?path=package#v0.0.0
```
Replace `v0.0.0` with the [latest release tag](https://github.com/rive-app/rive-unity/releases). Or add directly to `Packages/manifest.json`:
```json
"app.rive.rive-unity": "https://github.com/rive-app/rive-unity.git?path=package#v0.0.0"
```

Once installed, drag `.riv` files into the Unity **Project** window. Unity imports them as **Rive Asset** objects.

### Key Components

**RivePanel**: The foundation rendering component. Acts as a viewport that manages one or more Rive Widgets, rendering them all to a single RenderTexture. Multiple Widgets under one Panel share a texture — more efficient than multiple Panels.
- Right-click in Hierarchy → `Rive > Rive Panel`
- Requires a Panel Renderer to display its texture

**RiveWidget**: The primary component for displaying a Rive artboard. Manages file loading, artboard selection, state machine setup, and data binding mode. Must be placed under a RivePanel.
- Right-click in Hierarchy → `Rive > Widgets > Rive Widget`
- Configure `Asset`, `Artboard Name`, `State Machine Name` in the Inspector
- Events: `OnWidgetStatusChanged`, `OnRiveEventReported`

**RiveCanvasRenderer** (Panel Renderer): Displays a RivePanel's texture inside Unity's uGUI Canvas system. Handles UI input forwarding automatically. Requires an EventSystem and GraphicRaycaster on the Canvas. Use this for HUDs and menus.

**RiveTextureRenderer** (Panel Renderer): Projects a RivePanel's texture onto a 3D mesh material. Requires a MeshRenderer and MeshCollider on the target GameObject, plus a PhysicsRaycaster on the camera for pointer input in 3D space. Use this for in-world Rive surfaces.

**When to use each:**
- Use **RivePanel + RiveCanvasRenderer** for screen-space UI (HUDs, menus, overlays)
- Use **RivePanel + RiveTextureRenderer** for in-world 3D mesh surfaces

### Procedural Rendering to Texture

To render Rive content onto a 3D object:
1. Create a RivePanel (the render target holder)
2. Add a RiveWidget under it pointing to your `.riv` asset
3. Add a RiveTextureRenderer on the 3D mesh GameObject and link it to the RivePanel
4. Unity auto-creates and assigns the material using the Panel's RenderTexture

For custom render pipelines, access `rivePanel.RenderTexture` directly and apply it to any material.

### State Machine Control from C#

Access the state machine after the widget reports `WidgetStatus.Loaded`:

```csharp
[SerializeField] private RiveWidget riveWidget;

void OnEnable()
{
    riveWidget.OnWidgetStatusChanged += HandleWidgetStatusChanged;
}

void OnDisable()
{
    riveWidget.OnWidgetStatusChanged -= HandleWidgetStatusChanged;
}

private void HandleWidgetStatusChanged()
{
    if (riveWidget.Status == WidgetStatus.Loaded)
    {
        StateMachine stateMachine = riveWidget.StateMachine;
        // RiveWidget advances the state machine automatically each frame
    }
}
```

For the low-level (legacy) API, advance the state machine manually:
```csharp
private void Update()
{
    stateMachine?.Advance(Time.deltaTime);
}
```

### C# Data Binding API

The preferred approach uses **ViewModels**. Set the `Data Binding Mode` on the RiveWidget in the Inspector (`Auto Bind Default`, `Auto Bind Selected`, or `Manual`).

**Getting a ViewModel instance:**
```csharp
private void HandleWidgetStatusChanged()
{
    if (riveWidget.Status == WidgetStatus.Loaded)
    {
        // Auto-bound instance (when using Auto Bind Default)
        ViewModelInstance vmi = riveWidget.StateMachine.ViewModelInstance;

        // Or get by name from the file (Manual mode)
        ViewModel vm = riveWidget.File.GetViewModelByName("PlayerStats");
        ViewModelInstance vmiManual = vm.CreateDefaultInstance();
        riveWidget.StateMachine.BindViewModelInstance(vmiManual);
    }
}
```

**Reading and writing properties:**
```csharp
ViewModelInstance vmi = riveWidget.StateMachine.ViewModelInstance;

// String
ViewModelInstanceStringProperty nameProp = vmi.GetStringProperty("playerName");
nameProp.Value = "Hero";

// Number
ViewModelInstanceNumberProperty hpProp = vmi.GetNumberProperty("health");
hpProp.Value = 85.0f;

// Boolean
ViewModelInstanceBooleanProperty activeProp = vmi.GetBooleanProperty("isActive");
activeProp.Value = true;

// Color
ViewModelInstanceColorProperty colorProp = vmi.GetColorProperty("tint");
colorProp.Value = new UnityEngine.Color(1f, 0f, 0f, 1f);

// Trigger (one-shot action)
ViewModelInstanceTriggerProperty trigger = vmi.GetTriggerProperty("onHit");
trigger.Trigger();

// Nested property via path notation
var nestedNum = vmi.GetNumberProperty("Inventory/Weapon/damage");
```

Subscribe to `OnValueChanged` on any typed property to react when Rive's state machine modifies a value back to Unity code.

### Asset Loading and Swapping

Provide a `CustomAssetLoaderCallback` when loading the Rive file to swap fonts, images, or audio at runtime:

```csharp
private bool AssetLoaderDelegate(EmbeddedAssetReference assetRef)
{
    if (assetRef is ImageEmbeddedAssetReference imageRef)
    {
        imageRef.SetImage(myImageOutOfBandAsset);
        return true;
    }
    return false;
}

// Load with custom asset handler
File riveFile = Rive.File.Load(myRiveAsset, AssetLoaderDelegate);

// Or with fallback to Inspector-assigned assets for unhandled types
File riveFile = Rive.File.Load(myRiveAsset, AssetLoaderDelegate, fallbackToAssignedAssets: true);
```

Asset types: `FontOutOfBandAsset`, `ImageOutOfBandAsset`, `AudioOutOfBandAsset`. For runtime-fetched assets (e.g., from a CDN):
```csharp
var img = OutOfBandAsset.Create<ImageOutOfBandAsset>(imageBytes);
```

Always call `Unload()` on out-of-band assets and `Dispose()` on the File when done.

## Unreal Engine

### Supported Versions and Platforms

Unreal Engine 5.7.3 and above. Supported platforms: Windows (DirectX), macOS (Metal). Mobile support is planned but not yet available. The runtime uses RHI for rendering backend integration.

### Installation

**Fab / Epic Games Launcher (recommended)**
1. Open the Epic Games Launcher or Unreal Editor and navigate to Fab
2. Search for "Rive" or go directly to: `https://www.fab.com/listings/3a2968c1-4a1d-427c-934e-92e4d8578b77`
3. Add the plugin to your engine or project
4. Restart Unreal Engine if prompted

**GitHub**
```bash
git clone https://github.com/rive-app/rive-unreal.git
```
Copy the `Rive` plugin folder into your project's `Plugins/` directory, then regenerate project files and build.

**Enable the plugin:** Edit → Plugins → locate "Rive" under Runtime → Enable → restart editor.

### Importing a Rive File

Drag a `.riv` file into the Content Browser. Unreal creates a **Rive File** asset. This asset does not render directly — it is the data source for widgets and render targets.

> Note: The Unreal runtime does not yet support referenced (out-of-band) assets. Embed all assets inside the `.riv` file before importing.

### RiveActor and Widget Setup

The core Unreal runtime objects are the **Rive File** (Unreal asset containing imported data), the **Artboard** (runtime instance for evaluation and rendering), and the **ViewModel** (typed data boundary between Unreal and Rive logic).

**Rive Widget (screen-space UI/UMG):**
1. Right-click a Rive File asset → **Create Rive Widget**
2. Use the widget in any Blueprint as a standard UMG widget
3. If the Rive file does not use autobinding, assign a ViewModel via the **Make View Model** Blueprint node

### Blueprint Integration

**Binding a ViewModel:**
```
Event BeginPlay
  → Create Widget (class: YourRiveWidget)
  → Add to Viewport
  → Make View Model (select ViewModel type)
  → Set View Model on the widget instance
```

**Observing property changes in Blueprint:**
1. Get the bound ViewModel Instance reference
2. Call **Add Field Value Changed Delegate** on a specific property
3. Connect a Custom Event to handle the updated value

The callback fires synchronously during the artboard tick: Unreal sets values → state machine evaluates → state machine may modify values → callbacks fire → rendering occurs.

**Firing a trigger from Blueprint:**
1. Get the bound ViewModel Instance
2. Call **Call {TriggerName}** (e.g., `Call OnClick`)

The trigger fires during the next artboard tick and resets automatically.

**Observing a trigger result from Blueprint:**
Use **Bind Event to {TriggerName}** on the ViewModel Instance. Unbind delegates before destroying the instance to avoid dangling references.

### C++ Data Binding Access

```cpp
// Create and bind a ViewModel Instance
URiveViewModel* ViewModel = RiveFile->MakeViewModel(TEXT("PlayerStats"));
URiveViewModelInstance* Instance = ViewModel->CreateInstance();

// Write input values
Instance->SetNumberProperty(TEXT("health"), 85.0f);
Instance->SetBoolProperty(TEXT("isShielded"), true);

// Observe output changes from the state machine
Instance->BindFieldValueChanged(TEXT("score"),
    FRivePropertyChanged::CreateLambda([this](URiveViewModelInstance* Inst)
    {
        float NewScore = Inst->GetNumberProperty(TEXT("score"));
        // React to state machine output in C++
    }));

// Bind to the artboard
RiveArtboard->BindViewModelInstance(Instance);
```

Unobserve callbacks before destroying the ViewModel Instance. State machine events and direct input mechanisms are deprecated — use ViewModels for all input and output in new integrations.

### In-World Texture Rendering

Use a **Rive RenderTarget** asset to display Rive on a 3D mesh surface:

1. Right-click a Rive File asset → **Create Rive Render Target**
2. Double-click to configure: Rive File, Artboard, State Machine, and Size/Resolution (start with 512×512)
3. Drag the RenderTarget from the Content Browser into the viewport — Unreal spawns an actor, creates a material sampling the texture, and assigns it to the mesh
4. Add a **RiveRenderTargetUpdater** component to an Actor Blueprint in the level and point it at the RenderTarget to drive tick and draw each frame

Without a driver component the RenderTarget appears static. For interactive in-world content, bind a ViewModel to the RenderTarget and set values or fire triggers as normal.

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

1. **UI overlays**: Use RiveWidget + RiveCanvasRenderer (Unity) or URiveWidget in UMG (Unreal) for HUD and menu elements
2. **In-world animation**: RiveTextureRenderer on a mesh (Unity) or Rive RenderTarget + RiveRenderTargetUpdater (Unreal)
3. **Data binding**: Same ViewModel concept as app runtimes — get a ViewModelInstance, read/write typed properties, observe changes via callbacks
4. **Performance**: Game engines handle frame timing; Rive advances within the engine's update loop — use Auto update mode in Unity or the RiveRenderTargetUpdater driver in Unreal rather than manual tick management where possible
