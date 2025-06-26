# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# file_modal.py                             #
# ######################################### #

"""Modal window to request a file path from the user."""

from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical, Horizontal
from textual.widgets import Static, Input, Button
from textual import on


class FileModal(ModalScreen[str | None]):
    """Prompt the user to enter a path for opening or saving a file."""

    def __init__(self, title: str) -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:  # type: ignore[override]
        with Vertical(id="file-modal"):
            yield Static(self.title, id="file-title")
            yield Input(id="file-path")
            with Horizontal():
                yield Button("OK", id="file-ok")
                yield Button("Cancel", id="file-cancel")

    def on_mount(self) -> None:
        self.query_one("#file-path", Input).focus()

    @on(Button.Pressed, "#file-ok")
    def _ok(self) -> None:
        path = self.query_one("#file-path", Input).value
        self.dismiss(path or None)

    @on(Button.Pressed, "#file-cancel")
    def _cancel(self) -> None:
        self.dismiss(None)

