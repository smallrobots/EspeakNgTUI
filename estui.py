from textual.app import App, ComposeResult
from textual.containers import Grid
from textual.containers import Horizontal, Vertical, Container
from textual.screen import Screen
from textual.widgets import Static, Input, Button, ListView, ListItem
from textual.reactive import reactive
from textual import on
from rich.text import Text
import re
import asyncio

from espeak_checker import EspeakNgChecker
from command_builder import EspeakParameters, compose_command
from presets import MessagePreset


class Defaults:
    """Costanti di default per i parametri di espeak-ng."""
    VOICE = "it"
    SPEED = "175"
    PITCH = "50"
    VOLUME = "100"
    WORD_GAP = "0"
    TEXT = ""

class MessageItem(ListItem):
    """Messaggio in stile tabellare: 2 colonne, 1 riga."""

    def __init__(self, preset: MessagePreset) -> None:
        self.preset = preset
        super().__init__(
            Grid(
                Vertical(
                    Static(preset.text, classes="msg-text"),
                    Static(
                        f"Voce: {preset.voice}  Velocità: {preset.speed}  Pitch: {preset.pitch}  Volume: {preset.volume}  Pausa: {preset.word_gap}",
                        classes="params"
                    ),
                    classes="message-col1"
                ),
                Button("x", id="delete"),
                classes="message-grid"
            )
        )

    @on(Button.Pressed, "#delete")
    def delete_pressed(self, event: Button.Pressed) -> None:
        self.remove()
        event.stop()


class MainScreen(Screen):
    """Screen principale dell'applicazione."""

    text: reactive[str] = reactive(Defaults.TEXT)
    voice: reactive[str] = reactive(Defaults.VOICE)
    speed: reactive[str] = reactive(Defaults.SPEED)
    pitch: reactive[str] = reactive(Defaults.PITCH)
    volume: reactive[str] = reactive(Defaults.VOLUME)
    word_gap: reactive[str] = reactive(Defaults.WORD_GAP)

    preview_widget: Static
    messages_view: ListView
    empty_label: Static

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
                        yield Input(id="voice", value=Defaults.VOICE)
                        yield Static("Velocità (80-500)", classes="label")
                        yield Input(id="speed", value=Defaults.SPEED)
                        yield Static("Pitch (0-99)", classes="label")
                        yield Input(id="pitch", value=Defaults.PITCH)
                        yield Static("Volume (0-200)", classes="label")
                        yield Input(id="volume", value=Defaults.VOLUME)
                        yield Static("Pausa tra parole (x10ms)", classes="label")
                        yield Input(id="word_gap", value=Defaults.WORD_GAP)
                        yield Static("Testo da sintetizzare", classes="label")
                        yield Input(id="text", value=Defaults.TEXT, placeholder="Scrivi qualcosa qui...")
                        yield Button(label="Riproduci", id="play")
                        yield Button(label="Aggiungi", id="add")
                with Container(id="right"):
                    yield Static("Messaggi", classes="label")
                    yield ListView(id="messages")
                    yield Static(
                        "Nessun messaggio presente. Per aggiungere un nuovo messaggio utilizzare il pulsante \"Aggiungi\".",
                        id="empty-label",
                        classes="label"
                    )
            yield Static("Anteprima comando", classes="label")
            yield Static("", id="preview")

    def on_mount(self) -> None:
        self.preview_widget = self.query_one("#preview", Static)
        self.messages_view = self.query_one("#messages", ListView)
        self.empty_label = self.query_one("#empty-label", Static)
        self.update_empty_label_visibility()
        self.update_preview()

    def update_empty_label_visibility(self) -> None:
        self.empty_label.display = len(self.messages_view.children) == 0

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
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

    async def execute_espeak(self, command: str) -> None:
        process = await asyncio.create_subprocess_shell(command)
        await process.wait()

    @on(ListView.Selected, "#messages")
    def on_message_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, MessageItem):
            preset = item.preset
            self.query_one("#text", Input).value = preset.text
            self.query_one("#voice", Input).value = preset.voice
            self.query_one("#speed", Input).value = preset.speed
            self.query_one("#pitch", Input).value = preset.pitch
            self.query_one("#volume", Input).value = preset.volume
            self.query_one("#word_gap", Input).value = preset.word_gap
            self.text = preset.text
            self.voice = preset.voice
            self.speed = preset.speed
            self.pitch = preset.pitch
            self.volume = preset.volume
            self.word_gap = preset.word_gap

    async def on_button_pressed(self, event: Button.Pressed) -> None:
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
            await self.execute_espeak(command)
        elif event.button.id == "add":
            preset = MessagePreset(
                text=self.text,
                voice=self.voice,
                speed=self.speed,
                pitch=self.pitch,
                volume=self.volume,
                word_gap=self.word_gap,
            )
            self.messages_view.append(MessageItem(preset))
            self.update_empty_label_visibility()

    @on(Button.Pressed, "#delete")
    def handle_delete(self, event: Button.Pressed) -> None:
        item = event.button.ancestor(MessageItem)
        if item:
            self.messages_view.remove(item)
            self.update_empty_label_visibility()
        event.stop()


class EspeakNgTuiApp(App):
    """Applicazione TUI principale."""

    CSS_PATH = "estui.css"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EspeakNgChecker().validate_or_raise()
    EspeakNgTuiApp().run()
