import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from clipboard_util import copy_to_clipboard
import pyperclip


def test_copy_to_clipboard(monkeypatch):
    captured = {}

    def fake_copy(text):
        captured['text'] = text

    monkeypatch.setattr(pyperclip, "copy", fake_copy)
    copy_to_clipboard("hello")
    assert captured['text'] == "hello"

