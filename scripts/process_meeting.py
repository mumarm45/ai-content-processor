"""
CLI tool for processing meeting recordings.

This combines audio transcription with meeting minutes generation.

Usage:
    python scripts/process_meeting.py meeting.wav
    python scripts/process_meeting.py meeting.mp3 --output minutes.txt
"""

import sys
import argparse
import logging
from pathlib import Path


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Process meeting recordings: transcribe and generate minutes"
    )
    
    parser.add_argument(
        "audio_file",
        help="Path to meeting recording (WAV, MP3, M4A, FLAC, etc.)"
    )
    
    parser.add_argument(
        "--model",
        default="tiny.en",
        help="Whisper model to use (default: tiny.en)"
    )
    
    parser.add_argument(
        "--output",
        "-o",
        help="Output file path for minutes (optional)"
    )
    
    parser.add_argument(
        "--save-transcript",
        help="Also save raw transcript to this file"
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
    print(f"📝 Meeting Processing")
    print(f"{'='*60}")
    print(f"File: {audio_path.name}")
    print(f"Model: {args.model}")
    print(f"{'='*60}\n")
    
    try:
        print("🎤 Step 1: Transcribing audio...")
        from services import AudioService
        
        audio_service = AudioService(model_name=args.model)
        transcription = audio_service.transcribe(audio_path)
        
        print(f"\n✅ Transcription complete ({len(transcription.text)} characters)")
        print(f"Language: {transcription.language} ({transcription.language_probability:.2%})\n")
        
        if args.save_transcript:
            transcript_path = Path(args.save_transcript)
            transcript_path.write_text(transcription.text)
            print(f"💾 Transcript saved to: {transcript_path}\n")
        
        print("📝 Step 2: Generating meeting minutes...\n")
        from services import DocumentService
        
        doc_service = DocumentService()
        minutes = doc_service.generate_meeting_minutes(transcription.text)
        
        print(f"\n{'='*60}")
        print("Meeting Minutes:")
        print(f"{'='*60}")
        print(minutes)
        print(f"{'='*60}\n")
        
        if args.output:
            output_path = Path(args.output)
            output_path.write_text(minutes)
            print(f"💾 Minutes saved to: {output_path}\n")
        
        return 0
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        if args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
