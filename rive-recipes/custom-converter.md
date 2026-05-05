# Custom Converter Script (number → formatted string)

**What this covers:** A Luau Converter script that transforms a number into a formatted display string (e.g. `1500` → `"1,500 pts"`).
**Rive features used:** Scripting (Converter protocol), data binding, view model.

## Editor setup

1. Create a **Script** asset: Assets Panel → + → Script → **Converter** protocol. Name it `ScoreFormatter`.
2. In the Data panel, click `+` → **Converters → Script → ScoreFormatter** to create a converter instance.
3. Create a View Model with a number property `score`.
4. Create a text object and bind its text run to `score` using `ScoreFormatter` as the converter.

## Script

```lua
-- ScoreFormatter.lua
type ScoreFormatter = {}

local function commaFormat(n: number): string
  local sign = ""
  if n < 0 then
    sign = "-"
    n = math.abs(n)
  end

  local s = tostring(math.floor(n))
  local result = ""
  local count = 0

  for i = #s, 1, -1 do
    if count > 0 and count % 3 == 0 then
      result = "," .. result
    end
    result = s:sub(i, i) .. result
    count += 1
  end

  return sign .. result
end

function init(self: ScoreFormatter, context: Context): boolean
  return true
end

function convert(self: ScoreFormatter, input: DataValueNumber): DataValueString
  local output = DataValue.string()
  output.value = commaFormat(input.value) .. " pts"
  return output
end

function reverseConvert(self: ScoreFormatter, input: DataValueString): DataValueNumber
  local output = DataValue.number()
  local digits = input.value:gsub("[^%d%-]", "")
  output.value = tonumber(digits) or 0
  return output
end

return function(): Converter<ScoreFormatter, DataValueNumber, DataValueString>
  return {
    init = init,
    convert = convert,
    reverseConvert = reverseConvert,
  }
end
```

## Notes

- The converter type declares its exact input and output: `Converter<ScoreFormatter, DataValueNumber, DataValueString>`.
- `DataValue.number()` and `DataValue.string()` construct new typed values.
- The editor uses `reverseConvert` for reverse/bidirectional flow; source-to-target-only use cases can implement a simple inverse or documented passback as appropriate for the selected converter type.
- Keep `convert` and `reverseConvert` side-effect free; they should not mutate view models, play audio, or call external services.
- Built-in converters (add, multiply, to-string) handle simple cases — use a script only for logic built-ins can't express.
- Keep `convert` fast — it runs every frame when the bound value changes.
- Source docs: `scripting/protocols/converter-scripts.mdx`
