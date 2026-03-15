#!/usr/bin/env python3
"""
Nepali Voice Cloning TTS — Main CLI
A unified command-line interface that combines voice recording and voice cloning.
"""

import argparse
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Sub-command handlers
# ---------------------------------------------------------------------------

def cmd_record(args: argparse.Namespace) -> int:
    """Handle the 'record' sub-command."""
    # Import here so the module is only needed when recording
    from record_voice import record_audio, play_audio  # type: ignore[import-not-found]

    saved = record_audio(
        duration=args.duration,
        filename=args.output,
        sample_rate=args.sample_rate,
    )
    if args.playback:
        play_audio(saved)
    return 0


def cmd_synthesize(args: argparse.Namespace) -> int:
    """Handle the 'synthesize' sub-command."""
    from nepali_voice_clone import NepaliVoiceCloner  # type: ignore[import-not-found]

    if not args.text and not args.text_file:
        print("❌ Provide either --text or --text-file")
        return 1

    cloner = NepaliVoiceCloner(gpu=args.gpu)

    if args.batch and args.text_file:
        lines = Path(args.text_file).read_text(encoding="utf-8").splitlines()
        texts = [line.strip() for line in lines if line.strip()]
        output_dir = str(Path(args.output).parent)
        cloner.batch_synthesize(texts, args.voice_sample, output_dir, args.language)
    elif args.text_file:
        cloner.synthesize_from_file(args.text_file, args.voice_sample, args.output, args.language)
    else:
        cloner.clone_voice(args.text, args.voice_sample, args.output, args.language)

    return 0


def cmd_run(args: argparse.Namespace) -> int:
    """
    Handle the default 'run' mode: record then synthesize in one step.
    Useful for a quick end-to-end demo.
    """
    from record_voice import record_audio  # type: ignore[import-not-found]
    from nepali_voice_clone import NepaliVoiceCloner  # type: ignore[import-not-found]

    voice_file = record_audio(duration=args.record_duration, filename=args.voice_sample)
    cloner = NepaliVoiceCloner(gpu=args.gpu)

    text = args.text or Path(args.text_file).read_text(encoding="utf-8").strip()
    cloner.clone_voice(text, voice_file, args.output, args.language)
    return 0


# ---------------------------------------------------------------------------
# Parser builders
# ---------------------------------------------------------------------------

def _add_synthesis_args(parser: argparse.ArgumentParser) -> None:
    """Add synthesis-related arguments to a parser."""
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", type=str, help="Text to synthesize")
    source.add_argument("--text-file", type=str, help="Path to UTF-8 text file")

    parser.add_argument(
        "--voice-sample",
        type=str,
        required=True,
        help="Path to reference voice WAV file",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="data/output/output.wav",
        help="Output audio file path (default: data/output/output.wav)",
    )
    parser.add_argument(
        "--language",
        type=str,
        default="hi",
        help="BCP-47 language code (default: hi for Hindi/Nepali; YourTTS supports en, fr-fr, pt-br, hi)",
    )
    parser.add_argument("--gpu", action="store_true", help="Enable GPU acceleration")
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Synthesize each line of --text-file as a separate file",
    )


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="main",
        description="Nepali Voice Cloning TTS — local, offline, Windows-optimized.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Quick Start:
  # 1. Record your voice sample (20 seconds)
  python scripts/main.py record --output my_voice.wav

  # 2. Synthesize Nepali text with your cloned voice
  python scripts/main.py synthesize --text "नमस्ते" --voice-sample my_voice.wav

  # 3. Or do both in one command
  python scripts/main.py run --text "नमस्ते" --voice-sample my_voice.wav
        """,
    )

    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    # --- record ---
    rec = sub.add_parser("record", help="Record a voice sample from the microphone")
    rec.add_argument(
        "--duration", type=int, default=20, help="Max recording duration in seconds (default: 20)"
    )
    rec.add_argument(
        "--output", type=str, default="my_voice.wav", help="Output WAV file (default: my_voice.wav)"
    )
    rec.add_argument("--sample-rate", type=int, default=22050, help="Sample rate in Hz")
    rec.add_argument("--playback", action="store_true", help="Play back after recording")

    # --- synthesize ---
    syn = sub.add_parser("synthesize", help="Synthesize speech with a cloned voice")
    _add_synthesis_args(syn)

    # --- run (end-to-end) ---
    run = sub.add_parser("run", help="Record voice then synthesize in one step")
    run.add_argument(
        "--record-duration", type=int, default=20, help="Recording duration in seconds"
    )
    run.add_argument(
        "--voice-sample",
        type=str,
        default="my_voice.wav",
        help="Voice sample file path (will be recorded here)",
    )
    source = run.add_mutually_exclusive_group(required=True)
    source.add_argument("--text", type=str, help="Text to synthesize")
    source.add_argument("--text-file", type=str, help="Path to UTF-8 text file")
    run.add_argument(
        "--output", type=str, default="data/output/output.wav", help="Output audio file path"
    )
    run.add_argument("--language", type=str, default="hi", help="BCP-47 language code (default: hi)")
    run.add_argument("--gpu", action="store_true", help="Enable GPU acceleration")

    return parser


# ---------------------------------------------------------------------------
# Entry-point
# ---------------------------------------------------------------------------

def main() -> int:
    # Add scripts/ directory to path so sibling modules can be imported
    scripts_dir = Path(__file__).resolve().parent
    if str(scripts_dir) not in sys.path:
        sys.path.insert(0, str(scripts_dir))

    parser = build_parser()
    args = parser.parse_args()

    if args.command == "record":
        return cmd_record(args)
    elif args.command == "synthesize":
        return cmd_synthesize(args)
    elif args.command == "run":
        return cmd_run(args)
    else:
        parser.print_help()
        return 0


if __name__ == "__main__":
    sys.exit(main())
