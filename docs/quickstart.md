# Quickstart

Use this page if you are new to `rive-assistant` and want the shortest path from clone to a useful Rive answer.

## 1. Choose Your Tool

Open the setup page for the AI tool you use:

- [Codex](setup/codex.md)
- [Claude Code](setup/claude-code.md)
- [Gemini CLI](setup/gemini-cli.md)
- [Cursor](setup/cursor.md)
- [Windsurf](setup/windsurf.md)
- [GitHub Copilot](setup/github-copilot.md)

Each page tells you which context file the tool should load and how to confirm it is working.

## 2. Clone The Repo

For most users:

```bash
git clone https://github.com/isaganttus/rive-assistant.git
```

For offline use with the full upstream Rive docs submodule:

```bash
git clone --recurse-submodules https://github.com/isaganttus/rive-assistant.git
```

Open the cloned `rive-assistant` folder in your AI tool.

## 3. Ask The First Check Prompt

Ask:

```text
What Rive assistant instructions are you following in this repo? Name the local files you would use before answering a Rive question.
```

A working setup should mention the Rive expert assistant instructions and local files such as:

- [rive-reference/00-concept-map.md](../rive-reference/00-concept-map.md)
- [rive-reference/](../rive-reference/)
- [rive-recipes/](../rive-recipes/)

## 4. Try A Real Rive Question

Ask:

```text
How should I build a dynamic list in Rive and update it from React? Should I use Inputs?
```

A good answer should prefer Data Binding with View Models for new data-driven workflows, explain that Legacy Inputs are deprecated for that use case, and route through local references before giving exact runtime code.

## 5. Run The Smoke Test

Use [docs/smoke-testing.md](smoke-testing.md) for a 10-minute manual check across context loading, Data Binding guidance, runtime guidance, and scripting guidance.

## 6. Use Goal-Based Prompts

Use the prompts in [examples/prompts/](../examples/prompts/) when you want a repeatable starting point:

- [Confirm context loaded](../examples/prompts/confirm-context-loaded.md)
- [Build a dynamic UI](../examples/prompts/build-a-dynamic-ui.md)
- [Choose a runtime](../examples/prompts/choose-a-runtime.md)
- [Fix outdated Rive advice](../examples/prompts/fix-outdated-rive-advice.md)
- [Write a converter script](../examples/prompts/write-a-converter-script.md)

Use [examples/conversations/](../examples/conversations/) when you want to see what a good answer shape looks like.

## 7. If Something Feels Wrong

Open [docs/troubleshooting.md](troubleshooting.md) if the assistant gives generic answers, recommends deprecated Inputs, cannot fetch docs, or seems outdated.
