# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# message_item.py                           #
# ######################################### #

from textual.widgets import ListItem, Button, Static
from textual.containers import Grid, Vertical
from textual import on

from app.presets import MessagePreset


class MessageItem(ListItem):
    """Message displayed in two-column table style."""

    def __init__(self, preset: MessagePreset) -> None:
        self.preset = preset
        super().__init__(
            Grid(
                Vertical(
                    Static(preset.text, classes="msg-text"),
                    Static(
                        f"Voice: {preset.voice}  Speed: {preset.speed}  Pitch: {preset.pitch}  Volume: {preset.volume}  Gap: {preset.word_gap}",
                        classes="params",
                    ),
                    classes="message-col1",
                ),
                Button("x", id="delete"),
                classes="message-grid",
            )
        )

    @on(Button.Pressed, "#delete")
    def delete_pressed(self, event: Button.Pressed) -> None:
        self.remove()
        event.stop()
