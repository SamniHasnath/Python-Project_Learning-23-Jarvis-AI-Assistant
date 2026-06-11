# Jarvis Assistant Desktop

A Python-based voice assistant for desktop. Talk to it, and it'll tell you the time, fetch the weather, crack a joke, open apps, search the web, play music, and more — with an AI fallback (OpenAI) for everything else.

<img width="800" height="600" alt="image" src="https://github.com/user-attachments/assets/6ced6ead-d72f-4cb5-b388-a306c0d0f4e2" />

## Features

- **Voice in / voice out** — speech recognition for input, `pyttsx3` for spoken replies
- **Time & date** — "what's the time", "what's the date"
- **System info** — battery status, CPU/RAM/disk usage, IP address
- **Web & search** — Google search, Wikipedia summaries, YouTube playback
- **Media** — play/stop local music from `assets/music`
- **Apps** — open common apps (Notepad, Calculator, browsers, VS Code, Spotify, etc.)
- **Utilities** — screenshots, timers, coin flip, dice roll
- **Fun & info** — jokes, motivational quotes, BBC news headlines, weather
- **AI fallback** — anything not matched by a built-in command is sent to OpenAI's `gpt-3.5-turbo`

## Project Structure

```
jarvis-assistant-desktop/
├── main.py            # Entry point: TTS/STT setup, AI fallback, main loop
├── commands.py        # All command implementations + command router
├── config.py          # Assistant settings, voice config, .env loading
├── requirements.txt   # Python dependencies
├── assets/
│   └── music/         # Local music files for the "play music" command
└── screenshots/        # Saved screenshots from the "take a screenshot" command
```

## Requirements

- Python 3.10+
- A working microphone and speakers
- Windows (uses Windows-specific commands like `notepad.exe`, `start ms-settings:`, etc.)

## Installation

1. Clone the repository
   ```bash
   git clone <repo-url>
   cd jarvis-assistant-desktop
   ```

2. Create and activate a virtual environment (recommended)
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

   For battery/CPU/RAM/disk info, also install:
   ```bash
   pip install psutil
   ```

4. (Optional) Create a `.env` file in the project root for AI fallback replies:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   ```

## Usage

Run the assistant:
```bash
python main.py
```

Jarvis will greet you and start listening. Speak a command — for example:

- "What's the time?"
- "What's the weather in London?"
- "Tell me a joke"
- "Open notepad"
- "Play music"
- "Set timer for 5 minutes"
- "What can you do?"
- "Goodbye" (to exit)

If a command isn't recognized, it's passed to the AI fallback (requires `OPENAI_API_KEY`).

## Configuration

Edit `config.py` to customize:

- `ASSISTANT_NAME` — the assistant's name (default: `Jarvis`)
- `VOICE_RATE`, `VOICE_VOLUME`, `VOICE_INDEX` — text-to-speech voice settings
- `MUSIC_DIR` — folder scanned for playable music files

## License

This project is for personal/educational use.
