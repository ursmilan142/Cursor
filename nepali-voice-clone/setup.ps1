# PowerShell Setup Script — Nepali Voice Cloning TTS
# Run with: .\setup.ps1
# If execution policy blocks the script:
#   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

param(
    [switch]$SkipVenv,
    [switch]$GPU
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "  Nepali Voice Cloning TTS — Windows PowerShell Setup" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# ---- Verify Python ----
try {
    $pythonVersion = (python --version 2>&1).ToString()
    Write-Host "✅ Found $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Python not found. Download from https://python.org" -ForegroundColor Red
    exit 1
}

# ---- Create virtual environment ----
if (-not $SkipVenv) {
    if (-not (Test-Path "venv")) {
        Write-Host "📦 Creating virtual environment..." -ForegroundColor Yellow
        python -m venv venv
    } else {
        Write-Host "✅ Virtual environment already exists." -ForegroundColor Green
    }

    Write-Host "🔄 Activating virtual environment..." -ForegroundColor Yellow
    & ".\venv\Scripts\Activate.ps1"
}

# ---- Upgrade pip ----
Write-Host "⬆️  Upgrading pip, setuptools, wheel..." -ForegroundColor Yellow
python -m pip install --upgrade pip setuptools wheel

# ---- Install PyTorch (CPU unless --GPU flag) ----
if ($GPU) {
    Write-Host "🚀 Installing PyTorch with CUDA support..." -ForegroundColor Yellow
    pip install "torch==2.6.0+cu121" "torchaudio==2.6.0+cu121" --index-url https://download.pytorch.org/whl/cu121
} else {
    Write-Host "💻 Installing PyTorch (CPU build)..." -ForegroundColor Yellow
    pip install "torch==2.6.0+cpu" "torchaudio==2.6.0+cpu" --index-url https://download.pytorch.org/whl/cpu
}

# ---- Install remaining dependencies ----
Write-Host "📦 Installing remaining dependencies..." -ForegroundColor Yellow
pip install TTS numpy scipy soundfile librosa pydub

# ---- Install PyAudio (with pipwin fallback) ----
Write-Host "🎤 Installing PyAudio..." -ForegroundColor Yellow
$pyaudioOk = $false
try {
    pip install pyaudio
    $pyaudioOk = $true
} catch {
    Write-Host "⚠️  Direct PyAudio install failed. Trying pipwin..." -ForegroundColor Yellow
}

if (-not $pyaudioOk) {
    try {
        pip install pipwin
        pipwin install pyaudio
        $pyaudioOk = $true
    } catch {
        Write-Host "⚠️  PyAudio could not be installed automatically." -ForegroundColor Yellow
        Write-Host "   Voice recording will not be available." -ForegroundColor Yellow
        Write-Host "   Download PyAudio wheel manually from:" -ForegroundColor Yellow
        Write-Host "   https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio" -ForegroundColor Yellow
    }
}

# ---- Create output directory ----
New-Item -ItemType Directory -Force -Path "data\output" | Out-Null
Write-Host "✅ Output directory ready: data\output" -ForegroundColor Green

Write-Host ""
Write-Host "============================================================" -ForegroundColor Green
Write-Host "  ✅ Setup complete!" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "  1. Record your voice:" -ForegroundColor White
Write-Host "       python scripts\record_voice.py" -ForegroundColor Yellow
Write-Host ""
Write-Host "  2. Synthesize Nepali text:" -ForegroundColor White
Write-Host '       python scripts\main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav' -ForegroundColor Yellow
Write-Host ""
Write-Host "  See README.md and WINDOWS_GUIDE.md for more details." -ForegroundColor Cyan
Write-Host ""
