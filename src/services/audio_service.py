"""
Audio Service for transcription using Whisper AI.

This service provides audio transcription capabilities with proper error
handling and configuration management.
"""

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass
import logging

# Fix OpenMP conflict before importing torch-based libraries
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from config import settings

logger = logging.getLogger(__name__)


@dataclass
class TranscriptionResult:
    """Complete transcription result with metadata."""
    text: str
    language: str
    language_probability: float
    
    def __str__(self) -> str:
        return self.text


class AudioServiceError(Exception):
    """Base exception for audio service errors."""
    pass


class AudioService:
    """
    Service for audio transcription using Whisper AI.
    
    Example:
        >>> service = AudioService()
        >>> result = service.transcribe("meeting.wav")
        >>> print(result.text)
    """
    
    def __init__(
        self, 
        model_name: Optional[str] = None,
        device: Optional[str] = None,
        compute_type: str = "int8"
    ):
        """
        Initialize the audio service.
        
        Args:
            model_name: Whisper model to use (tiny.en, base.en, etc.)
            device: Device to run on (cpu, cuda, mps)
            compute_type: Computation type (int8, float16, float32)
        """
        self.model_name = model_name or settings.WHISPER_MODEL
        self.device = device or settings.WHISPER_DEVICE
        self.compute_type = compute_type
        self._model = None  # Lazy loading
        
        logger.info(
            f"Initialized AudioService with model={self.model_name}, "
            f"device={self.device}"
        )
    
    @property
    def model(self):
        """Lazy load the Whisper model."""
        if self._model is None:
            logger.info(f"Loading Whisper model: {self.model_name}")
            from faster_whisper import WhisperModel
            
            self._model = WhisperModel(
                self.model_name, 
                device=self.device, 
                compute_type=self.compute_type
            )
            logger.info("Model loaded successfully")
        
        return self._model
    
    def transcribe(
        self, 
        audio_path: str | Path, 
        language: Optional[str] = "en",
        beam_size: int = 5
    ) -> TranscriptionResult:
        """
        Transcribe an audio file to text.
        
        Args:
            audio_path: Path to the audio file
            language: Language code (en, es, fr, etc.) or None for auto-detect
            beam_size: Beam size for decoding (1-10, higher = more accurate)
            
        Returns:
            TranscriptionResult with text and metadata
            
        Raises:
            AudioServiceError: If transcription fails
        """
        audio_path = Path(audio_path)
        
        # Validate file exists
        if not audio_path.exists():
            raise AudioServiceError(f"Audio file not found: {audio_path}")
        
        logger.info(f"🎤 Transcribing: {audio_path.name}")
        
        try:
            # Perform transcription
            segments_iter, info = self.model.transcribe(
                str(audio_path),
                beam_size=beam_size,
                language=language
            )
            
            # Log detection info
            logger.info(
                f"📝 Detected language: {info.language} "
                f"(probability: {info.language_probability:.2%})"
            )
            
            # Process segments
            full_text = []
            
            for segment in segments_iter:
                logger.debug(
                    f"[{segment.start:.2f}s → {segment.end:.2f}s] {segment.text}"
                )
                full_text.append(segment.text.strip())
            
            result = TranscriptionResult(
                text=" ".join(full_text),
                language=info.language,
                language_probability=info.language_probability
            )
            
            logger.info(f"✅ Transcription complete: {len(result.text)} characters")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Transcription failed: {e}", exc_info=True)
            raise AudioServiceError(f"Transcription failed: {e}") from e


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) > 1:
        audio_file = sys.argv[1]
        
        try:
            service = AudioService()
            result = service.transcribe(audio_file)
            
            print(f"\n{'='*60}")
            print(f"Language: {result.language} ({result.language_probability:.2%})")
            print(f"{'='*60}")
            print(result.text)
            print(f"{'='*60}\n")
            
        except AudioServiceError as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python audio_service.py <audio_file>")
