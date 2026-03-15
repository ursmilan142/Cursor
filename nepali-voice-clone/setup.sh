#!/usr/bin/env bash
# ============================================================
#  Nepali Voice Cloning TTS — Git Bash / WSL Setup Script
#  Run with: bash setup.sh
# ============================================================

set -e

# Colour helpers (fall back gracefully if tput is unavailable)
GREEN=""
YELLOW=""
RED=""
CYAN=""
RESET=""
if command -v tput &>/dev/null && tput colors &>/dev/null; then
    GREEN=$(tput setaf 2)
    YELLOW=$(tput setaf 3)
    RED=$(tput setaf 1)
    CYAN=$(tput setaf 6)
    RESET=$(tput sgr0)
fi

info()    { echo "${CYAN}[INFO]${RESET}  $*"; }
success() { echo "${GREEN}[OK]${RESET}    $*"; }
warn()    { echo "${YELLOW}[WARN]${RESET}  $*"; }
error()   { echo "${RED}[ERROR]${RESET} $*"; exit 1; }

echo ""
echo "${CYAN}============================================================${RESET}"
echo "${CYAN}  Nepali Voice Cloning TTS — Git Bash Setup${RESET}"
echo "${CYAN}============================================================${RESET}"
echo ""

# ---- Verify Python ----
command -v python &>/dev/null || error "Python not found. Install from https://python.org"
PYVER=$(python --version 2>&1)
success "Found $PYVER"

# ---- Create and activate virtual environment ----
if [ ! -d "venv" ]; then
    info "Creating virtual environment..."
    python -m venv venv
fi
info "Activating virtual environment..."
# Git Bash on Windows uses Scripts/; Linux/macOS uses bin/
if [ -f "venv/Scripts/activate" ]; then
    # shellcheck disable=SC1091
    source venv/Scripts/activate
else
    # shellcheck disable=SC1091
    source venv/bin/activate
fi
success "Virtual environment active."

# ---- Upgrade pip ----
info "Upgrading pip, setuptools, wheel..."
python -m pip install --upgrade pip setuptools wheel

# ---- Install PyTorch (CPU) ----
info "Installing PyTorch (CPU build)..."
pip install "torch==2.6.0+cpu" "torchaudio==2.6.0+cpu" --index-url https://download.pytorch.org/whl/cpu

# ---- Install remaining dependencies ----
info "Installing TTS and audio dependencies..."
pip install TTS numpy scipy soundfile librosa pydub

# ---- Install PyAudio ----
info "Installing PyAudio..."
if ! pip install pyaudio 2>/dev/null; then
    warn "Direct PyAudio install failed. Trying pipwin..."
    if pip install pipwin 2>/dev/null && pipwin install pyaudio 2>/dev/null; then
        success "PyAudio installed via pipwin."
    else
        warn "PyAudio could not be installed automatically."
        warn "Voice recording will not be available."
        warn "Download a pre-built wheel from:"
        warn "  https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio"
    fi
else
    success "PyAudio installed."
fi

# ---- Create output directory ----
mkdir -p data/output
success "Output directory ready: data/output"

echo ""
echo "${GREEN}============================================================${RESET}"
echo "${GREEN}  ✅ Setup complete!${RESET}"
echo "${GREEN}============================================================${RESET}"
echo ""
echo "Next steps:"
echo "  1. Record your voice:"
echo "       python scripts/record_voice.py"
echo ""
echo "  2. Synthesize Nepali text:"
echo '       python scripts/main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav'
echo ""
echo "  See README.md and WINDOWS_GUIDE.md for more details."
echo ""
