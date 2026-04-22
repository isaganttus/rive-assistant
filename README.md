# rive-assistant

A Rive expert assistant for AI models. Drop it into any AI coding environment to get a context-aware Rive co-pilot that can help you plan projects, write Luau scripts, navigate runtimes, and answer technical questions — always grounded in the official Rive documentation.

## What's included

- **`CLAUDE.md`** — System prompt / AI context file defining the assistant's role, Rive vocabulary, deprecation notices, and documentation routing rules
- **`rive-reference/`** — 11 curated reference files covering every Rive domain (editor, state machines, data binding, layouts, scripting, all runtimes, best practices)

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

The assistant will automatically use the local `rive-docs/` folder instead of fetching from GitHub.

To keep the local docs up to date:

```bash
git submodule update --remote
```

## Usage

### AI coding tools (Claude Code, Cursor, Windsurf, etc.)

Open the cloned folder as your working directory. The `CLAUDE.md` file is picked up automatically as project context.

### Other AI tools

Use the contents of `CLAUDE.md` as a system prompt, and make the `rive-reference/` files available to your tool as context or attachments.

## What the assistant covers

- **Editor** — Artboards, components, shapes, bones, meshes, constraints, text, solos
- **State Machines** — States, transitions, layers, listeners, blend states
- **Data Binding** — View models, bindings, converters, enums, lists
- **Layouts** — Responsive containers, Hug/Fill/Fixed sizing, N-slicing
- **Scripting** — Luau, all protocols, scripting API reference
- **Runtimes** — Web, React, React Native, Flutter, iOS, Android, Unity, Unreal, Defold
- **Best practices** — Performance, file organization, cross-platform patterns

## Contributing

The `rive-reference/` files are hand-curated summaries. If you find outdated information or missing coverage, PRs are welcome.
