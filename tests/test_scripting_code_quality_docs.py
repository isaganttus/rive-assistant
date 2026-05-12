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

AUDIO_SCRIPTING_SURFACES = [
    "AGENTS.md",
    "CLAUDE.md",
    "GEMINI.md",
    ".cursor/rules/rive.mdc",
    ".windsurfrules",
    ".github/copilot-instructions.md",
    "rive-reference/02-state-machines-and-events.md",
    "rive-reference/05-scripting.md",
    "rive-recipes/audio-from-script.md",
    "evals/cases/audio-from-luau-script.json",
]

STALE_PATTERNS = {
    "Vec2D": "Use `Vector` and `Vector.xy(...)` in Rive Luau scripts.",
    "vm:number(": "Use `vm:getNumber(...)` and read the returned property's `.value`.",
    ":get()": "Read Rive ViewModel properties through `.value`.",
    "context = late()": "Protocol context is passed to `init`; do not invent a `context` field.",
    "DataInputs": "Use exact DataValue input types when the converter type is known.",
    "DataOutput": "Use exact DataValue output types when the converter type is known.",
}

LEGACY_LISTENER_ACTION_PATTERN = "perform(self"
LEGACY_LISTENER_ACTION_GUIDANCE = (
    "Use `performAction(self, listenerContext)` for new ListenerAction scripts."
)


def is_allowed_legacy_listener_action_line(line: str) -> bool:
    lowered = line.lower()
    return "deprecated" in lowered or "legacy" in lowered


class ScriptingCodeQualityDocsTest(unittest.TestCase):
    def read(self, relative_path: str) -> str:
        return (ROOT / relative_path).read_text(encoding="utf-8")

    def test_scripting_surfaces_do_not_use_stale_luau_api_shapes(self):
        for relative_path in SCRIPTING_SURFACES:
            for line_number, line in enumerate(self.read(relative_path).splitlines(), start=1):
                location = f"{relative_path}:{line_number}"
                for stale, guidance in STALE_PATTERNS.items():
                    with self.subTest(path=relative_path, line=line_number, stale=stale):
                        self.assertNotIn(stale, line, f"{location}: {guidance}")

                if (
                    LEGACY_LISTENER_ACTION_PATTERN in line
                    and not is_allowed_legacy_listener_action_line(line)
                ):
                    self.fail(f"{location}: {LEGACY_LISTENER_ACTION_GUIDANCE}")

    def test_audio_scripting_surfaces_use_dot_call_audio_global(self):
        for relative_path in AUDIO_SCRIPTING_SURFACES:
            for line_number, line in enumerate(self.read(relative_path).splitlines(), start=1):
                location = f"{relative_path}:{line_number}"
                with self.subTest(path=relative_path, line=line_number):
                    self.assertNotIn(
                        "Audio:play",
                        line,
                        f"{location}: Use `Audio.play*` dot-call global functions.",
                    )

    def test_scripting_surfaces_teach_current_replacements(self):
        reference = self.read("rive-reference/05-scripting.md")
        self.assertIn("Before writing Luau code", reference)
        self.assertIn("Vector.xy", reference)
        self.assertIn("vm:getNumber", reference)
        self.assertIn("performAction", reference)
        self.assertIn("reverseConvert(self, input: O) -> I`: Required by the protocol contract", reference)

        converter = self.read("rive-recipes/custom-converter.md")
        self.assertIn("Converter<ScoreFormatter, DataValueNumber, DataValueString>", converter)
        self.assertIn("`reverseConvert` is part of the `Converter<T, I, O>` protocol contract", converter)

        transition = self.read("rive-recipes/transition-condition-script.md")
        self.assertIn("pressCount.value", transition)

        audio = self.read("rive-recipes/audio-from-script.md")
        self.assertIn("Audio.play", audio)
        self.assertIn("ListenerContext", audio)

        events = self.read("rive-reference/02-state-machines-and-events.md")
        self.assertIn("Audio.play", events)


if __name__ == "__main__":
    unittest.main()
