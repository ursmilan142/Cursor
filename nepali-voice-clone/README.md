# Nepali Voice Cloning TTS

A **fully local, offline** Nepali voice cloning text-to-speech system for Windows, powered by [Coqui TTS (YourTTS)](https://github.com/coqui-ai/TTS). Clone your own voice and synthesize any Nepali text — no cloud, no API keys required.

## Features

- 🎤 **Voice Cloning** — Clone your voice from a 10–30 second sample
- 🇳🇵 **Nepali TTS** — Synthesize Nepali (and other multilingual) text
- 💻 **Fully Local** — Runs entirely on your machine; no internet after model download
- 🪟 **Windows-Optimized** — Setup scripts for PowerShell, CMD, and Git Bash
- 🐍 **Python 3.14 Compatible** — Tested on Python 3.14
- ⚡ **CPU Default** — Works without a GPU; optional GPU acceleration
- 🔄 **Batch Processing** — Synthesize multiple sentences at once
- 🌐 **Optional REST API** — FastAPI server for programmatic access

## Quick Start

### 1 — Clone the repository

```bash
git clone https://github.com/ursmilan142/Cursor.git
cd Cursor/nepali-voice-clone
```

### 2 — Run the setup script

**PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
.\setup.ps1
```

**CMD:**
```cmd
setup.bat
```

**Git Bash:**
```bash
bash setup.sh
```

### 3 — Record your voice sample

```bash
python scripts/record_voice.py
```

Speak clearly for 15–30 seconds. The recording is saved as `my_voice.wav`.

### 4 — Synthesize Nepali speech

```bash
python scripts/main.py synthesize \
    --text "नमस्ते, मेरो नाम उर्स हो।" \
    --voice-sample my_voice.wav \
    --output data/output/hello.wav
```

## Project Structure

```
nepali-voice-clone/
├── scripts/
│   ├── main.py                 # Unified CLI (record + synthesize)
│   ├── nepali_voice_clone.py   # Core voice cloning engine
│   ├── record_voice.py         # Microphone recording utility
│   └── api_server.py           # Optional FastAPI REST server
├── data/
│   ├── nepali_samples.txt      # Sample Nepali sentences
│   └── output/                 # Generated audio files (git-ignored)
├── setup.ps1                   # PowerShell setup
├── setup.bat                   # CMD setup
├── setup.sh                    # Git Bash setup
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── WINDOWS_GUIDE.md            # Detailed Windows walkthrough
├── TROUBLESHOOTING.md          # Common issues and fixes
└── .gitignore
```

## CLI Reference

### `main.py record` — Record a voice sample

```
python scripts/main.py record [--duration N] [--output FILE] [--playback]
```

| Flag | Default | Description |
|---|---|---|
| `--duration` | `20` | Max recording length in seconds |
| `--output` | `my_voice.wav` | Output WAV file |
| `--playback` | off | Play back after recording |

### `main.py synthesize` — Synthesize speech

```
python scripts/main.py synthesize --voice-sample FILE (--text TEXT | --text-file FILE) [options]
```

| Flag | Default | Description |
|---|---|---|
| `--text` | — | Inline text to synthesize |
| `--text-file` | — | Path to UTF-8 text file |
| `--voice-sample` | *(required)* | Reference voice WAV file |
| `--output` | `data/output/output.wav` | Output audio file |
| `--language` | `ne` | BCP-47 language code |
| `--gpu` | off | Enable GPU acceleration |
| `--batch` | off | One output file per line in `--text-file` |

### `main.py run` — Record then synthesize in one step

```
python scripts/main.py run --text "नमस्ते" [--record-duration N] [--voice-sample FILE]
```

## Batch Processing

Synthesize every line of a text file as a separate audio file:

```bash
python scripts/main.py synthesize \
    --text-file data/nepali_samples.txt \
    --voice-sample my_voice.wav \
    --output data/output/batch.wav \
    --batch
```

Output files are named `output_001.wav`, `output_002.wav`, etc.

## Optional REST API

```bash
pip install fastapi "uvicorn[standard]" python-multipart
python scripts/api_server.py
```

Then open `http://127.0.0.1:8000/docs` for the interactive Swagger UI.

## First-Run Notes

- The TTS model (~1–2 GB) is downloaded on first use and cached in `%USERPROFILE%\.tts` (Windows).
- An internet connection is only needed for the initial model download.
- Subsequent runs are fully offline.

## Requirements

- Python 3.9+ (tested with 3.14)
- ~5 GB free disk space (model cache + dependencies)
- Microphone (for voice recording)
- Windows 10/11 (also works on Linux/macOS)

## License

This project is released under the [MIT License](../LICENSE).

## See Also

- [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md) — Step-by-step Windows setup walkthrough
- [TROUBLESHOOTING.md](TROUBLESHOOTING.md) — Solutions to common problems
- [Coqui TTS](https://github.com/coqui-ai/TTS) — Upstream TTS library
