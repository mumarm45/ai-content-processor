"""
Document Service for processing transcripts and generating structured output.

This service handles meeting minutes generation, financial document processing,
and other document-related tasks.
"""

import logging
from typing import Optional
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough

from core.llm_client import LLMClient
from core.prompt_templates import (
    MeetingPromptTemplate,
    FinancialPromptTemplate
)

logger = logging.getLogger(__name__)


class DocumentServiceError(Exception):
    """Base exception for document service errors."""
    pass


class DocumentService:
    """
    Service for document processing and generation.
    
    Example:
        >>> service = DocumentService()
        >>> minutes = service.generate_meeting_minutes(transcript)
        >>> print(minutes)
    """
    
    def __init__(self, llm_client: Optional[LLMClient] = None):
        """
        Initialize the document service.
        
        Args:
            llm_client: Optional LLM client instance
        """
        self.llm_client = llm_client or LLMClient(temperature=0.5)
        logger.info("Initialized DocumentService")
    
    def generate_meeting_minutes(self, transcript: str) -> str:
        """
        Generate meeting minutes and task list from a transcript.
        
        Args:
            transcript: Meeting transcript text
            
        Returns:
            Formatted meeting minutes with tasks
            
        Raises:
            DocumentServiceError: If generation fails
        """
        if not transcript or not transcript.strip():
            raise DocumentServiceError("Transcript cannot be empty")
        
        logger.info("🤖 Generating meeting minutes and tasks...")
        
        try:
            prompt = MeetingPromptTemplate.create_meeting_minutes_prompt()
            
            chain = (
                {"transcript": RunnablePassthrough()}
                | prompt
                | self.llm_client.client
                | StrOutputParser()
            )
            
            result = chain.invoke(transcript)
            
            logger.info(f"✅ Generated {len(result)} characters of meeting notes")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Meeting minutes generation failed: {e}", exc_info=True)
            raise DocumentServiceError(f"Generation failed: {e}") from e
    
    def format_financial_transcript(self, transcript: str) -> str:
        """
        Format financial terminology in a transcript.
        
        Expands acronyms like:
        - '401k' → '401(k) retirement savings plan'
        - 'ROA' → 'Return on Assets (ROA)'
        
        Args:
            transcript: Raw financial transcript
            
        Returns:
            Formatted transcript with expanded terms
            
        Raises:
            DocumentServiceError: If formatting fails
        """
        if not transcript or not transcript.strip():
            raise DocumentServiceError("Transcript cannot be empty")
        
        logger.info("🤖 Formatting financial transcript...")
        
        try:
            prompt = FinancialPromptTemplate.create_financial_formatting_prompt(
                transcript
            )
            
            formatted_prompt = prompt.format(transcript=transcript)
            response = self.llm_client.invoke(formatted_prompt)
            
            if hasattr(response, 'content'):
                result = response.content
            else:
                result = str(response)
            
            logger.info(f"✅ Formatted {len(result)} characters")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Financial formatting failed: {e}", exc_info=True)
            raise DocumentServiceError(f"Formatting failed: {e}") from e
    
    def summarize(self, text: str, max_length: Optional[int] = None) -> str:
        """
        Summarize a long text document.
        
        Args:
            text: Text to summarize
            max_length: Optional maximum length for summary
            
        Returns:
            Summary of the text
        """
        logger.info("🤖 Summarizing text...")
        
        length_instruction = ""
        if max_length:
            length_instruction = f" Keep the summary under {max_length} words."
        
        prompt = f"""
        Please provide a concise summary of the following text.{length_instruction}
        
        Text:
        {text}
        
        Summary:
        """
        
        try:
            response = self.llm_client.invoke(prompt)
            
            if hasattr(response, 'content'):
                result = response.content
            else:
                result = str(response)
            
            logger.info(f"✅ Created summary: {len(result)} characters")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Summarization failed: {e}", exc_info=True)
            raise DocumentServiceError(f"Summarization failed: {e}") from e


if __name__ == "__main__":
    import sys
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    sample_transcript = """
    Team meeting on January 2nd, 2026.
    
    Sarah presented the Q1 marketing plan. The team agreed to increase 
    the budget by $50,000. John will finalize the technical specifications 
    by January 10th.
    
    Maria raised concerns about the supply chain. She will research 
    alternative vendors and report back by January 8th.
    
    Launch date confirmed for February 1st, 2026.
    """
    
    print("=" * 60)
    print("Document Service Demo")
    print("=" * 60)
    
    try:
        service = DocumentService()
        
        print("\n📝 Generating meeting minutes...")
        result = service.generate_meeting_minutes(sample_transcript)
        
        print("\n✨ Result:")
        print("-" * 60)
        print(result)
        print("-" * 60)
        
    except DocumentServiceError as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
