# Rive Web & React Runtime Reference
> Last verified: 2026-04-23

## Overview

The Web runtime is the JavaScript/WASM-based Rive engine for browsers. React wrappers provide hooks and components on top.

**Source docs**: `runtimes/web/`, `runtimes/react/`

## Web JS Runtime

### Installation

**Script tag**:
```html
<script src="https://unpkg.com/@rive-app/canvas@latest"></script>
```

**Package manager**: `npm install @rive-app/canvas` (or `@rive-app/webgl2`)

### Basic Setup

```javascript
const r = new rive.Rive({
  src: "path/to/file.riv",
  canvas: document.getElementById("canvas"),
  stateMachines: "StateMachineName",
  autoplay: true,
  onLoad: () => {
    r.resizeDrawingSurfaceToCanvas();
  },
});
```

**Critical**: Call `resizeDrawingSurfaceToCanvas()` in `onLoad` and on window resize for sharp rendering.

### Loading Files

1. **URL**: `src: "https://example.com/file.riv"`
2. **Static asset**: `src: "/public/file.riv"`
3. **ArrayBuffer**: `buffer: arrayBuffer` (from fetch)
4. **Reuse parsed file**: `rivFile: alreadyParsedFile`

### Cleanup

Always call `riveInstance.cleanup()` to free C++ WASM objects and prevent memory leaks.

### Canvas vs WebGL2

| Package | Renderer | Best For |
|---|---|---|
| `@rive-app/canvas` | Canvas2D | Simpler graphics, smaller bundle |
| `@rive-app/webgl2` | Rive Renderer | Best quality, vector feathering, advanced blend modes |

**WebGL2 caveat**: Browser limits WebGL contexts. Use `useOffscreenRenderer: true` for many instances on one page.

**Chrome optimization**: Enable WEBGL_shader_pixel_local_storage extension for better performance.

### Lite Variants
`-lite` suffix (e.g., `@rive-app/canvas-lite`): Smaller footprint, no text, layout, audio, or scripting support.

### Single Variants
`-single` suffix: WASM bundled in JS. Larger bundle but fewer network requests.

## React Runtime

### Installation

```bash
npm install @rive-app/react-canvas
# or for WebGL2:
npm install @rive-app/react-webgl2
```

### useRive Hook

```jsx
import { useRive } from "@rive-app/react-canvas";

function MyComponent() {
  const { rive, RiveComponent } = useRive({
    src: "file.riv",
    stateMachines: "StateMachineName",
    autoplay: true,
  });

  return <RiveComponent />;
}
```

**Returns**:
- `rive`: Rive instance for programmatic control
- `RiveComponent`: React component to render

### Key Parameters
- `src`: URL or path to .riv file
- `stateMachines`: State machine name(s)
- `artboard`: Artboard name (optional)
- `autoplay`: Auto-start playback
- `layout`: Fit and alignment options

### Playback Control
```javascript
rive.play();
rive.pause();
rive.stop();
```

## State Machine Interaction (Both Web & React)

### Legacy Inputs (deprecated)
```javascript
const inputs = rive.stateMachineInputs("StateMachineName");
const boolInput = inputs.find((i) => i.name === "isHovered");
boolInput.value = true;
```

### Modern: Data Binding (View Models)
Use the runtime Data Binding API to get/set view model instance properties. See `runtimes/web/data-binding.mdx` and `runtimes/react/data-binding.mdx` for detailed API.

## Asset Loading

### Embedded (default)
Assets baked into the .riv file. Simple but larger file size.

### Out-of-Band
Load fonts, images, audio separately at runtime:
```javascript
new rive.Rive({
  src: "file.riv",
  assetLoader: (asset, bytes) => {
    // Return true if you handle loading this asset
    // Return false to use embedded fallback
  },
});
```

### Font Loading
Configure custom font loading for text-heavy animations. See `runtimes/web/text.mdx` for details.

### WASM Preloading
For performance, preload the WASM binary before creating Rive instances.

## Events

Listen for events reported from the state machine:
```javascript
const r = new rive.Rive({
  src: "file.riv",
  stateMachines: "SM",
  onRiveEvent: (event) => {
    console.log("Event:", event.data);
  },
});
```

## Low-Level API

For game-like applications with custom render loops, use the low-level WASM API directly. This gives full control over the update/draw cycle.

**For detailed API**: See `runtimes/web/` source docs.

## Common Patterns

1. **Resize handling**: Always call `resizeDrawingSurfaceToCanvas()` on window resize
2. **Memory cleanup**: Always call `.cleanup()` when removing Rive instances
3. **Multiple instances**: Use `useOffscreenRenderer: true` with WebGL2
4. **Caching**: Parse .riv once, reuse for multiple instances
5. **Lazy loading**: Load .riv files on demand, not all at page load
6. **Accessibility**: Respect `prefers-reduced-motion` — set `autoplay: false`
