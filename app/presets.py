# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# presets.py                                #
# ######################################### #

from dataclasses import dataclass

@dataclass
class MessagePreset:
    """Parameters for a stored TTS message."""

    text: str
    voice: str
    speed: str
    pitch: str
    volume: str
    word_gap: str
