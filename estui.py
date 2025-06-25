# ######################################### #
# Textual User Interface for ESpeak-NG      #
#                                           #
# Copyright 2025 - Oreste Riccardo Natale   #
# Released under MIT License                #
#                                           #
# estui.py                                  #
# ######################################### #

from app.espeak_checker import EspeakNgChecker
from app.espeak_ng_tui_app import EspeakNgTuiApp

if __name__ == "__main__":
    EspeakNgChecker().validate_or_raise()
    EspeakNgTuiApp().run()

