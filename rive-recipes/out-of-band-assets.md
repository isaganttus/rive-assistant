# Out-of-Band Asset Loading

**What this covers:** Loading images and fonts separately from the .riv file to reduce bundle size and enable asset reuse or dynamic swapping.
**Rive features used:** Asset loading, `assetLoader` callback.

## Editor setup

1. Import your image or font into the Rive file as usual.
2. In the Assets panel, select the asset.
3. In the Inspector under **Export Options**, set the asset to **Referenced** (not embedded). This strips it from the .riv.
4. Note the asset's **name** — you will match by name at runtime.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";

const { RiveComponent } = useRive({
  src: "file.riv",
  stateMachines: "SM",
  autoplay: true,
  assetLoader: (asset, bytes) => {
    if (asset.isImage && asset.name === "hero-image") {
      fetch("/images/hero.webp")
        .then((res) => res.arrayBuffer())
        .then((buf) => asset.decode(new Uint8Array(buf)));
      return true; // we handle this asset
    }
    if (asset.isFont && asset.name === "Inter") {
      fetch("/fonts/Inter.ttf")
        .then((res) => res.arrayBuffer())
        .then((buf) => asset.decode(new Uint8Array(buf)));
      return true;
    }
    return false; // use embedded fallback
  },
});
```

**Swapping an asset after load:**
```javascript
const imageAsset = rive.assets.find((a) => a.name === "hero-image");
fetch("/images/hero-v2.webp")
  .then((res) => res.arrayBuffer())
  .then((buf) => imageAsset.decode(new Uint8Array(buf)));
```

> **API note:** Verify `asset.decode()`, `rive.assets`, and `assetLoader` signature against `runtimes/web/loading-assets.mdx` and `runtimes/web/web-js.mdx`.

## Notes

- **Referenced vs Embedded**: Referenced = stripped from .riv, must be provided at runtime. Embedded = baked in (default).
- `assetLoader` fires synchronously during initialization — start the fetch immediately and call `asset.decode()` when data arrives.
- Out-of-band assets can be shared across multiple .riv files.
- For locale swapping (different images per region), use `asset.name` and locale to pick the correct file.
- Flutter, iOS, Android, Unity, and Unreal all have equivalent asset loader APIs. See platform runtime docs.
