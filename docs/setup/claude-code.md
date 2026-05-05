# Claude Code Setup

Claude Code reads [CLAUDE.md](../../CLAUDE.md) as the repo context file.

## Setup

1. Clone this repo.
2. Open the `rive-assistant` folder in Claude Code.
3. Start from the repo root so Claude Code can see `CLAUDE.md`, [rive-reference/](../../rive-reference/), and [rive-recipes/](../../rive-recipes/).

Claude Code should use local summaries first and fetch official Rive docs pages when exact API signatures are needed.

## Smoke test

Ask:

```text
How should I make a dynamic list in Rive and update it from React? Should I use Inputs?
```

Expected result: Claude Code recommends Data Binding with View Models, treats Legacy Inputs as deprecated for new data-driven workflows, and routes through local Rive references.

## Troubleshooting

If Claude Code does not seem to load `CLAUDE.md`, restart the conversation from the repo root and read [Troubleshooting](../troubleshooting.md).
