from textual.app import App, ComposeResult
from textual.containers import Horizontal, Container
from textual.screen import Screen
from textual.widgets import Static

class MainScreen(Screen):
    """Screen principale dell'applicazione."""

    def compose(self) -> ComposeResult:
        """Crea il layout di base con due colonne."""
        with Horizontal(id="main"):
            yield Container(Static("Sinistra"), id="left")
            yield Container(Static("Destra"), id="right")


class EspeakNgTuiApp(App):
    """Applicazione TUI principale."""

    CSS_PATH = "estui.css"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EspeakNgTuiApp().run()
