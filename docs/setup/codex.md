# Codex Setup

Codex reads [AGENTS.md](../../AGENTS.md) as the repo instruction file.

## Setup

1. Clone this repo.
2. Open the `rive-assistant` folder in Codex.
3. Start a new conversation from the repo root.

Codex should use the local [rive-reference/](../../rive-reference/) files first, then fetch official Rive docs pages when exact API signatures are needed and network access is available.

## Smoke test

Ask:

```text
What Rive assistant instructions are you following in this repo? Name the local files you would use before answering a Rive question.
```

Expected result: Codex mentions `AGENTS.md`, the Rive expert assistant role, [rive-reference/00-concept-map.md](../../rive-reference/00-concept-map.md), and local reference or recipe files.

## Troubleshooting

If Codex gives generic answers, confirm the working directory is the repo root and read [Troubleshooting](../troubleshooting.md).
