from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.reactive import reactive

from espeak_checker import EspeakNgChecker
from command_builder import EspeakParameters, compose_command

class MainScreen(Screen):
    """Screen principale dell'applicazione."""

    text: reactive[str] = reactive("")
    voice: reactive[str] = reactive("")
    speed: reactive[str] = reactive("175")
    pitch: reactive[str] = reactive("50")
    volume: reactive[str] = reactive("100")
    word_gap: reactive[str] = reactive("0")

    def watch_text(self, old: str, new: str) -> None:  # noqa: D401
        """Update preview when text changes."""
        self.update_preview()

    def watch_voice(self, old: str, new: str) -> None:  # noqa: D401
        self.update_preview()

    def watch_speed(self, old: str, new: str) -> None:  # noqa: D401
        self.update_preview()

    def watch_pitch(self, old: str, new: str) -> None:  # noqa: D401
        self.update_preview()

    def watch_volume(self, old: str, new: str) -> None:  # noqa: D401
        self.update_preview()

    def watch_word_gap(self, old: str, new: str) -> None:  # noqa: D401
        self.update_preview()

    def update_preview(self) -> None:
        """Compose command and display it in the preview widget."""
        params = EspeakParameters(
            text=self.text,
            voice=self.voice,
            speed=self.speed,
            pitch=self.pitch,
            volume=self.volume,
            word_gap=self.word_gap,
        )
        command = compose_command(params)
        self.query_one("#preview", Static).update(command)

    def on_mount(self) -> None:
        self.update_preview()

    def compose(self) -> ComposeResult:
        """Crea il layout di base con due colonne e un'area inferiore."""
        with Vertical(id="root"):
            with Horizontal(id="main"):
                with Container(id="left"):
                    with Vertical(id="controls"):
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
                        yield Static("Testo da sintetizzare", classes="label")
                        yield Input(id="text")
                        yield Button(label="Riproduci", id="play")
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
        if event.input.id  is not None:
            attr = mapping.get(event.input.id)
            if attr is not None:
                setattr(self, attr, event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play":
            params = EspeakParameters(
                text=self.text,
                voice=self.voice,
                speed=self.speed,
                pitch=self.pitch,
                volume=self.volume,
                word_gap=self.word_gap,
            )
            command = compose_command(params)
            self.log(command)
            self.query_one("#preview", Static).update(command)


class EspeakNgTuiApp(App):
    """Applicazione TUI principale."""

    CSS_PATH = "estui.css"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EspeakNgChecker().validate_or_raise()
    EspeakNgTuiApp().run()
