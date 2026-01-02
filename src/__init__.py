"""
AI Content Processor

A comprehensive AI-powered application for processing audio and visual content.
"""

__version__ = "1.0.0"
__author__ = "Muhammad Omar Muneer <momarm45@gmail.com>"

from services.audio_service import AudioService
from services.image_service import ImageService
from services.document_service import DocumentService

__all__ = [
    "AudioService",
    "ImageService",
    "DocumentService",
]
