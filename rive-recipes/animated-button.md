# Animated Button (hover / press / disabled)

**What this covers:** A button artboard with idle, hover, pressed, and disabled visual states driven by a state machine, wired to pointer interaction via listeners.
**Rive features used:** State machine, animation states, transitions, listeners, view model (boolean properties).

## Editor setup

1. Create an artboard sized to your button (e.g. 200×56).
2. Create three timeline animations: `Idle`, `Hover`, `Pressed`. Animate fill/scale/shadow as needed.
3. Create a **View Model** named `ButtonVM` with boolean properties: `isHovered`, `isDisabled`, `isPressed`.
4. Create a **State Machine** named `ButtonSM`.
5. In the state machine graph, add animation states for `Idle`, `Hover`, `Pressed`.
6. Wire transitions:
   - `Idle → Hover`: condition `isHovered == true`
   - `Hover → Idle`: condition `isHovered == false`
   - `Hover → Pressed`: condition `isPressed == true`
   - `Pressed → Hover`: condition `isPressed == false`
   - **Any State → Idle**: condition `isDisabled == true` (connect from the Any State node)
7. Create an **Exported View Model Instance** from `ButtonVM`, name it `button`.
8. Add **Listeners** on the button shape:
   - Pointer Enter → View Model Change → `isHovered = true`
   - Pointer Exit → View Model Change → `isHovered = false`
   - Pointer Down → View Model Change → `isPressed = true`
   - Pointer Up → View Model Change → `isPressed = false`

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";
import { useEffect } from "react";

function Button({ disabled = false }: { disabled?: boolean }) {
  const { rive, RiveComponent } = useRive({
    src: "button.riv",
    stateMachines: "ButtonSM",
    autoplay: true,
  });

  useEffect(() => {
    if (!rive) return;
    const vm = rive.viewModelInstance;
    if (vm) {
      vm.boolean("isDisabled").value = disabled;
    }
  }, [rive, disabled]);

  return <RiveComponent style={{ width: 200, height: 56 }} />;
}
```

> **API note:** Verify `rive.viewModelInstance` and `.boolean(name).value` against `runtimes/react/data-binding.mdx`.

## Notes

- Pointer events (hover/press) are handled inside the .riv via Listeners — no JS event wiring needed.
- `isDisabled` is the only property driven from code; all interaction state is self-contained.
- The Any State → Idle transition ensures pressing a disabled button has no effect.
- For a non-React runtime, get the view model instance from your artboard or Rive object per that platform's API.
