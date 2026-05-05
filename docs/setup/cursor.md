# Cursor Setup

Cursor reads [.cursor/rules/rive.mdc](../../.cursor/rules/rive.mdc).

## Setup

1. Clone this repo.
2. Open the `rive-assistant` folder in Cursor.
3. Confirm the `.cursor/rules/rive.mdc` rule is present and applies to the workspace.

Cursor should use local context from [rive-reference/](../../rive-reference/) and [rive-recipes/](../../rive-recipes/). It is not expected to fetch official docs automatically from the context file; paste source docs into the chat when you need exact API details.

## Smoke test

Ask:

```text
What Rive files in this workspace should you read before answering questions about Data Binding?
```

Expected result: Cursor mentions `.cursor/rules/rive.mdc`, [rive-reference/00-concept-map.md](../../rive-reference/00-concept-map.md), and [rive-reference/03-data-binding.md](../../rive-reference/03-data-binding.md).

## Troubleshooting

If Cursor does not seem to load the rule, confirm the folder is opened as the workspace root and read [Troubleshooting](../troubleshooting.md).
