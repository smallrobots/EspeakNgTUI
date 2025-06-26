# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# test_cli_args.py                          #
# ######################################### #

import os
import sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from estui import parse_args, DEFAULT_PRESET_FILE


def test_default_file():
    args = parse_args([])
    assert args.document == DEFAULT_PRESET_FILE


def test_custom_file():
    args = parse_args(["custom.json"])
    assert args.document == "custom.json"


def test_invalid_extension():
    with pytest.raises(SystemExit):
        parse_args(["not_json.txt"])
