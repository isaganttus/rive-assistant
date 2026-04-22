# Rive Mobile Runtimes Reference

## Overview

Mobile runtimes cover Flutter, Apple (iOS/macOS), Android, and React Native. All share the same core pattern but with platform-specific APIs.

**Source docs**: `runtimes/flutter/`, `runtimes/apple/`, `runtimes/android/`, `runtimes/react-native/`

## Flutter

### Installation
```yaml
dependencies:
  rive: ^latest
```

### Basic Usage
```dart
RiveAnimation.asset(
  'assets/file.riv',
  stateMachines: ['StateMachineName'],
)
```

### Key Components
- `RiveAnimation.asset()` / `RiveAnimation.network()` — simple widget
- `StateMachineController` — programmatic control of state machines
- `RiveNative` — opt-in Rive Renderer (vs. Flutter's Skia/Impeller)

### Renderer Choice
Flutter requires explicit renderer choice:
- **Rive Native**: Best quality, vector feathering support
- **Flutter (Skia/Impeller)**: Default Flutter rendering

### State Machine Control
```dart
final controller = StateMachineController.fromArtboard(artboard, 'SM');
final input = controller.findInput<bool>('isActive');
input?.value = true;
```

### Data Binding
Use View Model APIs to get/set properties and subscribe to changes.

**For detailed Flutter API**: See `runtimes/flutter/` source docs.

## Apple (iOS / macOS)

### Installation
- **Swift Package Manager**: Add Rive package URL
- **CocoaPods**: `pod 'RiveRuntime'`

### SwiftUI
```swift
RiveViewModel(fileName: "file").view()
```

### UIKit
```swift
let riveView = RiveView()
let viewModel = RiveViewModel(fileName: "file")
viewModel.setView(riveView)
```

### Key Components
- `RiveViewModel` — manages Rive file, artboard, state machine
- `RiveView` — UIView/NSView subclass for rendering
- Rive Renderer is the default on Apple platforms

### State Machine Control
```swift
viewModel.setInput("isActive", value: true)
viewModel.triggerInput("fireTrigger")
```

### Data Binding
Use View Model Instance APIs for property access and change observation.

### Gotchas
- Monitor resource usage on older devices
- RiveViewModel manages lifecycle — don't retain extra references

**For detailed Apple API**: See `runtimes/apple/` source docs.

## Android

### Installation
```gradle
dependencies {
    implementation 'app.rive:rive-android:+'
}
```

### XML Layout
```xml
<app.rive.runtime.kotlin.RiveAnimationView
    android:id="@+id/rive_view"
    app:riveResource="@raw/file"
    app:riveStateMachine="StateMachineName"
    app:riveAutoPlay="true" />
```

### Jetpack Compose
```kotlin
RiveAnimation(
    resId = R.raw.file,
    stateMachineName = "StateMachineName",
    autoplay = true,
)
```

### Key Components
- `RiveAnimationView` — main rendering view
- Rive Renderer is the default on Android
- Supports both XML layout and Jetpack Compose

### State Machine Control
```kotlin
riveView.setInput("isActive", true)
riveView.fireState("StateMachineName", "triggerName")
```

### Data Binding
Observe view model property changes via platform-appropriate patterns.

**For detailed Android API**: See `runtimes/android/` source docs.

## React Native

### Installation
```bash
npm install rive-react-native
```

### Basic Usage
```jsx
import Rive, { useRef } from "rive-react-native";

function MyComponent() {
  const riveRef = useRef(null);
  return (
    <Rive
      ref={riveRef}
      resourceName="file"
      stateMachineName="StateMachineName"
      autoplay={true}
    />
  );
}
```

### Key Components
- `<Rive>` component — main rendering view
- `useRef` for `RiveRef` methods (programmatic control)
- Expo integration supported
- Native version customization available

### State Machine Control
```javascript
riveRef.current?.setInputState("SM", "isActive", true);
riveRef.current?.fireState("SM", "triggerName");
```

### Platform Notes
- Uses native Rive Renderer (platform-dependent)
- Customize underlying native Rive version if needed

**For detailed React Native API**: See `runtimes/react-native/` source docs.

## Cross-Platform Patterns

1. **Asset loading**: All platforms support embedded and out-of-band assets
2. **Caching**: Parse .riv once, reuse for multiple instances
3. **State machine names**: Must match exactly (case-sensitive)
4. **Data binding**: All platforms support View Model property access/modification
5. **Events**: All platforms can listen for reported events
6. **Cleanup**: Dispose/cleanup resources when views are removed
7. **Renderer**: Rive Renderer is default on most native platforms; explicitly choose on Flutter
