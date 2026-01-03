"""
Nutritionist Service for food item analysis.

This service provides nutrition analysis capabilities for food items.
"""

import logging
from pathlib import Path
from core.llm_client import LLMClient
from core.prompt_templates import NutritionistPromptTemplate

logger = logging.getLogger(__name__)

class NutritionServiceError(Exception):
    """Custom exception for nutrition service errors."""
    pass

class NutritionService:
    """Service for nutrition analysis of food items."""
    
    def __init__(self, llm_client=None):
        """Initialize the nutrition service."""
        self.logger = logger
        self.llm_client = llm_client or LLMClient()
        
        self.logger.info("Nutrition service initialized with LLM client")
        from .image_service import ImageService
        self.image_service = ImageService()

    def analyze_food_items(self, image_path: str, prompt: str = None) -> dict:
        """
        Analyze food items in an image and provide nutritional information.
        
        Args:
            image_path: Path to the image file
            prompt: Optional custom prompt for analysis
            
        Returns:
            Dictionary containing nutritional analysis results
        """
        
            
        image_path = Path(image_path)
        if not image_path.exists():
            raise NutritionServiceError(f"Image file not found: {image_path}")
        info = self.image_service.get_image_info(image_path)
        logger.debug(f"Image info: {info['format']} {info['width']}x{info['height']}")       
        try:
           
           
            self.logger.info(f"Analyzing food items in image: {image_path}")
            encoded_image = self.image_service.encode_image(image_path)
            media_type = f"image/{info['format'].lower()}";
            if media_type == "image/jpeg":
                media_type = "image/jpeg"
            elif media_type not in ["image/png", "image/jpeg", "image/gif", "image/webp"]:
                media_type = "image/png"  # Default fallback

            if prompt is None:
                prompt = "Analyze the food items in this image and provide nutritional information including calories, macronutrients, and dietary value."
            
            messages = NutritionistPromptTemplate.create_nutrition_summary_prompt(
                prompt,
                encoded_image,
                media_type
            )
            response = self.llm_client.invoke(messages)
            # Process the response here
            if hasattr(response, 'content'):
                result = response.content
            elif hasattr(response, 'output'):
                result = response.output
            else:
                result = str(response)
            logger.info(f"✅ Analysis complete: {len(result)} characters")
            return result
        
        except Exception as e:
            self.logger.error(f"Error analyzing food items: {e}")
            raise


if __name__ == "__main__":
    # Example usage
    try:
        service = NutritionService()
        result = service.analyze_food_items("test_image.jpg")
        print(result)
    except ValueError as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    except NutritionServiceError as e:
        print(f"Nutrition service error: {e}")
        traceback.print_exc()
    except Exception as e:
        print(f"Unexpected error: {e}")
        traceback.print_exc()