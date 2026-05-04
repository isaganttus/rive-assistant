# rive-assistant

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Last commit](https://img.shields.io/github/last-commit/isaganttus/rive-assistant)](https://github.com/isaganttus/rive-assistant/commits/main)
[![Sync docs paths](https://github.com/isaganttus/rive-assistant/actions/workflows/sync-docs-paths.yml/badge.svg)](https://github.com/isaganttus/rive-assistant/actions/workflows/sync-docs-paths.yml)
[![Validate docs references](https://github.com/isaganttus/rive-assistant/actions/workflows/validate-doc-paths.yml/badge.svg)](https://github.com/isaganttus/rive-assistant/actions/workflows/validate-doc-paths.yml)

A Rive expert assistant for AI models. Drop it into any AI coding environment to get a context-aware Rive co-pilot that can help you plan projects, write Luau scripts, navigate runtimes, and answer technical questions — always grounded in the official Rive documentation.

## What's included

- **`CLAUDE.md`** — System prompt / AI context file defining the assistant's role, Rive vocabulary, deprecation notices, and documentation routing rules
- **`rive-reference/`** — 11 curated reference files covering every Rive domain (editor, state machines, data binding, layouts, scripting, all runtimes, best practices)
- **`rive-recipes/`** — 10 code-first recipes for common Rive tasks
- **`GEMINI.md`, `.cursor/rules/rive.mdc`, `.windsurfrules`, `.github/copilot-instructions.md`** — Native context files for Gemini CLI, Cursor, Windsurf, and GitHub Copilot

The curated reference files handle the majority of questions. When exact API signatures are needed, the assistant fetches the relevant page directly from the [official Rive docs repository](https://github.com/rive-app/rive-docs) on GitHub.

## Setup

### Default — fetch on demand (recommended)

Clone the repo and point your AI tool at it. No extra steps needed.

```bash
git clone https://github.com/isaganttus/rive-assistant.git
```

The assistant will fetch official docs pages from GitHub as needed. Requires internet access during sessions.

### Offline — local docs

If you want the full docs available locally (faster lookups, works without internet), clone with the submodule:

```bash
git clone --recurse-submodules https://github.com/isaganttus/rive-assistant.git
```

The assistant will use the local `rive-docs/` folder instead of fetching from GitHub when the submodule is initialized and `rive-docs/docs.json` exists.

To keep the local docs up to date:

```bash
git submodule update --remote
```

## Usage

Open the cloned folder as your working directory. Each supported tool picks up its context file automatically — no extra configuration needed.

| Tool | Context file | Notes |
|---|---|---|
| **Claude Code** | `CLAUDE.md` | Auto-loaded. Supports remote docs fetching. |
| **Gemini CLI** | `GEMINI.md` | Auto-loaded. Supports remote docs fetching. |
| **Cursor** | `.cursor/rules/rive.mdc` | Auto-loaded (`alwaysApply: true`). |
| **Windsurf** | `.windsurfrules` | Auto-loaded from project root. |
| **GitHub Copilot** | `.github/copilot-instructions.md` | Auto-loaded for Copilot Chat. |

**Claude Code and Gemini CLI** fetch official documentation pages on demand for exact API signatures. **Cursor, Windsurf, and Copilot** use the local `rive-reference/` files only — for exact API details, paste the relevant page from [rive-app/rive-docs](https://github.com/rive-app/rive-docs) into the conversation.

### Other tools

Copy the contents of `CLAUDE.md` as a system prompt and make the `rive-reference/` directory available as context or attachments.

## What the assistant covers

- **Editor** — Artboards, components, shapes, bones, meshes, constraints, text, solos
- **State Machines** — States, transitions, layers, listeners, blend states
- **Data Binding** — View models, bindings, converters, enums, lists
- **Layouts** — Responsive containers, Hug/Fill/Fixed sizing, N-slicing
- **Scripting** — Luau, all protocols, scripting API reference
- **Runtimes** — Web, React, React Native, Flutter, iOS, Android, Unity, Unreal, Defold
- **Best practices** — Performance, file organization, cross-platform patterns

## Staying up to date

The concept map in `rive-reference/00-concept-map.md` is kept in sync with the official Rive docs structure. When the Rive team reorganizes their docs, this repo gets updated automatically via a weekly check.

To get the latest version, run `git pull` in your `rive-assistant` folder. Check the [Releases](../../releases) tab on GitHub for a summary of what changed in each update. If the assistant starts warning you that docs paths can't be found, that's a sign it's time to pull.

**Watch this repo on GitHub** to get notified when updates are pushed — click the Watch button and choose "All activity" or "Releases only".

## Contributing

The `rive-reference/` files are hand-curated summaries. If you find outdated information or missing coverage, PRs are welcome. See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

Please note that this project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold it.
