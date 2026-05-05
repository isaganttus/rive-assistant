# Luau Currency Converter

## User

```text
Can you write a Rive script that formats a number as USD currency?
```

## Assistant

```text
This sounds like a converter script, so I would start with rive-reference/05-scripting.md and the custom converter recipe in rive-recipes/custom-converter.md.

The answer should describe the converter behavior first: accept a numeric value, format it as a currency string, and return that value for display through Data Binding.

Before giving final code, I would verify the current converter script protocol in the official Rive scripting docs, because exact Luau function names and signatures should match the current API.
```

## Why This Is Good

- Identifies converter scripts as the right protocol.
- Mentions Luau and Data Binding context.
- Routes through [rive-reference/05-scripting.md](../../rive-reference/05-scripting.md) and [rive-recipes/custom-converter.md](../../rive-recipes/custom-converter.md).
- Avoids final code until exact source docs are verified.
