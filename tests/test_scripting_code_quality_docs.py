import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

SCRIPTING_SURFACES = [
    "rive-reference/05-scripting.md",
    "rive-recipes/custom-converter.md",
    "rive-recipes/transition-condition-script.md",
    "rive-recipes/custom-layout.md",
    "rive-recipes/audio-from-script.md",
]

STALE_PATTERNS = {
    "Vec2D": "Use `Vector` and `Vector.xy(...)` in Rive Luau scripts.",
    "vm:number(": "Use `vm:getNumber(...)` and read the returned property's `.value`.",
    ":get()": "Read Rive ViewModel properties through `.value`.",
    "perform(self": "Use `performAction(self, listenerContext)` for ListenerAction scripts.",
    "context = late()": "Protocol context is passed to `init`; do not invent a `context` field.",
    "DataInputs": "Use exact DataValue input types when the converter type is known.",
    "DataOutput": "Use exact DataValue output types when the converter type is known.",
}


class ScriptingCodeQualityDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_scripting_surfaces_do_not_use_stale_luau_api_shapes(self):
        for relative_path in SCRIPTING_SURFACES:
            content = self.read(relative_path)
            for stale, guidance in STALE_PATTERNS.items():
                with self.subTest(path=relative_path, stale=stale):
                    self.assertNotIn(stale, content, guidance)

    def test_scripting_surfaces_teach_current_replacements(self):
        reference = self.read("rive-reference/05-scripting.md")
        self.assertIn("Before writing Luau code", reference)
        self.assertIn("Vector.xy", reference)
        self.assertIn("vm:getNumber", reference)
        self.assertIn("performAction", reference)

        converter = self.read("rive-recipes/custom-converter.md")
        self.assertIn("Converter<ScoreFormatter, DataValueNumber, DataValueString>", converter)

        transition = self.read("rive-recipes/transition-condition-script.md")
        self.assertIn("pressCount.value", transition)

        audio = self.read("rive-recipes/audio-from-script.md")
        self.assertIn("Audio.play", audio)
        self.assertIn("ListenerContext", audio)


if __name__ == "__main__":
    unittest.main()
