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


if __name__ == "__main__":
    # Example usage
    print("Financial Prompt Template:")
    print("-" * 60)
    financial_prompt = FinancialPromptTemplate.create_financial_formatting_prompt(
        "Our ROA improved and the 401k business grew."
    )
    print(financial_prompt.template[:200] + "...")
    
    print("\n\nMeeting Minutes Prompt Template:")
    print("-" * 60)
    meeting_prompt = MeetingPromptTemplate.create_meeting_minutes_prompt()
    print(meeting_prompt.messages[0].prompt.template[:200] + "...")
