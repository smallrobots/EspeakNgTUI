from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from textual.widgets import Static, Input
from textual.reactive import reactive

from espeak_checker import EspeakNgChecker

class MainScreen(Screen):
    """Screen principale dell'applicazione."""

    text: reactive[str] = reactive("")
    voice: reactive[str] = reactive("")
    speed: reactive[str] = reactive("175")
    pitch: reactive[str] = reactive("50")
    volume: reactive[str] = reactive("100")
    word_gap: reactive[str] = reactive("0")

    def compose(self) -> ComposeResult:
        """Crea il layout di base con due colonne e un'area inferiore."""
        with Vertical(id="root"):
            with Horizontal(id="main"):
                with Container(id="left"):
                    with Vertical(id="controls"):
                        yield Static("Testo da sintetizzare", classes="label")
                        yield Input(id="text")
                        yield Static("Voce (es. it+f1)", classes="label")
                        yield Input(id="voice", placeholder="it")
                        yield Static("Velocità (80-500)", classes="label")
                        yield Input(id="speed", placeholder="175")
                        yield Static("Pitch (0-99)", classes="label")
                        yield Input(id="pitch", placeholder="50")
                        yield Static("Volume (0-200)", classes="label")
                        yield Input(id="volume", placeholder="100")
                        yield Static("Pausa tra parole (x10ms)", classes="label")
                        yield Input(id="wordgap", placeholder="0")
                yield Container(Static("Messaggi"), id="right")
            yield Static("Anteprima comando", id="preview")

    def on_input_changed(self, event: Input.Changed) -> None:
        """Aggiorna le variabili reactive quando un input cambia."""
        mapping = {
            "text": "text",
            "voice": "voice",
            "speed": "speed",
            "pitch": "pitch",
            "volume": "volume",
            "wordgap": "word_gap",
        }
        attr = mapping.get(event.input.id)
        if attr is not None:
            setattr(self, attr, event.value)


class EspeakNgTuiApp(App):
    """Applicazione TUI principale."""

    CSS_PATH = "estui.css"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EspeakNgChecker().validate_or_raise()
    EspeakNgTuiApp().run()
