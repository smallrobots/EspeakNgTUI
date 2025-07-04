# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# info_modal.py                             #
# ######################################### #

from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Static, Button
from textual import on


class InfoModal(ModalScreen[None]):
    """Modal window displaying application information."""

    AUTO_FOCUS = "#info-close"

    def compose(self) -> ComposeResult:
        with Vertical(id="info-modal"):
            yield Static("ESpeak-ng TUI", id="info-title")
            yield Static(
                "Copyright 2025 - Oreste Riccardo Natale\nReleased under the MIT License",
                id="info-copy",
            )
            yield Static(
                "\nShortcuts:\nctrl+o open\nctrl+s save\nctrl+q quit",
                id="info-help",
            )
            yield Button("Close", id="info-close")

    @on(Button.Pressed, "#info-close")
    def close_modal(self) -> None:
        self.app.pop_screen()
