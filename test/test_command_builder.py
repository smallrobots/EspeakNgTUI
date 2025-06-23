# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# test_command_builder.py                   #
# ######################################### #

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from command_builder import EspeakParameters, compose_command


def test_compose_basic():
    params = EspeakParameters(text="hello")
    cmd = compose_command(params)
    assert "espeak-ng" in cmd
    assert cmd.endswith("hello")


def test_compose_all_params():
    params = EspeakParameters(
        text="hello",
        voice="it+f1",
        speed="180",
        pitch="70",
        volume="120",
        word_gap="10",
    )
    cmd = compose_command(params)
    expected = "espeak-ng -v it+f1 -s 180 -p 70 -a 120 -g 10 hello"
    assert cmd == expected
