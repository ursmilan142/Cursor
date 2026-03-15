# Troubleshooting Guide — Nepali Voice Cloning TTS

Common issues and their solutions for Windows users.

---

## Installation Issues

### ❌ `pip install pyaudio` fails on Windows

**Error:**
```
error: Microsoft Visual C++ 14.0 or greater is required
```

**Solutions (try in order):**

1. **Use pipwin:**
   ```cmd
   pip install pipwin
   pipwin install pyaudio
   ```

2. **Download a pre-built wheel:**
   - Go to <https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio>
   - Download the wheel matching your Python version (e.g., `PyAudio‑0.2.14‑cp314‑cp314‑win_amd64.whl`)
   - Install it:
     ```cmd
     pip install PyAudio-0.2.14-cp314-cp314-win_amd64.whl
     ```

3. **Install Visual C++ Build Tools:**
   - Download from <https://visualstudio.microsoft.com/visual-cpp-build-tools/>
   - Select **"Desktop development with C++"** workload
   - Retry `pip install pyaudio`

---

### ❌ `pip install TTS` fails or hangs

**Solutions:**

1. Upgrade pip first:
   ```cmd
   python -m pip install --upgrade pip setuptools wheel
   ```

2. Install with verbose output to see where it fails:
   ```cmd
   pip install TTS -v
   ```

3. Try installing dependencies separately:
   ```cmd
   pip install numpy scipy soundfile librosa
   pip install TTS
   ```

---

### ❌ PyTorch installation fails

```cmd
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
```

If that fails, try the stable release page: <https://pytorch.org/get-started/locally/>

---

### ❌ `setup.ps1` blocked by execution policy

**Error:**
```
File .\setup.ps1 cannot be loaded because running scripts is disabled on this system.
```

**Fix:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```
Then retry `.\setup.ps1`.

---

## Runtime Issues

### ❌ Model download stuck or failing

The Coqui TTS model (~1–2 GB) is downloaded on first use.

**Check:**
- Make sure you have a stable internet connection.
- Make sure you have ~5 GB free disk space.

**Set a custom cache directory:**

**PowerShell:**
```powershell
$env:TTS_HOME = "$env:USERPROFILE\.tts"
python scripts\main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav
```

**CMD:**
```cmd
set TTS_HOME=%USERPROFILE%\.tts
python scripts\main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav
```

**Delete and re-download the model cache:**
```cmd
rmdir /s /q %USERPROFILE%\.tts
```

---

### ❌ `RuntimeError: CUDA out of memory`

You are attempting to use GPU mode on a GPU with insufficient VRAM.

**Fix:** Run in CPU mode (remove `--gpu` flag):
```cmd
python scripts\main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav
```

---

### ❌ Output audio is silent or corrupted

**Possible causes:**

1. **Voice sample too short** — Record at least 10 seconds of clear speech.
2. **Voice sample has background noise** — Re-record in a quiet environment.
3. **Wrong language code** — Make sure `--language ne` is specified for Nepali.
4. **Text encoding issue** — Ensure your Nepali text is saved as UTF-8.

**Verify your voice sample:**
```python
import soundfile as sf
data, sr = sf.read("my_voice.wav")
print(f"Duration: {len(data)/sr:.1f}s  Sample rate: {sr} Hz")
```

---

### ❌ `No module named 'TTS'` (after setup)

The virtual environment may not be activated.

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

---

### ❌ Nepali characters display as `???` in CMD

Windows CMD does not display Unicode by default.

**Fix:**
```cmd
chcp 65001
```
Or switch to PowerShell / Windows Terminal, which support Unicode natively.

---

### ❌ `RecordingError: No input device found`

**Possible causes:**
- Microphone is not plugged in or not set as default.
- Windows privacy settings block microphone access.

**Fix:**
1. Open **Settings → Privacy → Microphone**
2. Enable microphone access for desktop apps.
3. Set your microphone as the **Default Recording Device** in Sound settings.

---

### ❌ Very slow synthesis (CPU mode)

Synthesis on CPU can take 10–60 seconds per sentence depending on your hardware.

**Tips to speed up:**
- Use shorter sentences (under 50 characters).
- Enable GPU if you have a CUDA-capable NVIDIA GPU (see [WINDOWS_GUIDE.md](WINDOWS_GUIDE.md)).
- Close other CPU-intensive applications.

---

## Getting More Help

If your issue is not listed here:

1. Check the [Coqui TTS issues](https://github.com/coqui-ai/TTS/issues) page.
2. Search [Stack Overflow](https://stackoverflow.com/questions/tagged/coqui-tts).
3. Open an issue in this repository with:
   - Your Windows version (`winver`)
   - Python version (`python --version`)
   - The full error message and traceback
