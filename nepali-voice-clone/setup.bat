@echo off
REM ============================================================
REM  Nepali Voice Cloning TTS — Windows CMD Setup Script
REM  Run with: setup.bat
REM ============================================================

setlocal enabledelayedexpansion
title Nepali Voice Cloning TTS Setup

echo.
echo ============================================================
echo   Nepali Voice Cloning TTS -- Windows CMD Setup
echo ============================================================
echo.

REM ---- Verify Python ----
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found. Download from https://python.org
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Found %PYVER%

REM ---- Create virtual environment ----
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        pause
        exit /b 1
    )
) else (
    echo [OK] Virtual environment already exists.
)

REM ---- Activate virtual environment ----
echo [INFO] Activating virtual environment...
call venv\Scripts\activate.bat

REM ---- Upgrade pip ----
echo [INFO] Upgrading pip, setuptools, wheel...
python -m pip install --upgrade pip setuptools wheel

REM ---- Install PyTorch (CPU) ----
echo [INFO] Installing PyTorch (CPU build for Windows compatibility)...
pip install torch torchaudio --index-url https://download.pytorch.org/whl/cpu
if errorlevel 1 (
    echo [ERROR] PyTorch installation failed. Check your internet connection.
    pause
    exit /b 1
)

REM ---- Install remaining dependencies ----
echo [INFO] Installing TTS and audio dependencies...
pip install TTS numpy scipy soundfile librosa pydub
if errorlevel 1 (
    echo [WARNING] Some packages failed to install. Check the error messages above.
)

REM ---- Install PyAudio ----
echo [INFO] Installing PyAudio...
pip install pyaudio
if errorlevel 1 (
    echo [WARNING] PyAudio direct install failed. Trying pipwin...
    pip install pipwin
    pipwin install pyaudio
    if errorlevel 1 (
        echo [WARNING] PyAudio could not be installed automatically.
        echo           Voice recording will not be available.
        echo           Download PyAudio wheel manually:
        echo           https://www.lfd.uci.edu/~gohlke/pythonlibs/#pyaudio
    )
)

REM ---- Create output directory ----
if not exist "data\output" mkdir data\output
echo [OK] Output directory ready: data\output

echo.
echo ============================================================
echo   Setup complete!
echo ============================================================
echo.
echo Next steps:
echo   1. Record your voice:
echo        python scripts\record_voice.py
echo.
echo   2. Synthesize Nepali text:
echo        python scripts\main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav
echo.
echo   See README.md and WINDOWS_GUIDE.md for more details.
echo.
pause
