# Convert Legacy Inputs

## User

```text
I found an old Rive tutorial that uses Inputs to pass user profile data into an animation. Should I copy that pattern?
```

## Assistant

```text
For new user profile data, I would not copy that pattern directly. Legacy Inputs are deprecated for new data-driven workflows. Start with Data Binding and View Models instead.

I would check rive-reference/03-data-binding.md for View Models and binding concepts, then use rive-reference/02-state-machines-and-events.md only for interaction or animation state that still belongs in a state machine.

Inputs may still appear in older files or state-machine-control examples, but for structured app data like profile name, plan, avatar state, or list items, model the data with Data Binding.
```

## Why This Is Good

- Directly calls out deprecated Inputs.
- Routes user profile data to [rive-reference/03-data-binding.md](../../rive-reference/03-data-binding.md).
- Keeps state machines for animation and interaction logic instead of app data modeling.
