from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from textual.widgets import Static, Input, Button
from textual.reactive import reactive
from textual import on
from rich.text import Text
import re

from espeak_checker import EspeakNgChecker
from command_builder import EspeakParameters, compose_command


class Defaults:
    """Costanti di default per i parametri di espeak-ng."""
    VOICE = "it"
    SPEED = "175"
    PITCH = "50"
    VOLUME = "100"
    WORD_GAP = "0"
    TEXT = ""


class MainScreen(Screen):
    """Screen principale dell'applicazione."""

    text: reactive[str] = reactive(Defaults.TEXT)
    voice: reactive[str] = reactive(Defaults.VOICE)
    speed: reactive[str] = reactive(Defaults.SPEED)
    pitch: reactive[str] = reactive(Defaults.PITCH)
    volume: reactive[str] = reactive(Defaults.VOLUME)
    word_gap: reactive[str] = reactive(Defaults.WORD_GAP)

    preview_widget: Static

    def watch_text(self, old: str, new: str) -> None:
        self.update_preview()

    def watch_voice(self, old: str, new: str) -> None:
        self.update_preview()

    def watch_speed(self, old: str, new: str) -> None:
        self.update_preview()

    def watch_pitch(self, old: str, new: str) -> None:
        self.update_preview()

    def watch_volume(self, old: str, new: str) -> None:
        self.update_preview()

    def watch_word_gap(self, old: str, new: str) -> None:
        self.update_preview()

    def sanitize_text(self, text: str) -> str:
        """Rimuove caratteri di controllo e invisibili dal testo."""
        return re.sub(r'[\x00-\x1F\x7F\x9B\x80-\x9F\u2028\u2029]', '', text)

    def update_preview(self) -> None:
        """Compose command and display it in the preview widget."""
        clean_text = self.sanitize_text(self.text)
        params = EspeakParameters(
            text=clean_text,
            voice=self.voice,
            speed=self.speed,
            pitch=self.pitch,
            volume=self.volume,
            word_gap=self.word_gap,
        )
        command = compose_command(params)
        self.preview_widget.update(Text(command))
        self.preview_widget.refresh(layout=True)

    def compose(self) -> ComposeResult:
        with Vertical(id="root"):
            with Horizontal(id="main"):
                with Container(id="left"):
                    with Vertical(id="controls"):
                        yield Static("Voce (es. it+f1)", classes="label")
                        yield Input(id="voice", value=Defaults.VOICE, placeholder="es. it+f1")
                        yield Static("Velocità (80-500)", classes="label")
                        yield Input(id="speed", value=Defaults.SPEED, placeholder=Defaults.SPEED)
                        yield Static("Pitch (0-99)", classes="label")
                        yield Input(id="pitch", value=Defaults.PITCH, placeholder=Defaults.PITCH)
                        yield Static("Volume (0-200)", classes="label")
                        yield Input(id="volume", value=Defaults.VOLUME, placeholder=Defaults.VOLUME)
                        yield Static("Pausa tra parole (x10ms)", classes="label")
                        yield Input(id="word_gap", value=Defaults.WORD_GAP, placeholder=Defaults.WORD_GAP)
                        yield Static("Testo da sintetizzare", classes="label")
                        yield Input(id="text", value=Defaults.TEXT, placeholder="Scrivi qualcosa qui...")
                        yield Button(label="Riproduci", id="play")
                yield Container(Static("Messaggi"), id="right")
            yield Static("Anteprima comando", classes="label")
            yield Static("", id="preview")

    def on_mount(self) -> None:
        self.preview_widget = self.query_one("#preview", Static)
        self.update_preview()

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        """Aggiorna le variabili reactive quando un input cambia."""
        mapping = {
            "text": "text",
            "voice": "voice",
            "speed": "speed",
            "pitch": "pitch",
            "volume": "volume",
            "word_gap": "word_gap",
        }
        if event.input.id is not None:
            attr = mapping.get(event.input.id)
            if attr is not None:
                setattr(self, attr, event.value)

    def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play":
            clean_text = self.sanitize_text(self.text)
            params = EspeakParameters(
                text=clean_text,
                voice=self.voice,
                speed=self.speed,
                pitch=self.pitch,
                volume=self.volume,
                word_gap=self.word_gap,
            )
            command = compose_command(params)
            self.log(command)
            self.preview_widget.update(Text(command))


class EspeakNgTuiApp(App):
    """Applicazione TUI principale."""

    CSS_PATH = "estui.css"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EspeakNgChecker().validate_or_raise()
    EspeakNgTuiApp().run()