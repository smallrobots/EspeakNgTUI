# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# espeak_checker.py                         #
# ######################################### #

import shutil

class EspeakNgChecker:
    """Utility class to verify that the ``espeak-ng`` command is available."""

    @staticmethod
    def check_exists() -> bool:
        """Return ``True`` if ``espeak-ng`` is found in ``PATH``."""
        return shutil.which("espeak-ng") is not None

    def validate_or_raise(self) -> None:
        """Raise ``RuntimeError`` if ``espeak-ng`` is not available."""
        if not self.check_exists():
            raise RuntimeError("espeak-ng executable not found")

