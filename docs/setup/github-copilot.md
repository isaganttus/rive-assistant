# GitHub Copilot Setup

GitHub Copilot reads [.github/copilot-instructions.md](../../.github/copilot-instructions.md) when repository custom instructions are enabled.

## Setup

1. Clone this repo.
2. Open the `rive-assistant` folder in an editor with GitHub Copilot Chat.
3. Confirm repository custom instructions are enabled for the workspace.

Copilot should use local context from [rive-reference/](../../rive-reference/) and [rive-recipes/](../../rive-recipes/). It is not expected to fetch official docs automatically from the context file; paste source docs into the chat when exact API details are required.

## Smoke test

Ask:

```text
What local Rive references should you use before answering a question about React runtime integration?
```

Expected result: Copilot mentions `.github/copilot-instructions.md`, [rive-reference/00-concept-map.md](../../rive-reference/00-concept-map.md), and [rive-reference/07-web-react-runtime.md](../../rive-reference/07-web-react-runtime.md).

## Troubleshooting

If Copilot does not seem to load repository instructions, confirm custom instructions are enabled and read [Troubleshooting](../troubleshooting.md).
