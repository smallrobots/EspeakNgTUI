# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# estui.py                                  #
# ######################################### #

from pathlib import Path
import argparse

from app.espeak_checker import EspeakNgChecker

DEFAULT_PRESET_FILE = "messages_preset.json"


def _json_file(value: str) -> str:
    """Validate that ``value`` is a path to a JSON file."""
    path = Path(value)
    if path.is_dir() or path.suffix.lower() != ".json":
        raise argparse.ArgumentTypeError("Document path must be a JSON file")
    return value


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Return parsed command line arguments."""
    parser = argparse.ArgumentParser(
        description="Textual User Interface for ESpeak-NG"
    )
    parser.add_argument(
        "document",
        nargs="?",
        default=DEFAULT_PRESET_FILE,
        type=_json_file,
        help="JSON file used to load and save message presets",
    )
    return parser.parse_args(argv)

if __name__ == "__main__":
    args = parse_args()
    EspeakNgChecker().validate_or_raise()
    from app.espeak_ng_tui_app import EspeakNgTuiApp

    EspeakNgTuiApp(args.document).run()

