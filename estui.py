# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# estui.py                                  #
# ######################################### #

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
    """Default values for espeak-ng parameters."""
    VOICE = "it"
    SPEED = "175"
    PITCH = "50"
    VOLUME = "100"
    WORD_GAP = "0"
    TEXT = ""

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
    """Main application screen."""

    text: reactive[str] = reactive(Defaults.TEXT)
    voice: reactive[str] = reactive(Defaults.VOICE)
    speed: reactive[str] = reactive(Defaults.SPEED)
    pitch: reactive[str] = reactive(Defaults.PITCH)
    volume: reactive[str] = reactive(Defaults.VOLUME)
    word_gap: reactive[str] = reactive(Defaults.WORD_GAP)

    preview_widget: Static
    messages_view: ListView
    empty_label: Static
    copy_button: Button
    current_command: str = ""

    # --- Sanitizer --------------------------------------------------------

    ANSI_ESCAPE_RE = re.compile(r"\x1b\[[0-9;:<=>?]*[A-Za-z]")
    NON_PRINTABLE_RE = re.compile(r"[\x00-\x1F\x7F\x9B\x80-\x9F\u2028\u2029]")

    @classmethod
    def sanitize_input_text(cls, text: str) -> str:
        """Remove ANSI sequences and non‑printable characters from *any* text coming
        from a Textual ``Input`` widget.
        """
        text = cls.ANSI_ESCAPE_RE.sub("", text)            # 1️⃣ Strip ANSI / xterm mouse sequences
        text = cls.NON_PRINTABLE_RE.sub("", text)          # 2️⃣ Drop control chars & separators
        return text

    # ---------------------------------------------------------------------

    def update_preview(self) -> None:
        """Compose command and display it in the preview widget."""
        clean_text = self.sanitize_input_text(self.text)
        params = EspeakParameters(
            text=clean_text,
            voice=self.voice,
            speed=self.speed,
            pitch=self.pitch,
            volume=self.volume,
            word_gap=self.word_gap,
        )
        command = compose_command(params)
        self.current_command = command
        self.preview_widget.update(Text(command))
        self.preview_widget.refresh(layout=True)

    def compose(self) -> ComposeResult:
        with Vertical(id="root"):
            yield Static("Textual User Interface for ESpeak-NG", id="title")
            with Horizontal(id="main"):
                with Container(id="left"):
                    with Vertical(id="controls"):
                        yield Static("Voice (e.g. it+f1)", classes="label")
                        yield Input(id="voice", value=Defaults.VOICE)
                        yield Static("Speed (80-500)", classes="label")
                        yield Input(id="speed", value=Defaults.SPEED)
                        yield Static("Pitch (0-99)", classes="label")
                        yield Input(id="pitch", value=Defaults.PITCH)
                        yield Static("Volume (0-200)", classes="label")
                        yield Input(id="volume", value=Defaults.VOLUME)
                        yield Static("Word gap (x10ms)", classes="label")
                        yield Input(id="word_gap", value=Defaults.WORD_GAP)
                        yield Static("Text to synthesize", classes="label")
                        yield Input(id="text", value=Defaults.TEXT, placeholder="Type something here…")
                        yield Button(label="Play", id="play")
                        yield Button(label="Add", id="add")
                with Container(id="right"):
                    yield Static("Messages", classes="label")
                    yield ListView(id="messages")
                    yield Static(
                        "No messages yet. Use the 'Add' button to create one.",
                        id="empty-label",
                        classes="label"
                    )
            yield Static("Command preview", classes="label")
            with Grid(id="preview-row"):
                yield Static("", id="preview")
                yield Button(label="Copy", id="copy")

    def on_mount(self) -> None:
        self.preview_widget = self.query_one("#preview", Static)
        self.messages_view = self.query_one("#messages", ListView)
        self.copy_button = self.query_one("#copy", Button)
        self.empty_label = self.query_one("#empty-label", Static)
        self.update_empty_label_visibility()
        self.update_preview()

    def update_empty_label_visibility(self) -> None:
        self.empty_label.display = len(self.messages_view.children) == 0

    @on(Input.Changed)
    def on_input_changed(self, event: Input.Changed) -> None:
        # Sanitize the raw input value first
        event.input.value = self.sanitize_input_text(event.value)

        # Map the sanitized value to reactive attrs
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
                setattr(self, attr, event.input.value)

    async def execute_espeak(self, command: str) -> None:
        process = await asyncio.create_subprocess_shell(command)
        await process.wait()

    @on(ListView.Selected, "#messages")
    def on_message_selected(self, event: ListView.Selected) -> None:
        item = event.item
        if isinstance(item, MessageItem):
            self.query_one("#text", Input).value = item.preset.text
            self.query_one("#voice", Input).value = item.preset.voice
            self.query_one("#speed", Input).value = item.preset.speed
            self.query_one("#pitch", Input).value = item.preset.pitch
            self.query_one("#volume", Input).value = item.preset.volume
            self.query_one("#word_gap", Input).value = item.preset.word_gap
            self.text = item.preset.text
            self.voice = item.preset.voice
            self.speed = item.preset.speed
            self.pitch = item.preset.pitch
            self.volume = item.preset.volume
            self.word_gap = item.preset.word_gap

    async def on_button_pressed(self, event: Button.Pressed) -> None:
        if event.button.id == "play":
            clean_text = self.sanitize_input_text(self.text)
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
            self.current_command = command
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
        elif event.button.id == "copy":
            if self.current_command:
                self.app.copy_to_clipboard(self.current_command)

class EspeakNgTuiApp(App):
    """Main TUI application."""

    CSS_PATH = "estui.css"

    def on_mount(self) -> None:
        self.push_screen(MainScreen())


if __name__ == "__main__":
    EspeakNgChecker().validate_or_raise()
    EspeakNgTuiApp().run()
