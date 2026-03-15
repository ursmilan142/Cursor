#!/usr/bin/env python3
"""
Nepali Voice Cloning Engine
Core module for cloning voices and synthesizing Nepali text using
Indic Parler TTS — a state-of-the-art model from AI4Bharat specifically
trained for Indian languages including Nepali (नेपाली).
Fully local/offline operation after the initial model download.
"""

import sys
import argparse
from pathlib import Path


class NepaliVoiceCloner:
    """Voice cloning engine using Indic Parler TTS (AI4Bharat)."""

    def __init__(self, gpu: bool = False):
        """
        Initialize Indic Parler TTS with Nepali language support.

        Args:
            gpu: Use GPU acceleration if available (default: False for CPU)
        """
        try:
            from indic_parler_tts import IndicParlerTTS  # type: ignore[import-untyped]
        except ImportError:
            print("❌ indic-parler-tts library not found.")
            print("   Run setup script or: pip install git+https://github.com/ai4bharat/indic-parler-tts.git")
            sys.exit(1)

        device = "cuda" if gpu else "cpu"
        print(f"🔄 Loading Indic Parler TTS model for Nepali (device: {device})...")
        print("   First run downloads the model — this may take a few minutes.")
        self.tts = IndicParlerTTS(
            language="ne",  # Nepali
            device=device,
        )
        self.gpu = gpu
        print("✅ Indic Parler TTS model loaded successfully!")

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def clone_voice(
        self,
        text: str,
        reference_audio: str,
        output_file: str = "output.wav",
        language: str = "ne",
    ) -> str | None:
        """
        Clone voice and synthesize text using Indic Parler TTS.

        Args:
            text: Text to synthesize (Nepali Devanagari script).
            reference_audio: Path to reference voice sample (10-30 seconds recommended).
            output_file: Path for the generated audio file.
            language: Language code — ``"ne"`` for Nepali (default).

        Returns:
            Path to the generated file, or ``None`` on failure.
        """
        if not Path(reference_audio).is_file():
            print(f"❌ Reference audio not found: {reference_audio}")
            return None

        # Ensure output directory exists
        Path(output_file).parent.mkdir(parents=True, exist_ok=True)

        print(f"🎤 Cloning voice from: {reference_audio}")
        print(f"📝 Synthesizing: {text}")
        print(f"🌐 Language: {language}")

        try:
            self.tts.synthesize(
                text=text,
                speaker_wav=reference_audio,
                output_path=output_file,
            )
            print(f"✅ Successfully created: {output_file}")
            return output_file
        except Exception as exc:  # noqa: BLE001
            print(f"❌ Synthesis error: {exc}")
            return None

    def synthesize_from_file(
        self,
        text_file: str,
        reference_audio: str,
        output_file: str = "output.wav",
        language: str = "ne",
    ) -> str | None:
        """
        Synthesize speech from a plain-text file.

        Args:
            text_file: Path to a UTF-8 encoded text file.
            reference_audio: Path to reference voice sample.
            output_file: Path for the generated audio file.
            language: Language code.

        Returns:
            Path to the generated file, or ``None`` on failure.
        """
        try:
            text = Path(text_file).read_text(encoding="utf-8").strip()
        except FileNotFoundError:
            print(f"❌ Text file not found: {text_file}")
            return None
        except OSError as exc:
            print(f"❌ Could not read text file: {exc}")
            return None

        if not text:
            print("❌ Text file is empty.")
            return None

        return self.clone_voice(text, reference_audio, output_file, language)

    def batch_synthesize(
        self,
        texts: list[str],
        reference_audio: str,
        output_dir: str = "data/output",
        language: str = "ne",
        prefix: str = "output",
    ) -> list[str]:
        """
        Synthesize multiple texts with the same cloned voice.

        Args:
            texts: List of texts to synthesize.
            reference_audio: Path to reference voice sample.
            output_dir: Directory for generated audio files.
            language: Language code.
            prefix: Filename prefix for output files.

        Returns:
            List of paths to successfully generated files.
        """
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        results: list[str] = []

        for idx, text in enumerate(texts, start=1):
            out_file = str(Path(output_dir) / f"{prefix}_{idx:03d}.wav")
            print(f"\n[{idx}/{len(texts)}] Processing: {text[:50]}...")
            result = self.clone_voice(text, reference_audio, out_file, language)
            if result:
                results.append(result)

        print(f"\n✅ Batch complete: {len(results)}/{len(texts)} files generated.")
        return results


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="nepali_voice_clone",
        description="Nepali Voice Cloning TTS — powered by Indic Parler TTS (AI4Bharat).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Synthesize a single line of Nepali text
  python nepali_voice_clone.py --text "नमस्ते" --voice-sample my_voice.wav

  # Synthesize from a text file
  python nepali_voice_clone.py --text-file data/nepali_samples.txt --voice-sample my_voice.wav

  # Batch processing (one line per output)
  python nepali_voice_clone.py --batch --text-file data/nepali_samples.txt --voice-sample my_voice.wav

  # Use GPU
  python nepali_voice_clone.py --text "नमस्ते" --voice-sample my_voice.wav --gpu
        """,
    )
    source = parser.add_mutually_exclusive_group()
    source.add_argument("--text", type=str, help="Text to synthesize")
    source.add_argument("--text-file", type=str, help="Path to UTF-8 text file")

    parser.add_argument(
        "--voice-sample", type=str, required=True, help="Path to reference voice WAV file"
    )
    parser.add_argument(
        "--output", type=str, default="data/output/output.wav", help="Output audio file path"
    )
    parser.add_argument(
        "--language", type=str, default="ne", help="Language code (default: ne for Nepali)"
    )
    parser.add_argument(
        "--gpu", action="store_true", help="Enable GPU acceleration (default: CPU)"
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Treat each line of --text-file as a separate synthesis job",
    )
    return parser


def main() -> int:
    parser = _build_parser()
    args = parser.parse_args()

    if not args.text and not args.text_file:
        parser.error("Provide either --text or --text-file")

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


if __name__ == "__main__":
    sys.exit(main())

