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
return function(): Node<SoundController>
  local sound: AudioSource

  local function init(self, context): boolean
    sound = context:audio("explosion") -- matches the asset name in the Assets Panel
    return sound ~= nil
  end

  local function advance(self, seconds): boolean
    return false
  end

  local function playOnce(self)
    if sound then
      local s: AudioSound = sound:playOnce()
      s.volume = 0.8
    end
  end

  return { init = init, advance = advance, playOnce = playOnce }
end
```

## Triggering from a Listener Action Script

```lua
-- TriggerOnClick.lua (ListenerAction protocol)
return function(): ListenerAction<TriggerOnClick>
  local function perform(self, context)
    local controller = context:node("SoundController")
    if controller then controller:playOnce() end
  end
  return { perform = perform }
end
```

## AudioSound control

```lua
local s: AudioSound = sound:play()   -- starts looping
s:pause()
s:resume()
s:stop()
s:seek(1.5)    -- jump to 1.5 seconds
s.volume = 0.5
```

## Notes

- `context:audio("name")` — name must match the asset name in the Assets Panel exactly.
- Play methods: `play()` (loops), `playOnce()` (fires once, auto-releases), `playFrom(seconds)`.
- Source docs: `scripting/api-reference/interfaces/audio-source.mdx`, `scripting/api-reference/interfaces/audio-sound.mdx`.
- **Audio Events** (non-scripting): add an Audio Event to a timeline keyframe or state machine transition — simpler for static sound cues.
- Web Audio API autoplay policy requires a user gesture before the first audio call.
- Not all runtimes support all audio features — check `feature-support.mdx` for your platform.
