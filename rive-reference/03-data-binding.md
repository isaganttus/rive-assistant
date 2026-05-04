# Rive Data Binding Reference
> Last verified: 2026-04-23

## Overview

Data Binding is Rive's modern reactive system using the **MVVM pattern** (Model-View-ViewModel). It creates a "contract" between designers and developers, decoupling design from code.

**This replaces legacy Inputs and Events for all new work.**

**Source docs**: `editor/data-binding/` and platform runtime data binding pages such as `runtimes/web/data-binding.mdx` and `runtimes/react/data-binding.mdx`

## Core Entities

- **View Model**: Blueprint/class for a collection of related data. Template without concrete values.
- **View Model Property**: Individual field within a view model. Has a type and name. Can be bound to multiple editor elements.
- **View Model Instance**: Living object with actual values (like a class instance). Each instance can have different initial values. Must be marked **"Exported"** to be visible to runtime developers.
- **Binding**: Association between a property and an editor element.
- **Converter**: Transforms data between types in a binding (e.g., number to string, add operation).
- **Enumeration (Enum)**: Fixed set of named options. System enums (editor-defined) or user-defined.

## Supported Property Types

- Floating point numbers
- Booleans
- Triggers
- Strings
- Enumerations (Enums)
- Colors
- View Model Nesting (view models as properties of other view models)
- Lists
- Images
- Artboards

Legacy Inputs do NOT support: strings, enums, colors, nesting, lists, images, artboards, or triggers in the same way.

## Binding Directions

| Direction | Behavior |
|---|---|
| **Source-to-Target** (default) | Property changes update the editor element |
| **Target-to-Source** | Element changes update the property |
| **Bidirectional** | Changes flow both ways |
| **Bind Once** | Initial value applies, then binding disconnects |

## Advantages Over Legacy Systems

**vs. Inputs**:
- Can drive most editor elements, not just state machine transitions
- Support both polling AND listening APIs at runtime
- Can be converted before use
- Support blend states (1D and Additive) as mix parameters
- Can be receivers for listeners

**vs. Events**:
- Richer data channel for developers
- Can be changed from multiple sources
- Property values carry most recent data
- Better for internal reactivity through listeners
- **Audio**: Audio Events (legacy) still handle sound triggering from timelines/transitions/listeners. Audio can also be triggered via scripting using the `Audio` global API.

## View Model Nesting

View models can have other view models as properties, enabling:
- Component-like data architecture
- Reusable data patterns across artboards
- Nested data access in scripts: `self.character.health.value`

## Lists

Lists dynamically generate items at runtime based on bound data.

### Artboard Lists
- Must be children of artboard or layout
- Inherit layout properties from parent (direction, wrapping, padding, gap, alignment)
- Support scrolling if parent layout has Scroll Constraint

### Two ways to populate:

**1. View Model List Property** (more flexible):
- Each list item = a View Model instance
- Create list item view model, bind to artboard template
- Create main view model with List property
- Bind list property to Artboard List

**2. Number-to-List Converter** (simpler for fixed count):
- Number property specifies count
- Converter transforms number to artboard instances

### List Item Index
- Special property providing item position (0-based)
- Added via "List Attributes > Index"
- Can be bound to properties, used in converters, or in state machine conditions

## Converters

General-purpose data transformation in bindings:
- Type conversion (number to string, color to number, etc.)
- Operations (add, multiply, concatenate)
- Custom logic via Converter Scripts (Luau)

Created in Data Panel > Converters.

## Runtime APIs

All runtimes provide APIs for:
- Reading view model instance properties
- Updating property values
- Subscribing to property change notifications
- Working with lists (add, remove, update items)
- Enumerating available properties

**For platform-specific API details**: See the data binding page for your runtime, such as `runtimes/web/data-binding.mdx`, `runtimes/react/data-binding.mdx`, `runtimes/flutter/data-binding.mdx`, `runtimes/apple/data-binding.mdx`, `runtimes/android/data-binding.mdx`, or `runtimes/react-native/data-binding.mdx`.

## Best Practices

1. **Use data binding for all new projects** — don't use legacy inputs/events
2. **Plan migration** from inputs/events in existing projects
3. **Exported instances** are the developer contract — mark them explicitly
4. **One view model per artboard** as default pattern
5. **Nested view models** for reusable components
6. **Listeners** are the preferred in-editor method for user interaction (trigger view model changes)
7. **Converters** enable complex operations without code
8. **View model nesting** unifies several complex patterns (nested inputs, nested text, event bubbling)
