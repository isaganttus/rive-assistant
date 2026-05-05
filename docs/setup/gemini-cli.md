# Gemini CLI Setup

Gemini CLI reads [GEMINI.md](../../GEMINI.md) as the repo context file.

## Setup

1. Clone this repo.
2. Start Gemini CLI from the `rive-assistant` repo root.
3. Confirm Gemini can read `GEMINI.md`, [rive-reference/](../../rive-reference/), and [rive-recipes/](../../rive-recipes/).

Gemini CLI should use the local concept map first and fetch official Rive docs pages when exact API signatures are needed.

## Smoke test

Ask:

```text
Which local files should you consult before answering a Rive runtime question?
```

Expected result: Gemini CLI mentions `GEMINI.md`, [rive-reference/00-concept-map.md](../../rive-reference/00-concept-map.md), [rive-reference/06-runtimes-overview.md](../../rive-reference/06-runtimes-overview.md), and the platform-specific runtime reference.

## Troubleshooting

If Gemini CLI gives generic answers, restart it from the repo root and read [Troubleshooting](../troubleshooting.md).
