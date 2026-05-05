# Dynamic Rive List In React

## User

```text
I have a Rive file with a card component and want to render a list of product cards from React data. Should I use Inputs for each card?
```

## Assistant

```text
For a new data-driven list, start with Data Binding and View Models rather than Legacy Inputs.

I would first consult rive-reference/00-concept-map.md, then rive-reference/03-data-binding.md for lists and View Models, and rive-reference/07-web-react-runtime.md for React runtime concerns. The recipe in rive-recipes/data-driven-list.md is also a good starting point.

At a high level:

1. Model the repeated card data as a View Model in the Rive file.
2. Use a list-style binding for repeated items instead of separate state machine inputs for every field.
3. Keep state machines for interaction and animation logic.
4. Verify the current React runtime Data Binding API before writing exact imports or method calls.
```

## Why This Is Good

- Starts from Data Binding with View Models.
- Does not recommend Legacy Inputs for new dynamic UI.
- Separates data flow from state machine animation logic.
- Names relevant local files in [rive-reference/](../../rive-reference/) and [rive-recipes/](../../rive-recipes/).
