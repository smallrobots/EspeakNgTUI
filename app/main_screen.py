# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# main_screen.py                            #
# ######################################### #

from textual.app import ComposeResult
from textual.containers import Grid, Horizontal, Vertical, Container
from textual.screen import Screen
from textual.widgets import Static, Input, Button, ListView
from textual.reactive import reactive
from textual import on
from rich.text import Text
import re
import asyncio

from app.command_builder import EspeakParameters, compose_command
from app.presets import MessagePreset
from app.defaults import Defaults
from app.message_item import MessageItem


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

    def sanitize_text(self, text: str) -> str:
        """Remove control and invisible characters from text."""
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
                        yield Input(id="text", value=Defaults.TEXT, placeholder="Type something here...")
                        yield Button(label="Play", id="play")
                        yield Button(label="Add", id="add")
                with Container(id="right"):
                    yield Static("Messages", classes="label")
                    yield ListView(id="messages")
                    yield Static(
                        "No messages yet. Use the 'Add' button to create one.",
                        id="empty-label",
                        classes="label",
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

