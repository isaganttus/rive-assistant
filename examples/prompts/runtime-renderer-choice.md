# Runtime Renderer Choice

## Prompt

```text
Which Rive runtime should I use for many WebGL-backed animations in a React app, and what should you verify before giving code?
```

## Good Answer Should Mention

- The answer should compare Web and React runtime concerns.
- Renderer choice matters for many instances and performance-sensitive canvases.
- The assistant should route through [rive-reference/06-runtimes-overview.md](../../rive-reference/06-runtimes-overview.md) and [rive-reference/07-web-react-runtime.md](../../rive-reference/07-web-react-runtime.md).
- Exact API signatures should be verified against current Rive runtime docs before final code.
- Performance guidance should include caching, instance count, renderer choice, and asset-loading tradeoffs when relevant.

## Red Flags

- Treats renderer choice as irrelevant.
- Gives one-size-fits-all runtime advice without asking about instance count, environment, or renderer constraints.
- Provides exact imports and API calls without checking current source docs.
