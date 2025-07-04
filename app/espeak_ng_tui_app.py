# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# espeak_ng_tui_app.py                      #
# ######################################### #

from textual.app import App

from app.main_screen import MainScreen


class EspeakNgTuiApp(App):
    """Main TUI application."""

    CSS_PATH = "estui.css"

    def __init__(self, presets_path: str) -> None:
        super().__init__()
        self.presets_path = presets_path

    def on_mount(self) -> None:
        self.push_screen(MainScreen(self.presets_path))

