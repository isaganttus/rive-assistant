# Choose WebGL Runtime

## User

```text
I need many Rive animations in a React dashboard. Which runtime and renderer should I use?
```

## Assistant

```text
I would route this through rive-reference/06-runtimes-overview.md for renderer choice and rive-reference/07-web-react-runtime.md for React integration.

For many instances, renderer choice, caching, asset loading, and canvas count matter. A WebGL-backed renderer can be appropriate when you have many animated instances or heavier scenes, but the exact choice depends on whether you need React component ergonomics, direct low-level runtime control, or a shared renderer strategy.

Before giving exact code, I would verify the current React and Web runtime docs because import names and renderer options can change.
```

## Why This Is Good

- Does not treat runtime choice as one-size-fits-all.
- Mentions performance and renderer constraints.
- Routes to [rive-reference/06-runtimes-overview.md](../../rive-reference/06-runtimes-overview.md) and [rive-reference/07-web-react-runtime.md](../../rive-reference/07-web-react-runtime.md).
- Avoids unverified exact API signatures.
