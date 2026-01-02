"""
CLI tool for audio transcription.

Usage:
    python scripts/transcribe.py audio.wav
    python scripts/transcribe.py audio.mp3 --model base.en
"""

import sys
import argparse
import logging
from pathlib import Path


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Transcribe audio files to text using Whisper AI"
    )
    
    parser.add_argument(
        "audio_file",
        help="Path to audio file (WAV, MP3, M4A, FLAC, etc.)"
    )
    
    parser.add_argument(
        "--model",
        default="tiny.en",
        choices=["tiny.en", "tiny", "base.en", "base", "small.en", "small", "medium", "large-v3"],
        help="Whisper model to use (default: tiny.en)"
    )
    
    parser.add_argument(
        "--language",
        default="en",
        help="Language code (e.g., en, es, fr) or 'auto' for detection"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path (optional, will save transcript)"
    )
    
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    level = logging.DEBUG if args.verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    audio_path = Path(args.audio_file)
    if not audio_path.exists():
        print(f"❌ Error: File not found: {audio_path}")
        sys.exit(1)
    
    print(f"\n{'='*60}")
    print(f"🎤 Audio Transcription")
    print(f"{'='*60}")
    print(f"File: {audio_path.name}")
    print(f"Model: {args.model}")
    print(f"Language: {args.language}")
    print(f"{'='*60}\n")
    
    try:
        from services import AudioService
        
        service = AudioService(model_name=args.model)
        
        language = None if args.language == "auto" else args.language
        result = service.transcribe(audio_path, language=language)
        
        print(f"\n{'='*60}")
        print(f"Language: {result.language} ({result.language_probability:.2%} confidence)")
        print(f"{'='*60}")
        print(result.text)
        print(f"{'='*60}\n")
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(result.text)
            print(f"💾 Saved to: {output_path}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
