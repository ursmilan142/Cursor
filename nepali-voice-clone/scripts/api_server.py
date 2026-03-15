#!/usr/bin/env python3
"""
Optional FastAPI REST Server for Nepali Voice Cloning TTS.
Exposes HTTP endpoints so any app can request voice synthesis over localhost.

Install extra dependencies:
    pip install fastapi uvicorn[standard] python-multipart

Run:
    python scripts/api_server.py
    # or
    uvicorn scripts.api_server:app --reload
"""

import os
import sys
import uuid
from pathlib import Path

# ---------------------------------------------------------------------------
# Dependency checks
# ---------------------------------------------------------------------------

try:
    from fastapi import FastAPI, HTTPException, UploadFile, File, Form  # type: ignore
    from fastapi.responses import FileResponse  # type: ignore
    import uvicorn  # type: ignore
except ImportError:
    print("❌ FastAPI/uvicorn not found. Install with:")
    print("   pip install fastapi uvicorn[standard] python-multipart")
    sys.exit(1)

# Add scripts/ to path so sibling modules can be imported
_scripts_dir = Path(__file__).resolve().parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

from nepali_voice_clone import NepaliVoiceCloner  # type: ignore[import-not-found]

# ---------------------------------------------------------------------------
# App setup
# ---------------------------------------------------------------------------

OUTPUT_DIR = Path("data/output")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

UPLOAD_DIR = Path("data/uploads")
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

USE_GPU = os.getenv("TTS_USE_GPU", "0") == "1"
_cloner: NepaliVoiceCloner | None = None


def get_cloner() -> NepaliVoiceCloner:
    global _cloner
    if _cloner is None:
        _cloner = NepaliVoiceCloner(gpu=USE_GPU)
    return _cloner


app = FastAPI(
    title="Nepali Voice Cloning TTS API",
    description=(
        "Local, offline Nepali voice cloning TTS powered by Coqui YourTTS. "
        "Upload a voice sample and synthesize Nepali text in your own voice."
    ),
    version="1.0.0",
)

# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------


@app.get("/health", summary="Health check")
def health() -> dict:
    """Return service status."""
    return {"status": "ok", "gpu": USE_GPU}


@app.post("/synthesize", summary="Synthesize text with voice cloning")
async def synthesize(
    text: str = Form(..., description="Text to synthesize (Nepali recommended)"),
    language: str = Form("ne", description="BCP-47 language code"),
    voice_sample: UploadFile = File(..., description="Reference voice WAV file (10-30 s)"),
) -> FileResponse:
    """
    Upload a voice sample and synthesize ``text`` in that voice.

    Returns the generated WAV file as a downloadable response.
    """
    # Save uploaded voice sample
    sample_id = uuid.uuid4().hex
    sample_path = UPLOAD_DIR / f"sample_{sample_id}.wav"
    sample_path.write_bytes(await voice_sample.read())

    output_path = OUTPUT_DIR / f"output_{sample_id}.wav"

    cloner = get_cloner()
    result = cloner.clone_voice(
        text=text,
        reference_audio=str(sample_path),
        output_file=str(output_path),
        language=language,
    )

    # Clean up uploaded sample
    try:
        sample_path.unlink()
    except OSError:
        pass

    if result is None:
        raise HTTPException(status_code=500, detail="Voice synthesis failed. Check server logs.")

    return FileResponse(
        path=str(output_path),
        media_type="audio/wav",
        filename="output.wav",
        headers={"Content-Disposition": 'attachment; filename="output.wav"'},
    )


@app.post("/synthesize/file", summary="Synthesize a text file with voice cloning")
async def synthesize_file(
    text_file: UploadFile = File(..., description="UTF-8 plain-text file"),
    language: str = Form("ne", description="BCP-47 language code"),
    voice_sample: UploadFile = File(..., description="Reference voice WAV file (10-30 s)"),
) -> FileResponse:
    """
    Upload a voice sample and a text file; synthesize the full text.
    """
    sample_id = uuid.uuid4().hex

    sample_path = UPLOAD_DIR / f"sample_{sample_id}.wav"
    sample_path.write_bytes(await voice_sample.read())

    text = (await text_file.read()).decode("utf-8").strip()
    if not text:
        raise HTTPException(status_code=400, detail="Text file is empty.")

    output_path = OUTPUT_DIR / f"output_{sample_id}.wav"

    cloner = get_cloner()
    result = cloner.clone_voice(
        text=text,
        reference_audio=str(sample_path),
        output_file=str(output_path),
        language=language,
    )

    try:
        sample_path.unlink()
    except OSError:
        pass

    if result is None:
        raise HTTPException(status_code=500, detail="Voice synthesis failed. Check server logs.")

    return FileResponse(
        path=str(output_path),
        media_type="audio/wav",
        filename="output.wav",
    )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Start the Nepali TTS API server")
    parser.add_argument("--host", default="127.0.0.1", help="Host to bind (default: 127.0.0.1)")
    parser.add_argument("--port", type=int, default=8000, help="Port to listen on (default: 8000)")
    parser.add_argument("--reload", action="store_true", help="Enable auto-reload (development)")
    args = parser.parse_args()

    print(f"🚀 Starting Nepali TTS API server at http://{args.host}:{args.port}")
    print("   Interactive docs: http://127.0.0.1:8000/docs")
    uvicorn.run("api_server:app", host=args.host, port=args.port, reload=args.reload)
