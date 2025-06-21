import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from presets import MessagePreset


def test_preset_fields():
    preset = MessagePreset(
        text="hello",
        voice="it",
        speed="175",
        pitch="50",
        volume="100",
        word_gap="0",
    )
    assert preset.text == "hello"
    assert preset.voice == "it"
    assert preset.speed == "175"
    assert preset.pitch == "50"
    assert preset.volume == "100"
    assert preset.word_gap == "0"

