# Fix Outdated Rive Advice

## User Goal

Check whether an older Rive tutorial or assistant answer is still safe to follow.

## Prompt

```text
I found an old Rive tutorial that uses Inputs to pass app data into a file. Is that still the right approach for a new project?
```

## Good Answer Should Mention

- Legacy Inputs are deprecated for new data-driven workflows.
- Data Binding with View Models is the modern approach for structured app data.
- State machines still matter for animation and interaction logic.
- The assistant should route through [rive-reference/03-data-binding.md](../../rive-reference/03-data-binding.md) and [rive-reference/02-state-machines-and-events.md](../../rive-reference/02-state-machines-and-events.md).
- Existing files may still contain Inputs, but new app data patterns should be reviewed before copying old examples.

## Red Flags

- Says Inputs are always the best way to pass app data.
- Treats deprecation guidance as optional or irrelevant.
- Does not mention Data Binding or View Models.
