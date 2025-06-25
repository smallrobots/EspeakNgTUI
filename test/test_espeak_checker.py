# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# test_espeak_checker.py                    #
# ######################################### #

import os
import sys
import pytest
import shutil

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from app.espeak_checker import EspeakNgChecker


def test_check_exists(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda exe: "/usr/bin/espeak-ng")
    checker = EspeakNgChecker()
    assert checker.check_exists() is True
    checker.validate_or_raise()  # should not raise


def test_check_missing(monkeypatch):
    monkeypatch.setattr(shutil, "which", lambda exe: None)
    checker = EspeakNgChecker()
    assert checker.check_exists() is False
    with pytest.raises(RuntimeError):
        checker.validate_or_raise()
