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

-- Called once when the script initializes.
function init(self: ScoreFormatter): boolean
  return true
end

-- Converts a number input into a comma-formatted string.
function convert(self: ScoreFormatter, input: DataInputs): DataOutput
  local dv: DataValueString = DataValue.string()

  if input:isNumber() then
    local n = math.floor((input :: DataValueNumber).value)
    local s = tostring(n)
    local result = ""
    local count = 0
    for i = #s, 1, -1 do
      if count > 0 and count % 3 == 0 then result = "," .. result end
      result = s:sub(i, i) .. result
      count = count + 1
    end
    dv.value = result .. " pts"
  else
    dv.value = "0 pts"
  end

  return dv
end

-- For 2-way binding: converts the formatted string back to a number.
function reverseConvert(self: ScoreFormatter, input: DataOutput): DataInputs
  local dv: DataValueNumber = DataValue.number()

  if input:isString() then
    local digits = (input :: DataValueString).value:gsub("[^%d]", "")
    dv.value = tonumber(digits) or 0
  else
    dv.value = 0
  end

  return dv
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

- `input` is typed as `DataInputs` — check `input:isNumber()`, `input:isString()`, etc. before casting with `::`.
- `DataValue.number()` and `DataValue.string()` construct new typed output values.
- `reverseConvert` enables bidirectional bindings. Omit it for source-to-target only.
- Built-in converters (add, multiply, to-string) handle simple cases — use a script only for logic built-ins can't express.
- Keep `convert` fast — it runs every frame when the bound value changes.
- Source docs: `scripting/protocols/converter-scripts.mdx`
