# ESpeak-ng TUI

ESpeak-ng TUI is a small Textual application that lets you try the `espeak-ng` text-to-speech engine from a terminal interface. The user can adjust common speech parameters, enter text, preview the generated command and play it directly.

## Features
- **Parameter Controls** – Change voice, speed, pitch, volume and word gap.
- **Text Input and Playback** – Type the sentence to synthesize and press **Play** to hear the result.
- **Command Preview** – The full `espeak-ng` command is displayed so it can be copied or executed manually.
- **Message List** – Store multiple messages with their parameters and recall them quickly.

## Requirements
- Python 3.10+
- `textual` and `textual-dev` libraries
- `espeak-ng` available in `PATH`

Install dependencies with `pip install -r requirements.txt`.

## Usage
Run the application with:

```bash
python estui.py [presets.json]
```

If no file is provided, `messages_preset.json` is used.

Use the controls on the left to set parameters and type text. The right side lists stored messages. Select a message to load its values or press **Add** to store the current one. Press **Play** to run `espeak-ng` with the selected options.

## Development
Unit tests are located in the `test/` directory and can be executed with `pytest`.

Contributions are welcome!
