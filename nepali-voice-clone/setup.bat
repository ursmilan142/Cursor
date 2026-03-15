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

REM ---- Verify py ----
py --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] py not found. Download Python 3.11 from https://python.org/downloads/
    pause
    exit /b 1
)
for /f "tokens=*" %%i in ('py --version 2^>^&1') do set PYVER=%%i
echo [OK] Found %PYVER%
echo [NOTE] Python 3.11 is recommended. TTS==0.22.0 requires Python ^<=3.11.

REM ---- Create virtual environment ----
if not exist "venv" (
    echo [INFO] Creating virtual environment...
    py -m venv venv
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
py -m pip install --upgrade pip setuptools wheel

REM ---- Install PyTorch (CPU) ----
echo [INFO] Installing PyTorch (CPU build for Windows compatibility)...
pip install "torch==2.6.0+cpu" "torchaudio==2.6.0+cpu" --index-url https://download.pytorch.org/whl/cpu
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

REM ---- Install sounddevice ----
echo [INFO] Installing sounddevice (cross-platform audio, no build tools needed)...
pip install sounddevice
if errorlevel 1 (
    echo [WARNING] sounddevice could not be installed.
    echo           Voice recording will not be available.
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
echo        py scripts\record_voice.py
echo.
echo   2. Synthesize Nepali text (using Hindi language code as fallback):
echo        py scripts\main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav --language hi
echo.
echo   See README.md and WINDOWS_GUIDE.md for more details.
echo.
pause
