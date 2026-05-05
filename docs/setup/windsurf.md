# Windsurf Setup

Windsurf reads [.windsurfrules](../../.windsurfrules) from the repo root.

## Setup

1. Clone this repo.
2. Open the `rive-assistant` folder in Windsurf.
3. Confirm `.windsurfrules` is visible at the workspace root.

Windsurf should use local context from [rive-reference/](../../rive-reference/) and [rive-recipes/](../../rive-recipes/). It is not expected to fetch official docs automatically from the context file; paste source docs into the chat when exact API details are required.

## Smoke test

Ask:

```text
How should I check whether Legacy Inputs are still the right approach for a new Rive data workflow?
```

Expected result: Windsurf says Legacy Inputs are deprecated for new data-driven workflows and routes to [rive-reference/03-data-binding.md](../../rive-reference/03-data-binding.md).

## Troubleshooting

If Windsurf gives generic answers, confirm `.windsurfrules` is in the workspace root and read [Troubleshooting](../troubleshooting.md).
