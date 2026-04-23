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
  context: Context,
}

-- Called once when the script initializes.
-- Store context to access the main view model and other data.
function init(self: ComboReadyCondition, context: Context): boolean
  self.context = context
  return true
end

-- Runs every frame while the transition is a candidate.
-- Return true to allow the transition, false to block it.
function evaluate(self: ComboReadyCondition): boolean
  local vm = self.context:viewModel()
  if vm == nil then return false end

  local pressCount = vm:number("pressCount")
  return pressCount ~= nil and pressCount:get() >= 3
end

return function(): TransitionCondition<ComboReadyCondition>
  return {
    init = init,
    evaluate = evaluate,
    context = late(),  -- late() defers initialization; Rive fills this in at runtime
  }
end
```

> **API note:** `context = late()` in the return table is required — Rive uses it to inject the context before `init` runs. Verify `context:viewModel()` and `vm:number()` against `scripting/data-binding.mdx` and `scripting/protocols/transition-condition-scripts.mdx`.

## Notes

- `evaluate()` runs every frame while the transition is active — keep it fast and side-effect free. Never call audio, update state, or make external calls from here.
- Multiple Transition Condition scripts on one transition create AND logic — all must return `true`.
- For OR logic, add multiple transitions between the same states.
- To pass editor-configured values into the condition without changing script logic, use Script Inputs — bind them to view model properties or set them per-transition in the inspector.
- Source docs: `scripting/protocols/transition-condition-scripts.mdx`, `scripting/script-inputs.mdx`
