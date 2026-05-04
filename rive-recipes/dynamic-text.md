# Dynamic Text via Data Binding

**What this covers:** Binding a text object's content to a view model string property so it can be updated from code at runtime.
**Rive features used:** Text, view model (string property), data binding.

## Editor setup

1. Add a **Text** object to your artboard.
2. In the Data panel, create a **View Model** named `CardVM` with a string property `title` (default: `"Placeholder"`).
3. Create an **Exported View Model Instance**, name it `card`.
4. Select the Text object. In the Inspector, find the **Text Run** (usually named `run`).
5. Click the binding icon next to the text run value. Bind to `card.title` (source-to-target direction).

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";
import { useEffect } from "react";

function Card({ title }: { title: string }) {
  const { rive, RiveComponent } = useRive({
    src: "card.riv",
    stateMachines: "CardSM",
    autoplay: true,
  });

  useEffect(() => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (vm) {
      vm.string("title").value = title;
    }
  }, [rive, title]);

  return <RiveComponent />;
}
```

**Web JS (no React):**
```javascript
const r = new rive.Rive({
  src: "card.riv",
  canvas: document.getElementById("canvas"),
  stateMachines: "CardSM",
  autoplay: true,
  onLoad: () => {
    r.resizeDrawingSurfaceToCanvas();
    r.viewModelInstance.string("title").value = "Hello World";
  },
});
```

> **API note:** Verify `viewModelInstance`, `.string(name).value` against `runtimes/react/data-binding.mdx`.

## Notes

- The binding updates on the next render frame — changes take effect immediately on the next animation tick.
- For multiple text runs (title + subtitle), add multiple string properties to the view model.
- For formatted numbers, use a **Converter** (number → string) instead of a raw string property. See `custom-converter` recipe.
- Check the hierarchy panel for the exact Text Run name if multiple runs exist.
