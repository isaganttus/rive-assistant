# Custom Transition Condition Script

**What this covers:** A Luau Transition Condition script controlling when a state machine transition fires using custom logic.
**Rive features used:** Scripting (TransitionCondition protocol), state machine transitions.

## When to use

Use when:
- The condition combines multiple values with logic that built-in conditions can't express
- You need time-based or counter-based transitions

For simple conditions (boolean equals, number threshold), bind a view model property directly — no script needed.

## Editor setup

1. Create a **Script** asset: Assets Panel → + → Script → **Transition Condition Script** protocol. Name it `ComboReadyCondition`.
2. In the state machine, select the target transition.
3. In the transition inspector, click **+** to add a new Condition → **Script** → select `ComboReadyCondition`.

## Script

```lua
-- ComboReadyCondition.lua
type ComboReadyCondition = {
  vm: ViewModel?,
}

function init(self: ComboReadyCondition, context: Context): boolean
  self.vm = context:viewModel()
  return self.vm ~= nil
end

function evaluate(self: ComboReadyCondition): boolean
  local vm = self.vm
  if vm == nil then
    return false
  end

  local pressCount = vm:getNumber("pressCount")
  if pressCount == nil then
    return false
  end

  return pressCount.value >= 3
end

return function(): TransitionCondition<ComboReadyCondition>
  return {
    init = init,
    evaluate = evaluate,
    vm = nil,
  }
end
```

> **API note:** Rive passes `Context` to `init(self, context)`. Store values you need later on `self`; do not add a synthetic returned-table context field initialized with `late()`. ViewModel scalar properties are read through `vm:getNumber("name")` and `.value`.

## Notes

- `evaluate()` runs every frame while the transition is active — keep it fast and side-effect free. Never call audio, update state, or make external calls from here.
- Multiple Transition Condition scripts on one transition create AND logic — all must return `true`.
- For OR logic, add multiple transitions between the same states.
- To pass editor-configured values into the condition without changing script logic, use Script Inputs — bind them to view model properties or set them per-transition in the inspector.
- Source docs: `scripting/protocols/transition-condition-scripts.mdx`, `scripting/script-inputs.mdx`
