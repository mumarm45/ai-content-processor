"""
Image Service for image analysis and text extraction using Claude Vision.

This service provides image analysis capabilities with proper error
handling and configuration management.
"""

import base64
import os
from pathlib import Path
from typing import Optional
import logging
from PIL import Image

from core.llm_client import LLMClient
from core.prompt_templates import ImagePromptTemplate

logger = logging.getLogger(__name__)


class ImageServiceError(Exception):
    """Base exception for image service errors."""
    pass


class ImageService:
    """
    Service for image analysis using Claude Vision.
    
    Example:
        >>> service = ImageService()
        >>> result = service.analyze("diagram.png", prompt="What does this show?")
        >>> print(result)
    """
    
    SUPPORTED_FORMATS = {'.png', '.jpg', '.jpeg', '.gif', '.webp'}
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize the image service.
        
        Args:
            llm_client: Optional LLM client instance
        """
        self.llm_client = llm_client or LLMClient()
        logger.info("Initialized ImageService")
    
    @staticmethod
    def encode_image(image_path: str | Path) -> str:
        """
        Convert image to base64 for model input.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Base64 encoded image string
            
        Raises:
            ImageServiceError: If image cannot be read
        """
        try:
            with open(image_path, "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read()).decode('utf-8')
            return encoded_string
        except Exception as e:
            raise ImageServiceError(f"Failed to encode image: {e}") from e
    
    @staticmethod
    def get_image_info(image_path: str | Path) -> dict:
        """
        Get basic information about an image.
        
        Args:
            image_path: Path to the image
            
        Returns:
            Dictionary with image info (format, size, mode)
        """
        try:
            with Image.open(image_path) as img:
                return {
                    "format": img.format,
                    "size": img.size,
                    "mode": img.mode,
                    "width": img.width,
                    "height": img.height
                }
        except Exception as e:
            raise ImageServiceError(f"Failed to read image info: {e}") from e
    
    def analyze(
        self,
        image_path: str | Path,
        prompt: Optional[str] = None
    ) -> str:
        """
        Analyze an image and extract information.
        
        Args:
            image_path: Path to the image file
            prompt: Optional text prompt to guide the analysis
            
        Returns:
            Analysis result from Claude
            
        Raises:
            ImageServiceError: If analysis fails
        """
        image_path = Path(image_path)
        
        if not image_path.exists():
            raise ImageServiceError(f"Image file not found: {image_path}")
        
        if image_path.suffix.lower() not in self.SUPPORTED_FORMATS:
            raise ImageServiceError(
                f"Unsupported image format: {image_path.suffix}. "
                f"Supported: {', '.join(self.SUPPORTED_FORMATS)}"
            )
        
        logger.info(f"📸 Analyzing image: {image_path.name}")
        
        try:
            
            info = self.get_image_info(image_path)
            logger.debug(f"Image info: {info['format']} {info['width']}x{info['height']}")
            
            encoded_image = self.encode_image(image_path)
            
            if not prompt:
                prompt = "Describe what you see in this image. Extract any text present."
            
            media_type = f"image/{info['format'].lower()}"
            if media_type == "image/jpeg":
                media_type = "image/jpeg"
            elif media_type not in ["image/png", "image/jpeg", "image/gif", "image/webp"]:
                media_type = "image/png"  # Default fallback
            
            messages = ImagePromptTemplate.create_image_analysis_messages(
                encoded_image,
                prompt,
                media_type=media_type
            )
            
            logger.info("🤖 Analyzing with Claude Vision...")
            
            response = self.llm_client.invoke(messages)
            
            if hasattr(response, 'content'):
                result = response.content
            else:
                result = str(response)
            
            logger.info(f"✅ Analysis complete: {len(result)} characters")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Image analysis failed: {e}", exc_info=True)
            raise ImageServiceError(f"Image analysis failed: {e}") from e
    
    def extract_text(self, image_path: str | Path) -> str:
        """
        Extract text from an image (OCR).
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Extracted text
        """
        prompt = ImagePromptTemplate.create_text_extraction_prompt()
        return self.analyze(image_path, prompt=prompt)




if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    if len(sys.argv) > 1:
        image_file = sys.argv[1]
        prompt_text = sys.argv[2] if len(sys.argv) > 2 else None
        
        try:
            service = ImageService()
            result = service.analyze(image_file, prompt=prompt_text)
            
            print(f"\n{'='*60}")
            print("Image Analysis Result:")
            print(f"{'='*60}")
            print(result)
            print(f"{'='*60}\n")
            
        except ImageServiceError as e:
            print(f"\n❌ Error: {e}")
            sys.exit(1)
    else:
        print("Usage: python image_service.py <image_file> [prompt]")
        print("\nExample:")
        print("  python image_service.py diagram.png")
        print('  python image_service.py document.jpg "Extract all text"')
