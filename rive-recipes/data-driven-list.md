# Data-Driven List

**What this covers:** A dynamically populated list in Rive driven by a view model List property, rendered via an Artboard List.
**Rive features used:** View model (List property), Artboard List, data binding, layouts.

## Editor setup

1. **Create the list item artboard** (e.g. `ListItem`, 360×64):
   - Add text/image objects for each field.
   - Create View Model `ItemVM` with string properties (e.g. `name`, `subtitle`).
   - Create an Exported View Model Instance `item`.
   - Bind text runs and image properties to `item.*`.

2. **Create the main artboard** (e.g. `FeedView`):
   - Add a Layout container (Hug width, fixed height).
   - Inside, add a child Layout with a **Scroll Constraint** (direction: Vertical).
   - Inside that, add an **Artboard List** component.
   - Set the Artboard List's artboard template to `ListItem`.

3. **Create the feed view model**:
   - Create View Model `FeedVM` with a **List** property `items`, typed to `ItemVM`.
   - Create an Exported View Model Instance `feed`.
   - Bind the Artboard List to `feed.items`.

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";
import { useEffect } from "react";

interface FeedItem { name: string; subtitle: string; }

function Feed({ items }: { items: FeedItem[] }) {
  const { rive, RiveComponent } = useRive({
    src: "feed.riv",
    stateMachines: "FeedSM",
    autoplay: true,
  });

  useEffect(() => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (!vm) return;

    const list = vm.list("items");

    // Remove all existing instances from the end to avoid index shifting
    while (list.length > 0) {
      list.removeInstanceAt(list.length - 1);
    }

    // Get the view model definition to create blank instances
    const itemViewModel = rive.viewModel("ItemVM");
    for (const item of items) {
      const instance = itemViewModel.instance();
      instance.string("name").value = item.name;
      instance.string("subtitle").value = item.subtitle;
      list.addInstance(instance);
    }
  }, [rive, items]);

  return <RiveComponent />;
}
```

**Updating a single item without rebuilding the list:**
```typescript
const list = vm.list("items");
const instance = list.instanceAt(2); // get item at index 2
instance.string("name").value = "Updated Name";
```

**Removing a specific item:**
```typescript
const list = vm.list("items");
list.removeInstanceAt(index);
// or, if you hold a reference to the instance:
list.removeInstance(instance);
```

**Reordering items:**
```typescript
const list = vm.list("items");
list.swap(0, 3); // swap items at index 0 and 3
```

## Notes

- Artboard Lists inherit layout properties (wrapping, gap, scroll) from their parent container.
- For large lists (100+ items), enable **Virtualize** on the Artboard List — only visible items are rendered.
- List instances are created from the view model definition (`rive.viewModel("ItemVM").instance()`) — each instance is independent.
- For incremental updates, use `list.instanceAt(index)` to update specific items rather than rebuilding the whole list.
- `list.length` gives the current count of instances in the list.
- To swap two items in place, use `list.swap(index1, index2)`.
