# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# presets.py                                #
# ######################################### #

from dataclasses import dataclass, asdict
import json
from typing import List


@dataclass
class MessagePreset:
    """Parameters for a stored TTS message."""

    text: str
    voice: str
    speed: str
    pitch: str
    volume: str
    word_gap: str


@dataclass
class MessageDocument:
    """Collection of :class:`MessagePreset` with JSON I/O helpers."""

    messages: List[MessagePreset]

    def to_dict(self) -> dict:
        """Return a serializable representation."""
        return {"messages": [asdict(msg) for msg in self.messages]}

    def save(self, path: str) -> None:
        """Save document to ``path`` in JSON format."""
        with open(path, "w", encoding="utf-8") as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)

    @classmethod
    def load(cls, path: str) -> "MessageDocument":
        """Load document from ``path``."""
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        messages = [MessagePreset(**m) for m in data.get("messages", [])]
        return cls(messages)

