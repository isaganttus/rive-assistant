# Audio Triggered from Luau Script

**What this covers:** Playing audio programmatically from a Rive Luau script using the `Audio` global API.
**Rive features used:** Scripting (Node protocol), Audio API, imported audio assets.

## Editor setup

1. Import an audio file into the **Assets Panel** (drag in or + button). Accepts WAV, MP3, OGG.
2. Create a **Script** asset: Assets Panel → + → Script → **Node** protocol. Name it `SoundController`.
3. Attach the script to your artboard: right-click artboard → Add Script → `SoundController`.

## Script

```lua
-- SoundController.lua
type SoundController = {
  source: AudioSource?,
  active: AudioSound?,
}

function init(self: SoundController, context: Context): boolean
  self.source = context:audio("explosion")
  return self.source ~= nil
end

function playOnce(self: SoundController)
  local source = self.source
  if source == nil then
    return
  end

  local sound = Audio.play(source)
  if sound ~= nil then
    sound.volume = 0.8
    self.active = sound
  end
end

return function(): Node<SoundController>
  return {
    source = nil,
    active = nil,
    init = init,
    playOnce = playOnce,
  }
end
```

## Triggering from a Listener Action Script

```lua
-- TriggerOnClick.lua
type TriggerOnClick = {
  source: AudioSource?,
}

function init(self: TriggerOnClick, context: Context): boolean
  self.source = context:audio("explosion")
  return self.source ~= nil
end

function performAction(self: TriggerOnClick, listenerContext: ListenerContext)
  local pointer = listenerContext:asPointerEvent()
  if pointer ~= nil then
    pointer:hit()
  end

  local source = self.source
  if source == nil then
    return
  end

  local sound = Audio.play(source)
  if sound ~= nil then
    sound.volume = 0.8
  end
end

return function(): ListenerAction<TriggerOnClick>
  return {
    source = nil,
    init = init,
    performAction = performAction,
  }
end
```

## AudioSound control

```lua
local s = Audio.play(source)
if s ~= nil then
  s:pause()
  s:resume()
  s:stop()
  s:seek(1.5)    -- jump to 1.5 seconds
  s.volume = 0.5
end
```

## Notes

- `context:audio("name")` returns an `AudioSource?`; the name must match the asset in the Assets Panel exactly.
- `Audio.play(source)` and the other `Audio.play*` functions return an `AudioSound?`.
- `AudioSound` supports `pause()`, `resume()`, `stop(fadeToStopTime?)`, `seek(seconds)`, `seekFrame(frame)`, `time()`, `timeFrame()`, `completed()`, and writable `volume`.
- Use `performAction(self, listenerContext)` for new Listener Action scripts.
- Source docs: `scripting/api-reference/interfaces/audio-source.mdx`, `scripting/api-reference/interfaces/audio-sound.mdx`.
- **Audio Events** (non-scripting): add an Audio Event to a timeline keyframe or state machine transition — simpler for static sound cues.
- Web Audio API autoplay policy requires a user gesture before the first audio call.
- Not all runtimes support all audio features — check `feature-support.mdx` for your platform.
