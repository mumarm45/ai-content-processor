"""
LLM Client for interacting with Claude AI.

This module provides a client for the Anthropic Claude API with proper
configuration management and error handling.
"""

import logging
from typing import Optional
from langchain_anthropic import ChatAnthropic
from config import settings

logger = logging.getLogger(__name__)


class LLMClient:
    """
    Client for interacting with Claude LLM.
    
    This class provides a managed interface to the Claude API with
    proper configuration and error handling.
    
    Example:
        >>> client = LLMClient()
        >>> response = client.invoke("Tell me a story")
        >>> print(response.content)
    """
    
    def __init__(
        self,
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        api_key: Optional[str] = None
    ):
        """
        Initialize the LLM client.
        
        Args:
            model: Claude model to use (defaults to settings)
            temperature: Temperature for generation (0-1)
            max_tokens: Maximum tokens in response
            api_key: Anthropic API key (defaults to settings)
        """
        self.model = model or settings.ANTHROPIC_MODEL
        self.temperature = temperature if temperature is not None else settings.TEMPERATURE
        self.max_tokens = max_tokens or settings.MAX_TOKENS
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "ANTHROPIC_API_KEY is required. "
                "Set it in your .env file or pass it to LLMClient()"
            )
        
        self._client = None
        logger.info(f"Initialized LLMClient with model={self.model}")
    
    @property
    def client(self) -> ChatAnthropic:
        """
        Get the LangChain ChatAnthropic client (lazy loaded).
        
        Returns:
            ChatAnthropic instance
        """
        if self._client is None:
            self._client = ChatAnthropic(
                api_key=self.api_key,
                model=self.model,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            logger.debug(f"Created ChatAnthropic client: {self.model}")
        
        return self._client
    
    def invoke(self, prompt: str | list) -> any:
        """
        Invoke the LLM with a prompt.
        
        Args:
            prompt: Text prompt or list of messages
            
        Returns:
            Response from Claude
            
        Example:
            >>> client = LLMClient()
            >>> response = client.invoke("What is AI?")
            >>> print(response.content)
        """
        logger.debug(f"Invoking LLM with prompt length: {len(str(prompt))}")
        
        try:
            response = self.client.invoke(prompt)
            logger.debug(f"LLM response received")
            return response
        except Exception as e:
            logger.error(f"LLM invocation failed: {e}", exc_info=True)
            raise
    
    def set_temperature(self, temperature: float) -> None:
        """Update the temperature and reset the client."""
        self.temperature = temperature
        self._client = None
        logger.info(f"Temperature updated to {temperature}")
    
    def set_max_tokens(self, max_tokens: int) -> None:
        """Update max_tokens and reset the client."""
        self.max_tokens = max_tokens
        self._client = None
        logger.info(f"Max tokens updated to {max_tokens}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    try:
        client = LLMClient()
        response = client.invoke("Say hello in 5 words or less")
        print(f"\nResponse: {response.content}")
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set ANTHROPIC_API_KEY in your .env file")
