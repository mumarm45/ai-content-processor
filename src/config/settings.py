"""
Configuration settings for AI Content Processor.

This module manages all configuration from environment variables.
"""

import os
from pathlib import Path
from typing import Literal
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings loaded from environment variables."""
    
    # API Configuration
    ANTHROPIC_API_KEY: str = os.getenv("ANTHROPIC_API_KEY", "")
    ANTHROPIC_MODEL: str = os.getenv("ANTHROPIC_MODEL_ID", "claude-3-5-sonnet-20241022")
    
    # LLM Parameters
    TEMPERATURE: float = float(os.getenv("TEMPERATURE", "0.7"))
    MAX_TOKENS: int = int(os.getenv("MAX_TOKENS", "1024"))
    
    # Audio Settings
    WHISPER_MODEL: str = os.getenv("WHISPER_MODEL", "tiny.en")
    WHISPER_DEVICE: str = os.getenv("WHISPER_DEVICE", "cpu")
    WHISPER_COMPUTE_TYPE: str = os.getenv("WHISPER_COMPUTE_TYPE", "int8")
    
    # Server Settings
    SERVER_HOST: str = os.getenv("SERVER_HOST", "0.0.0.0")
    SERVER_PORT: int = int(os.getenv("SERVER_PORT", "5500"))
    
    # Paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent.parent
    DATA_DIR: Path = PROJECT_ROOT / "data"
    AUDIO_DIR: Path = DATA_DIR / "audio"
    IMAGES_DIR: Path = DATA_DIR / "images"
    OUTPUT_DIR: Path = DATA_DIR / "output"
    
    # Logging
    LOG_LEVEL: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = os.getenv("LOG_LEVEL", "INFO")
    
    @classmethod
    def validate(cls) -> bool:
        """
        Validate that required settings are present.
        
        Returns:
            True if valid, raises ValueError otherwise
        """
        if not cls.ANTHROPIC_API_KEY:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. "
                "Please set it in your .env file or environment variables."
            )
        return True
    
    @classmethod
    def create_directories(cls) -> None:
        """Create necessary data directories if they don't exist."""
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.AUDIO_DIR.mkdir(exist_ok=True)
        cls.IMAGES_DIR.mkdir(exist_ok=True)
        cls.OUTPUT_DIR.mkdir(exist_ok=True)


# Create singleton instance
settings = Settings()

# Validate on import
try:
    settings.validate()
except ValueError as e:
    import warnings
    warnings.warn(f"Configuration warning: {e}")
