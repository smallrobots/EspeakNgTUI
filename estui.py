from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from textual.widgets import Static

from espeak_checker import EspeakNgChecker

class MainScreen(Screen):
    """Screen principale dell'applicazione."""

    def compose(self) -> ComposeResult:
        """Crea il layout di base con due colonne e un'area inferiore."""
        with Vertical(id="root"):
            with Horizontal(id="main"):
                yield Container(Static("Controlli"), id="left")
                yield Container(Static("Messaggi"), id="right")
            yield Static("Anteprima comando", id="preview")


class EspeakNgTuiApp(App):
    """Applicazione TUI principale."""

    CSS_PATH = "estui.css"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EspeakNgChecker().validate_or_raise()
    EspeakNgTuiApp().run()
