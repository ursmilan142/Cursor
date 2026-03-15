# Windows Setup Guide — Nepali Voice Cloning TTS

This guide walks you through a complete, step-by-step installation on **Windows 10/11** using Python 3.14.

---

## Prerequisites

| Requirement | Notes |
|---|---|
| **Python 3.9+** (3.14 recommended) | Download from [python.org](https://python.org/downloads/) |
| **Git** | Download from [git-scm.com](https://git-scm.com/) |
| **~5 GB free disk space** | For model cache and dependencies |
| **Microphone** | For recording your voice sample |
| **Internet connection** | Only needed for the first model download (~1-2 GB) |

---

## Step 1 — Install Python 3.14

1. Go to <https://python.org/downloads/>
2. Download the **Windows installer (64-bit)**
3. Run the installer and **check "Add Python to PATH"**
4. Click **Install Now**

Verify the installation:
```cmd
python --version
```
Expected output: `Python 3.14.x`

---

## Step 2 — Get the Project

### Option A — Clone with Git

```cmd
git clone https://github.com/ursmilan142/Cursor.git
cd Cursor\nepali-voice-clone
```

### Option B — Download ZIP

1. Go to <https://github.com/ursmilan142/Cursor>
2. Click **Code → Download ZIP**
3. Extract and open a terminal in `Cursor\nepali-voice-clone`

---

## Step 3 — Run the Setup Script

Choose the shell you prefer.

### PowerShell

```powershell
# Allow local scripts (one-time)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Run setup
.\setup.ps1
```

### CMD

```cmd
setup.bat
```

### Git Bash

```bash
bash setup.sh
```

The setup script will:
1. Create a Python virtual environment (`venv/`)
2. Upgrade `pip`, `setuptools`, and `wheel`
3. Install PyTorch (CPU build)
4. Install Coqui TTS and audio libraries
5. Install PyAudio (with `pipwin` fallback)

---

## Step 4 — Activate the Virtual Environment

After setup, activate the virtual environment before each session.

**PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

**CMD:**
```cmd
venv\Scripts\activate.bat
```

**Git Bash:**
```bash
source venv/Scripts/activate
```

Your prompt will show `(venv)` when active.

---

## Step 5 — Record Your Voice Sample

```cmd
python scripts\record_voice.py
```

- Speak clearly for **15–30 seconds**
- Read the sample sentences in `data\nepali_samples.txt` aloud
- Press **Ctrl+C** to stop early
- The recording is saved as `my_voice.wav`

**Tips for a good voice sample:**
- Use a quiet room
- Hold the microphone 15–20 cm from your mouth
- Speak at a natural pace and volume
- Avoid background noise (fans, TV, traffic)

---

## Step 6 — Synthesize Nepali Speech

**PowerShell / CMD:**
```cmd
python scripts\main.py synthesize ^
    --text "नमस्ते, मेरो नाम उर्स हो। यो एक परीक्षण हो।" ^
    --voice-sample my_voice.wav ^
    --output data\output\hello.wav
```

**Git Bash:**
```bash
python scripts/main.py synthesize \
    --text "नमस्ते, मेरो नाम उर्स हो।" \
    --voice-sample my_voice.wav \
    --output data/output/hello.wav
```

> **First run:** The TTS model (~1–2 GB) will be downloaded automatically.
> Subsequent runs are fully offline.

---

## Step 7 — Play the Output

The output WAV file can be played with any media player (Windows Media Player, VLC, etc.):

```cmd
start data\output\hello.wav
```

Or from Git Bash:
```bash
start data/output/hello.wav
```

---

## Batch Processing

To synthesize all sample sentences at once:

**CMD:**
```cmd
python scripts\main.py synthesize ^
    --text-file data\nepali_samples.txt ^
    --voice-sample my_voice.wav ^
    --output data\output\batch.wav ^
    --batch
```

Output files: `data\output\batch_001.wav`, `batch_002.wav`, …

---

## GPU Acceleration (Optional)

If you have an NVIDIA GPU with CUDA support:

```powershell
# Reinstall PyTorch with CUDA
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cu121

# Use GPU for synthesis
python scripts\main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav --gpu
```

---

## Uninstall / Clean Up

To remove the virtual environment and cached models:

```cmd
rmdir /s /q venv
rmdir /s /q %USERPROFILE%\.tts
```

---

## Next Steps

- See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) if you encounter any issues
- Edit `data\nepali_samples.txt` to add your own Nepali sentences
- Use the optional REST API (`scripts\api_server.py`) for programmatic access
