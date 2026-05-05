# Smoke Testing

Use this guide after cloning `rive-assistant` or after changing a tool context file. The goal is to confirm that your AI tool loaded the Rive assistant instructions and is giving modern, source-aware Rive guidance.

This is a manual smoke test, not a benchmark. A good run takes about 10 minutes.

## Before You Start

Open this repository as the working folder in your AI tool. The tool should be able to read the repo files listed below:

- Codex: [AGENTS.md](../AGENTS.md)
- Claude Code: [CLAUDE.md](../CLAUDE.md)
- Gemini CLI: [GEMINI.md](../GEMINI.md)
- Cursor: [.cursor/rules/rive.mdc](../.cursor/rules/rive.mdc)
- Windsurf: [.windsurfrules](../.windsurfrules)
- GitHub Copilot: [.github/copilot-instructions.md](../.github/copilot-instructions.md)

Codex, Claude Code, and Gemini CLI are expected to fetch official Rive docs pages when exact API signatures are needed. Cursor, Windsurf, and GitHub Copilot should use the local [rive-reference/](../rive-reference/) files unless you paste official docs content into the chat.

## Tool Loading Checks

Run the first prompt in the tool you are testing:

```text
What Rive assistant instructions are you following in this repo? Name the local files you would use before answering a Rive question.
```

Expected answer:

- Mentions that it is acting as a Rive expert assistant.
- Mentions local references such as [rive-reference/00-concept-map.md](../rive-reference/00-concept-map.md), [rive-reference/](../rive-reference/), and [rive-recipes/](../rive-recipes/).
- Does not claim this is an official Rive project.
- Does not treat the repo as a runtime package, app template, or `.riv` asset library.

Red flags:

- The answer is generic and does not mention Rive.
- The answer cannot name any local files.
- The answer claims it has broad product support for every Rive domain.

## Rive Guidance Checks

Run these prompts one by one. You do not need perfect answers. You are checking that the assistant routes to the right concepts and avoids risky old guidance.

### 1. Concept Routing

```text
I need to build a responsive Rive UI with dynamic data and state machine logic. Which local reference files should you consult first?
```

Expected answer:

- Starts with [rive-reference/00-concept-map.md](../rive-reference/00-concept-map.md) or uses it as the routing table.
- Routes responsive UI to [rive-reference/04-layouts.md](../rive-reference/04-layouts.md).
- Routes dynamic data to [rive-reference/03-data-binding.md](../rive-reference/03-data-binding.md).
- Routes state machine logic to [rive-reference/02-state-machines-and-events.md](../rive-reference/02-state-machines-and-events.md).

### 2. Modern Data Guidance

```text
How should I make a dynamic list in Rive and update it from React? Should I use Inputs?
```

Expected answer:

- Recommends Data Binding with View Models for dynamic data.
- Explains that Legacy Inputs are deprecated for new data-driven workflows.
- Mentions lists and runtime binding concepts before reaching for state machine inputs.
- Uses [rive-reference/03-data-binding.md](../rive-reference/03-data-binding.md), [rive-reference/07-web-react-runtime.md](../rive-reference/07-web-react-runtime.md), or [rive-recipes/data-driven-list.md](../rive-recipes/data-driven-list.md).

Red flags:

- Recommends Legacy Inputs as the default data path.
- Ignores View Models.
- Gives exact React API signatures without saying they should be verified against current source docs.

### 3. Runtime Accuracy

```text
Which Rive runtime should I use for many WebGL-backed animations in a React app, and what should you verify before giving code?
```

Expected answer:

- Discusses Web and React runtime choices.
- Mentions renderer choice and performance tradeoffs.
- Says exact API signatures should be verified against current source docs before giving implementation code.
- Uses [rive-reference/06-runtimes-overview.md](../rive-reference/06-runtimes-overview.md) and [rive-reference/07-web-react-runtime.md](../rive-reference/07-web-react-runtime.md).

### 4. Scripting Safety

```text
Write a Luau converter script approach for formatting a number as currency in Rive. What source should you verify first?
```

Expected answer:

- Identifies converter scripts as the relevant scripting protocol.
- Mentions Luau and the converter protocol shape.
- Routes through [rive-reference/05-scripting.md](../rive-reference/05-scripting.md) or [rive-recipes/custom-converter.md](../rive-recipes/custom-converter.md).
- Says exact script APIs should be checked against current source docs before final code.

## Prompt Examples

Use the examples in [examples/prompts/](../examples/prompts/) for repeatable manual checks:

- [Context loaded](../examples/prompts/context-loaded.md)
- [Data Binding list in React](../examples/prompts/data-binding-list-react.md)
- [Runtime renderer choice](../examples/prompts/runtime-renderer-choice.md)
- [Scripting converter](../examples/prompts/scripting-converter.md)

Each example includes the prompt, what a good answer should mention, and red flags to watch for.

## Passing Criteria

Treat the setup as working when the assistant:

- Knows it is a Rive expert assistant.
- Uses the local concept map and reference files before answering.
- Prefers Data Binding with View Models over Legacy Inputs for new data-driven workflows.
- Distinguishes local summary guidance from exact API signatures that need current source verification.
- Avoids claiming official Rive ownership or unsupported product coverage.

If one tool fails but another passes, check that tool's context file is actually loaded by the editor or CLI. If all tools fail, run the repository validation commands from [CONTRIBUTING.md](../CONTRIBUTING.md) and inspect recent changes to the shared context files.
