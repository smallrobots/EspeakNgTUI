from textual.screen import ModalScreen
from textual.app import ComposeResult
from textual.containers import Vertical
from textual.widgets import Input, Button, Static
from textual import on

class FileModal(ModalScreen[str|None]):
    """Simple modal to input a file path."""

    AUTO_FOCUS = "#file-path"

    def __init__(self, title: str = "File path") -> None:
        super().__init__()
        self.title = title

    def compose(self) -> ComposeResult:
        with Vertical(id="file-modal"):
            yield Static(self.title, id="file-title")
            yield Input(placeholder="path", id="file-path")
            yield Button("OK", id="file-ok")
            yield Button("Cancel", id="file-cancel")

    @on(Button.Pressed, "#file-ok")
    def confirm(self) -> None:
        path = self.query_one("#file-path", Input).value
        self.dismiss(path)

    @on(Button.Pressed, "#file-cancel")
    def cancel(self) -> None:
        self.dismiss(None)
