# Troubleshooting

Use this page when the assistant does not behave like a Rive-aware assistant after you clone the repo.

## The Assistant Gives Generic Answers

Symptoms:

- It gives generic answers about animation or design.
- It does not mention Rive.
- It cannot name local files such as [rive-reference/00-concept-map.md](../rive-reference/00-concept-map.md).

Try:

1. Open the `rive-assistant` repo folder as the workspace root.
2. Ask the context check prompt from [docs/quickstart.md](quickstart.md).
3. Check your tool-specific setup page in [docs/setup/](setup/).
4. Restart the conversation after opening the correct folder.

## The Assistant Recommends Deprecated Inputs

Symptoms:

- It tells you to use deprecated Inputs for a new data-driven workflow.
- It ignores Data Binding and View Models.
- It treats state machine inputs as the default way to pass app data into Rive.

Try:

1. Ask it to consult [rive-reference/03-data-binding.md](../rive-reference/03-data-binding.md).
2. Mention that the workflow is new and data-driven.
3. Ask it to explain when Legacy Inputs are deprecated and when state machine control may still matter.

For new dynamic UI, a good answer should start from Data Binding with View Models.

## The Assistant Cannot Fetch Source Docs

Symptoms:

- It says it cannot fetch official docs.
- It gives only local summary guidance.
- It avoids exact API signatures.

Try:

1. Check whether your AI tool has network access.
2. If network access is unavailable, paste the relevant official Rive docs page into the chat.
3. For offline use, clone with the submodule:

```bash
git clone --recurse-submodules https://github.com/isaganttus/rive-assistant.git
```

The local references are useful for planning and routing, but exact API signatures should be checked against current source docs when possible.

## The Tool Does Not Seem To Load Instructions

Symptoms:

- Cursor, Windsurf, or GitHub Copilot does not seem to load custom instructions.
- The assistant does not mention the expected context file.
- The first smoke test fails.

Try:

1. Confirm the expected context file exists:
   - Codex: [AGENTS.md](../AGENTS.md)
   - Claude Code: [CLAUDE.md](../CLAUDE.md)
   - Gemini CLI: [GEMINI.md](../GEMINI.md)
   - Cursor: [.cursor/rules/rive.mdc](../.cursor/rules/rive.mdc)
   - Windsurf: [.windsurfrules](../.windsurfrules)
   - GitHub Copilot: [.github/copilot-instructions.md](../.github/copilot-instructions.md)
2. Open the repo root, not a parent folder or nested subfolder.
3. Start a new chat after opening the correct folder.

## The Local Repo Looks Outdated

Symptoms:

- The assistant warns that docs paths cannot be found.
- It gives guidance that seems outdated compared with current Rive docs.
- GitHub shows newer releases or commits.

Try:

```bash
git pull
```

If you cloned with the Rive docs submodule:

```bash
git submodule update --remote
```

Use `main` for the freshest docs tracking, or use GitHub releases when you want a stable snapshot.

## The Answer Is Too Confident About Code

Symptoms:

- It gives exact imports, method names, or script signatures without source verification.
- It does not distinguish local summary guidance from current API details.

Try:

Ask:

```text
Which local reference are you using, and which official Rive source doc would you verify before final code?
```

A good answer should name the local reference file and the official source path it would verify.
