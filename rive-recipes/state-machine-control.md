# State Machine Control from Code

**What this covers:** Driving state machine transitions from runtime code using view model properties — the modern replacement for legacy Inputs.
**Rive features used:** State machine, view model (boolean + trigger properties), data binding.

## Editor setup

1. Create a **View Model** named `PlayerVM` with:
   - Boolean `isRunning`
   - Trigger `jump`
2. Create an **Exported View Model Instance**, name it `player`.
3. In the state machine, add transitions with conditions bound to these properties:
   - `Idle → Run`: condition `isRunning == true`
   - `Run → Idle`: condition `isRunning == false`
   - **Any State → Jump**: condition on `jump` trigger

## Runtime code

```typescript
import { useRive } from "@rive-app/react-canvas";
import { useEffect, useRef } from "react";

function Player() {
  const { rive, RiveComponent } = useRive({
    src: "player.riv",
    stateMachines: "PlayerSM",
    autoplay: true,
  });

  const vmRef = useRef<any>(null);

  useEffect(() => {
    if (rive) vmRef.current = rive.viewModelInstance;
  }, [rive]);

  const setRunning = (running: boolean) => {
    vmRef.current?.boolean("isRunning").value = running;
  };

  const jump = () => {
    vmRef.current?.trigger("jump").fire();
  };

  return (
    <>
      <RiveComponent />
      <button onMouseDown={() => setRunning(true)} onMouseUp={() => setRunning(false)}>Run</button>
      <button onClick={jump}>Jump</button>
    </>
  );
}
```

**Cross-platform pattern (all runtimes):**
- Boolean: `vm.boolean("name").value = true`
- Number: `vm.number("name").value = 42`
- String: `vm.string("name").value = "hello"`
- Trigger: `vm.trigger("name").fire()`

> **API note:** Verify exact method names against `runtimes/react/data-binding.mdx` and your platform's runtime docs.

## Notes

- **Do not use legacy Inputs** (`rive.stateMachineInputs()`). They are deprecated. Use view model properties instead.
- Triggers fire once then reset — use them for one-shot events (jump, attack). Use booleans for sustained states (running, hovered).
- View model properties can also be subscribed to: listen for change events instead of polling.
