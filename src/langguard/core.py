"""Core functionality for LangGuard."""

from typing import Optional, Dict, Union
from .agent import GuardAgent, GuardResponse


def hello(name: str = "World") -> str:
    """
    Return a hello message.
    
    Args:
        name: The name to greet (default: "World")
    
    Returns:
        A greeting message
    """
    return f"Hello, {name}! Welcome to LangGuard!"


class LangGuard:
    """Main LangGuard class for prompt security and validation."""
    
    def __init__(self, config: dict = None, llm_provider: str = None):
        """
        Initialize LangGuard instance.
        
        Args:
            config: Optional configuration dictionary
            llm_provider: LLM provider to use ('openai', 'ollama', or None for test mode)
        """
        self.config = config or {}
        self.agent = GuardAgent(llm=llm_provider)
        self.default_specification = config.get('default_specification') if config else None
    
    def guard(self, 
              prompt: str, 
              specification: Optional[str] = None,
              temperature: float = 0.1) -> GuardResponse:
        """
        Guard a prompt against a security specification.
        
        Args:
            prompt: The user prompt to validate
            specification: Security specification to check against 
                         (uses default_specification if not provided)
            temperature: LLM temperature for generation (default: 0.1)
            
        Returns:
            GuardResponse with 'prompt_pass' (bool) and 'reason' (str)
        """
        spec_to_use = specification or self.default_specification
        
        if not spec_to_use:
            return {
                "prompt_pass": False, 
                "reason": "No specification provided and no default specification configured"
            }
        
        return self.agent.judge(
            specification=spec_to_use,
            prompt=prompt,
            temperature=temperature
        )
    
    def validate(self, prompt: str, specification: Optional[str] = None) -> bool:
        """
        Simple boolean validation of a prompt.
        
        Args:
            prompt: The user prompt to validate
            specification: Security specification to check against
            
        Returns:
            True if prompt passes, False otherwise
        """
        result = self.guard(prompt, specification)
        return result["prompt_pass"]
    
    def greet(self, name: str = "World") -> str:
        """
        Generate a greeting message.
        
        Args:
            name: The name to greet
            
        Returns:
            A greeting message
        """
        return hello(name)