#!/usr/bin/env python3
"""
Voice Recording Utility
Records audio from the default microphone and saves it as a WAV file.
Designed for capturing voice samples used by the voice cloning engine.
"""

import argparse
import sys
import wave
from pathlib import Path


def record_audio(
    duration: int = 20,
    filename: str = "my_voice.wav",
    sample_rate: int = 22050,
    channels: int = 1,
) -> str:
    """
    Record audio from the default microphone.

    Args:
        duration: Maximum recording duration in seconds.
        filename: Output WAV file path.
        sample_rate: Sample rate in Hz (22 050 Hz recommended for TTS models).
        channels: Number of audio channels (1 = mono).

    Returns:
        Path to the saved WAV file.
    """
    try:
        import pyaudio  # type: ignore[import-untyped]
    except ImportError:
        print("❌ PyAudio not found.")
        print("   Install it with one of the following commands:")
        print("   pip install pyaudio")
        print("   -- or, on Windows if the above fails --")
        print("   pip install pipwin && pipwin install pyaudio")
        sys.exit(1)

    CHUNK = 1024
    FORMAT = pyaudio.paInt16

    p = pyaudio.PyAudio()

    print(f"\n🎤 Recording up to {duration} seconds of audio...")
    print("   Speak clearly into your microphone.")
    print("   Press Ctrl+C to stop recording early.\n")

    stream = p.open(
        format=FORMAT,
        channels=channels,
        rate=sample_rate,
        input=True,
        frames_per_buffer=CHUNK,
    )

    frames: list[bytes] = []
    total_chunks = int(sample_rate / CHUNK * duration)

    try:
        for i in range(total_chunks):
            data = stream.read(CHUNK, exception_on_overflow=False)
            frames.append(data)
            elapsed = i * CHUNK / sample_rate
            remaining = duration - elapsed
            sys.stdout.write(f"\r⏱️  {elapsed:5.1f}s elapsed  |  {remaining:5.1f}s remaining ")
            sys.stdout.flush()
    except KeyboardInterrupt:
        print("\n\n⏹️  Recording stopped early by user.")

    print()
    stream.stop_stream()
    stream.close()
    p.terminate()

    # Save as WAV
    out_path = Path(filename)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with wave.open(str(out_path), "wb") as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(sample_rate)
        wf.writeframes(b"".join(frames))

    size_kb = out_path.stat().st_size / 1024
    print(f"✅ Recording saved: {out_path}  ({size_kb:.1f} KB)")
    return str(out_path)


def play_audio(filename: str) -> None:
    """Play back a WAV file so the user can verify the recording."""
    try:
        import pyaudio  # type: ignore[import-untyped]
    except ImportError:
        print("⚠️  PyAudio not available — cannot play back audio.")
        return

    p = pyaudio.PyAudio()
    try:
        with wave.open(filename, "rb") as wf:
            stream = p.open(
                format=p.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True,
            )
            print(f"\n▶️  Playing back: {filename}")
            data = wf.readframes(1024)
            while data:
                stream.write(data)
                data = wf.readframes(1024)
            stream.stop_stream()
            stream.close()
    except FileNotFoundError:
        print(f"❌ File not found: {filename}")
    finally:
        p.terminate()


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="record_voice",
        description="Record a voice sample from your microphone.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Record 20 seconds (default)
  python record_voice.py

  # Record 30 seconds and save to a specific file
  python record_voice.py --duration 30 --output samples/my_voice.wav

  # Record and immediately play back to verify
  python record_voice.py --playback
        """,
    )
    parser.add_argument(
        "--duration", type=int, default=20, help="Max recording duration in seconds (default: 20)"
    )
    parser.add_argument(
        "--output",
        type=str,
        default="my_voice.wav",
        help="Output WAV file path (default: my_voice.wav)",
    )
    parser.add_argument(
        "--sample-rate",
        type=int,
        default=22050,
        help="Sample rate in Hz (default: 22050)",
    )
    parser.add_argument(
        "--playback",
        action="store_true",
        help="Play back the recording after saving",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    saved_file = record_audio(
        duration=args.duration,
        filename=args.output,
        sample_rate=args.sample_rate,
    )

    if args.playback:
        play_audio(saved_file)

    print("\n📌 Next step — synthesize Nepali speech with your voice:")
    print(f'   python scripts/main.py --text "नमस्ते" --voice-sample {saved_file}')
    return 0


if __name__ == "__main__":
    sys.exit(main())
