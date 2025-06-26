# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# test_message_document.py                  #
# ######################################### #

import os
import sys
import tempfile
import json

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.presets import MessagePreset, MessageDocument


def test_save_and_load(tmp_path):
    doc = MessageDocument([
        MessagePreset(text="a", voice="it", speed="175", pitch="50", volume="100", word_gap="0"),
        MessagePreset(text="b", voice="en", speed="180", pitch="60", volume="110", word_gap="1"),
    ])
    file_path = tmp_path / "messages.json"
    doc.save(file_path)
    loaded = MessageDocument.load(file_path)
    assert loaded.messages == doc.messages


def test_json_format(tmp_path):
    preset = MessagePreset(text="hello", voice="it", speed="175", pitch="50", volume="100", word_gap="0")
    doc = MessageDocument([preset])
    file_path = tmp_path / "m.json"
    doc.save(file_path)
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    assert data == {
        "messages": [
            {
                "text": "hello",
                "voice": "it",
                "speed": "175",
                "pitch": "50",
                "volume": "100",
                "word_gap": "0",
            }
        ]
    }


