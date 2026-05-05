# Rive State Machines & Events Reference
> Last verified: 2026-04-23
> Source docs: `editor/state-machine/`, `editor/events/`, `editor/animate-mode/`

## Overview

State Machines are visual systems connecting animations with logic-driven transitions. They are the primary mechanism for interactive, developer-ready motion graphics.

## Architecture

- **Graph**: Visual space for states and transitions (replaces timeline when SM selected)
- **States**: Animation nodes that can play
- **Transitions**: Logic connections between states with conditions and timing
- **Layers**: Parallel animation tracks; rightmost layer has priority
- **Listeners**: In-editor interactive behaviors (modern approach)
- **Inputs**: Legacy control mechanism — **DEPRECATED, use Data Binding**

## State Types

### Default States (always present per layer)
- **Entry**: Starting state; first thing that plays
- **Exit**: Stops layer playback (niche; useful in multi-layer scenarios)
- **Any State**: States connected here can play anytime regardless of current state (e.g., character skins)

### Animation States
- **Single Animation State**: One timeline. Can be one-shot, looping, or ping-pong.
- **1D Blend State**: Mixes multiple timelines with a single numerical value. Additive blending (not linear). Use for: loading bars, health systems, scrolling interactions.
- **Additive Blend State**: Blends multiple timelines using multiple number values. Has "Blend by Value" (baseline pose) and "Blend by Input" (controlled mix). Use for: dynamic face rigs, complex pose blending.

### State Properties
- **Animation**: Assigned timeline
- **Speed**: Playback rate (positive = forward, negative = backward)
- **Transitions**: View/manage transitions leaving this state

## Transitions

Connections between states with configurable properties.

**Create**: Drag ellipse from source state to target. Multiple transitions between same states = "or" conditions.

### Properties
| Property | Description |
|---|---|
| **Duration** | How long transition takes (ms). Default 0 = instant snap. Properties interpolate from source to target. |
| **Exit Time** | How much of current state must play before transitioning. Value or percentage. |
| **Pause When Exiting** | Pauses the source animation during transition |
| **Interpolation** | Linear (default), Cubic, or Hold |

### Conditions
- **View Model Properties** (modern): Bind data binding properties as conditions
- **Boolean**: True/false condition (legacy)
- **Number**: Equals, greater than, less than (legacy)
- **Trigger**: Fires when triggered (legacy)
- **Multiple conditions**: Create "and" logic
- **Custom**: Transition Condition Scripts for complex logic

## Layers

Allow multiple simultaneous animations. One animation per layer at a time.

- **Order matters**: Rightmost layer takes priority for same object properties
- **Reorder**: Drag and drop
- **Each layer**: Has its own Entry, Exit, Any State
- **Use case**: Background animation + independent interactions on same artboard

## Listeners (Modern Interaction System)

Enable interactive behavior without code. **Preferred over legacy Inputs for in-editor interactivity.**

### Three Components

**1. Target** — Where to listen
- Shapes as hit areas (ellipse, rectangle, etc.)
- Groups (shapes within serve as interactive area)
- Artboards/components (for their events)
- **Opaque Target**: Controls whether pointer events pass through

**2. User Action** — What interaction
- Pointer Down, Pointer Up, Pointer Enter, Pointer Exit, Pointer Move, Click
- Listen for Event (if target is artboard/component)

**3. Listener Action** — What happens (multiple actions possible)
- **View Model Change** (default): Update any view model property. Can use converters (add, multiply, convert types).
- **Report Event**: Fire an event
- **Align Target**: Position object to follow pointer
- **Input Change** (legacy): Toggle boolean, fire trigger, set number

## Events — DEPRECATED (except Audio)

Events are the legacy signal system. Use Data Binding for output, Listeners for input.

### Event Types
- **General Event**: Custom event with optional properties
- **URL Event**: Navigate to URL
- **Audio Event**: Trigger sound (still active/valid)

### Signaling Events
Events can fire from: Timeline (at specific frame), State (start/end), Transition (start/end), Listener (user interaction)

### Audio Events (Still Active)
- Trigger sound effects within animations or via interaction
- Import audio or browse Soundly library (3000+ free sounds)
- Create clips from longer audio
- Export: Embedded (larger .riv), Referenced (separate files), Hosted (CDN)
- Best for: Sound effects. Not for: background music, voice-overs (no volume/panning control yet)

### Audio via Scripting
Audio can also be triggered programmatically using the `Audio` global scripting API:
- `Context:audio(name)` — get a handle to an audio asset
- `Audio:play*()` — play audio, returns an `AudioSound` instance
- `AudioSound` methods: `play()`, `pause()`, `resume()`, `stop()`, `seek(seconds)`, `volume`
- Source docs: `scripting/api-reference/interfaces/audio-source.mdx`, `scripting/api-reference/interfaces/audio-sound.mdx`

## Inputs — DEPRECATED

Legacy control mechanism. **Use Data Binding with View Models instead.**

Types: Boolean, Number, Trigger

Limitations:
- Can only drive state machine transitions
- No listening API at runtime (polling only)
- Cannot be converted
- Limited type support

## Animation Fundamentals

### Animate Mode
Activates when state machine or animation is selected. Shows timeline with keyframes and playback controls.

### Key Concepts
- Properties with key icons in Inspector are animatable
- Interpolation curves determine easing between keys
- Multiple animations blend via state machine layers
- Draw order can be animated over time

### Blend Mechanics
- **1D Blending**: Additive mixing (not linear — may give unexpected results). Single value controls mix across range.
- **Additive Blending**: Multiple values control different animation components. Baseline pose + controlled inputs create complex results.

## Best Practices

1. Use **listeners** for all in-editor interactive UI behaviors
2. Use **view model properties** for state machine transition conditions (not inputs)
3. Use **data binding** for all designer-developer communication
4. **Audio events** are still valid for sound triggering from timelines, transitions, and listeners. The scripting `Audio` API is the alternative for programmatic control.
5. **Layers**: Rightmost wins for property conflicts
6. **Exit Time**: Controls animation completion before transition
7. **Any State + multiple layers**: Enable complex interaction patterns
8. **One-shot animations** for idle states — state machine auto-pauses when idle (low CPU)
9. **Transition out of blend states** when finished to prevent continuous playback
