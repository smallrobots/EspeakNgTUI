import pyperclip


def copy_to_clipboard(text: str) -> None:
    """Copy the given text to the system clipboard."""
    pyperclip.copy(text)

