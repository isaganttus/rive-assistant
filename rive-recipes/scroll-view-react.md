# Scroll View in React

**What this covers:** Building a vertical scroll view in Rive and controlling scroll position from React code.
**Rive features used:** Layouts, Scroll Constraint, view model (optional number property for scroll position).

## Editor setup

Build this layout hierarchy:

```
Scroll View (Layout — fixed width and height, e.g. 360×600)
  └─ Scroll Content (Layout + Scroll Constraint — Direction: Vertical, Physics: Elastic)
       ├─ Item 1 (Layout or Component)
       ├─ Item 2
       └─ Item N
```

1. Create the outer **Scroll View** layout: set to a fixed width and height (the visible viewport).
2. Inside, add **Scroll Content** layout: set height to **Hug** (grows to fit all items), same width as parent.
3. Add a **Scroll Constraint** to Scroll Content:
   - Direction: Vertical
   - Physics: Elastic (iOS-style deceleration + rubber banding) or Clamped (basic drag)
4. Add item layouts or Component instances inside Scroll Content.
5. Optional: bind `Scroll Percent Y` (0–100) to a view model number property to expose scroll position to code.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";

function ScrollFeed() {
  const { rive, RiveComponent } = useRive({
    src: "feed.riv",
    stateMachines: "FeedSM",
    autoplay: true,
  });

  const scrollToTop = () => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (vm) vm.number("scrollPercentY").value = 0;
  };

  return (
    <>
      <RiveComponent style={{ width: 360, height: 600 }} />
      <button onClick={scrollToTop}>Back to top</button>
    </>
  );
}
```

> Pointer/touch events are forwarded to the Rive instance automatically — user scrolling works without extra event wiring.

## Notes

- Rive handles scroll physics and pointer tracking natively — no JavaScript scroll event listeners needed.
- `Scroll Percent Y` (0 = top, 100 = bottom) is animatable and bindable to a view model number property.
- `Scroll Index` snaps to a specific item by 0-based index — useful for carousels and paginated lists.
- For large lists, enable **Virtualize** on the Artboard List inside the scroll content — only visible rows are rendered.
- **Carousel**: enable Virtualize + Carousel mode on the Artboard List for endless looping scroll.
- On web, set `touch-action: none` on the canvas if it conflicts with page scrolling.
