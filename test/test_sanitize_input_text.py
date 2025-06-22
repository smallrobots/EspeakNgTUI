# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# test_sanitize_input_text.py               #
# ######################################### #

import re
import pytest

# Funzione da testare (estratta staticamente per test)
def sanitize_input_text(text: str) -> str:
    """Remove ANSI sequences and non-printable characters from text."""
    text = re.sub(r'\x1b\[[0-9;]*[A-Za-z]', '', text)  # ANSI
    text = ''.join(c for c in text if c.isprintable())  # Non-printables
    return text

# Test cases
test_cases = [
    # (input, expected_output)
    ("Hello world", "Hello world"),
    ("\x1b[31mRed Text\x1b[0m", "Red Text"),  # ANSI color codes removed
    ("Printable and \x07 bell", "Printable and  bell"),  # \x07 = BEL (non-printable)
    ("\x1b[999;999HCursorMove", "CursorMove"),  # another ANSI sequence
    ("Only printables! 😃", "Only printables! 😃"),  # Emoji should stay (printable)
    ("Line\u2028Separator", "LineSeparator"),  # Unicode line separator
]

@pytest.mark.parametrize("raw,expected", test_cases)
def test_sanitize_input_text(raw, expected):
    assert sanitize_input_text(raw) == expected
