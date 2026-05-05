# Scripting Converter

## Prompt

```text
Write a Luau converter script approach for formatting a number as currency in Rive. What source should you verify first?
```

## Good Answer Should Mention

- Converter scripts are the relevant Rive scripting protocol.
- Luau is the scripting language.
- The assistant should route through [rive-reference/05-scripting.md](../../rive-reference/05-scripting.md) and [rive-recipes/custom-converter.md](../../rive-recipes/custom-converter.md).
- Exact converter script API signatures should be verified against current source docs.
- The answer should describe the conversion behavior before producing final code.

## Red Flags

- Uses JavaScript instead of Luau for the Rive script itself.
- Confuses converter scripts with transition condition, node, layout, or listener action scripts.
- Gives final API syntax without source verification.
