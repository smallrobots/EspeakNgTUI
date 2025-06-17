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
