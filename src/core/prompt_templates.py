"""
Prompt Templates for various AI tasks.

This module contains reusable prompt templates for different document
processing tasks.
"""

from typing import Optional
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


class FinancialPromptTemplate:
    """Prompt templates for financial document processing."""
    
    @staticmethod
    def create_financial_formatting_prompt(transcript: str) -> PromptTemplate:
        """
        Create a prompt for formatting financial terminology in transcripts.
        
        This expands financial acronyms and standardizes terminology:
        - '401k' → '401(k) retirement savings plan'
        - 'HSA' → 'Health Savings Account (HSA)'
        - 'ROA' → 'Return on Assets (ROA)'
        
        Args:
            transcript: The raw transcript text
            
        Returns:
            PromptTemplate for financial formatting
        """
        template = """
        You are an intelligent assistant specializing in financial products.
        Your task is to process transcripts of earnings calls, ensuring that all 
        references to financial products and common financial terms are in the correct format.
        
        For each financial product or common term that is typically abbreviated as an acronym, 
        the full term should be spelled out followed by the acronym in parentheses.
        
        Examples:
        - '401k' → '401(k) retirement savings plan'
        - 'HSA' → 'Health Savings Account (HSA)'
        - 'ROA' → 'Return on Assets (ROA)'
        - 'VaR' → 'Value at Risk (VaR)'
        - 'PB' → 'Price to Book (PB) ratio'
        - 'five two nine' → '529 (Education Savings Plan)'
        - 'four zero one k' → '401(k) (Retirement Savings Plan)'
        
        Note: Some acronyms have different meanings based on context (e.g., 'LTV' can be 
        'Loan to Value' or 'Lifetime Value'). Discern from context which term is appropriate.
        
        Regular numbers like 'twenty three percent' should be left as is.
        
        After processing, provide:
        1. The adjusted transcript
        2. A list of the changes you made
        
        Transcript:
        {transcript}
        """
        
        return PromptTemplate(
            input_variables=["transcript"],
            template=template
        )


class MeetingPromptTemplate:
    """Prompt templates for meeting processing."""
    
    @staticmethod
    def create_meeting_minutes_prompt() -> ChatPromptTemplate:
        """
        Create a prompt for generating meeting minutes from transcripts.
        
        Returns:
            ChatPromptTemplate for meeting minutes
        """
        template = """
        Generate meeting minutes and a list of tasks based on the provided context.

        Context:
        {transcript}

        Please provide:
        
        ## Meeting Minutes
        - Key points discussed
        - Decisions made
        - Important topics covered

        ## Task List
        - Actionable items with assignees (if mentioned) and deadlines (if mentioned)
        - Follow-up actions needed
        """
        
        return ChatPromptTemplate.from_template(template)


class ImagePromptTemplate:
    """Prompt templates for image analysis."""
    
    @staticmethod
    def create_image_analysis_messages(
        encoded_image: str,
        prompt: Optional[str] = None,
        media_type: str = "image/png"
    ) -> list:
        """
        Create messages for image analysis with Claude Vision.
        
        Args:
            encoded_image: Base64 encoded image data
            prompt: Text prompt for the image (optional)
            media_type: MIME type of the image
            
        Returns:
            List of messages for Claude API
        """
        if not prompt:
            prompt = "Describe what you see in this image in detail. Extract any text present."
        
        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": prompt
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": encoded_image
                    }
                }
            ]
        }]
        
        return messages
    
    @staticmethod
    def create_text_extraction_prompt() -> str:
        """
        Create a prompt specifically for text extraction from images.
        
        Returns:
            Text extraction prompt
        """
        return (
            "Please extract all text from this image. "
            "Preserve the structure and formatting as much as possible. "
            "If there are any diagrams or visual elements, describe them briefly."
        )


class NutritionistPromptTemplate:
    """Prompt templates for nutritionist-related tasks."""
    
    @staticmethod
    def create_nutrition_analysis_prompt_assisstent() -> str:
        """
        Create a prompt for nutrition analysis.
        
        Returns:
            Nutrition analysis prompt
        """
        return """
                You are an expert nutritionist. Your task is to analyze the food items displayed in the image and provide a detailed nutritional assessment using the following format:
            1. **Identification**: List each identified food item clearly, one per line.
            2. **Portion Size & Calorie Estimation**: For each identified food item, specify the portion size and provide an estimated number of calories. Use bullet points with the following structure:
            - **[Food Item]**: [Portion Size], [Number of Calories] calories
            Example:
            *   **Salmon**: 6 ounces, 210 calories
            *   **Asparagus**: 3 spears, 25 calories
            3. **Total Calories**: Provide the total number of calories for all food items.
            Example:
            Total Calories: [Number of Calories]
            4. **Nutrient Breakdown**: Include a breakdown of key nutrients such as **Protein**, **Carbohydrates**, **Fats**, **Vitamins**, and **Minerals**. Use bullet points, and for each nutrient provide details about the contribution of each food item.
            Example:
            *   **Protein**: Salmon (35g), Asparagus (3g), Tomatoes (1g) = [Total Protein]
            5. **Health Evaluation**: Evaluate the healthiness of the meal in one paragraph.
            6. **Disclaimer**: Include the following exact text as a disclaimer:
            The nutritional information and calorie estimates provided are approximate and are based on general food data. 
            Actual values may vary depending on factors such as portion size, specific ingredients, preparation methods, and individual variations. 
            For precise dietary advice or medical guidance, consult a qualified nutritionist or healthcare provider.
            Format your response exactly like the template above to ensure consistency.
            """

    
    @staticmethod
    def create_nutrition_summary_prompt(prompt: str, encoded_image: str, media_type: str) -> list:
        """Create a prompt for summarizing nutritional information."""
        nutrition_prompt = NutritionistPromptTemplate.create_nutrition_analysis_prompt_assisstent()
        messages = [{
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text":  nutrition_prompt + " " + prompt
                },
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": media_type,
                        "data": encoded_image
                    }
                }
            ]
        }]

        return messages

if __name__ == "__main__":
    # Example usage
    print("Financial Prompt Template:")
    print("-" * 60)
    financial_prompt = FinancialPromptTemplate.create_financial_formatting_prompt(
        "Our ROA improved and the 401k business grew."
    )
    print(financial_prompt.template[:200] + "...")
    
    print("\n\nNutrition Prompt Template:")
    print("-" * 60)
    nutrition_prompt = NutritionistPromptTemplate.create_nutrition_analysis_prompt_assisstent()
    print(nutrition_prompt[:200] + "...")
    
    print("\n\nMeeting Minutes Prompt Template:")
    print("-" * 60)
    meeting_prompt = MeetingPromptTemplate.create_meeting_minutes_prompt()
    print(meeting_prompt.messages[0].prompt.template[:200] + "...")
