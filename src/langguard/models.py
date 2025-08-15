import os
import requests
from typing import Optional, Dict, Any


def set_llm(llm_provider: str = None):
    if not llm_provider:
        llm_provider = os.getenv("GUARD_LLM_PROVIDER", None)
    if llm_provider == "openai":
        return OpenAILLM()
    else:
        return TestLLM()


class OpenAILLM:
    """OpenAI LLM provider with native structured output support."""

    def __init__(
        self,
        model: str = "gpt-4o-mini",
        api_key: Optional[str] = None,
        temperature: float = 0,
    ):
        self.model = os.getenv("GUARD_LLM_MODEL", model)
        self.api_key = os.getenv("GUARD_LLM_API_KEY", api_key)
        if not self.api_key:
            raise ValueError(
                "OpenAI API key required. Set GUARD_LLM_API_KEY environment variable."
            )
        self.temperature = float(os.getenv("LLM_TEMPERATURE", temperature))
        self.endpoint_url = "https://api.openai.com/v1/chat/completions"

    def generate(
        self,
        prompt: str,
        temperature: Optional[float] = None,
        json_schema: Optional[Dict[str, Any]] = None,
    ) -> str:
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}",
        }

        messages = [
            {"role": "system", "content": "You are a security guard for AI systems."},
            {"role": "user", "content": prompt},
        ]

        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature or self.temperature,
        }

        # Use OpenAI's structured output feature
        if json_schema:
            payload["response_format"] = {
                "type": "json_schema",
                "json_schema": {
                    "name": "guard_response",
                    "strict": True,
                    "schema": json_schema,
                },
            }

        response = requests.post(self.endpoint_url, headers=headers, json=payload)
        response.raise_for_status()

        result = response.json()
        return result["choices"][0]["message"]["content"]


class TestLLM:
    """Test LLM provider that echoes prompts in generated responses for testing purposes."""

    def __init__(
        self,
        model: str = "test-model",
        endpoint_url: str = None,
        api_key: str = None,
        temperature: float = 0,
    ):
        self.model = model
        self.endpoint_url = endpoint_url
        self.api_key = api_key
        self.temperature = temperature

    def generate(
        self,
        prompt: str,
        temperature: float = None,
        json_schema: Optional[Dict[str, Any]] = None,
    ) -> str:
        """Generate a test response that echoes the input prompt."""

        # If json_schema is provided, return a test JSON response
        if json_schema:
            # For testing, always return a safe/failed response
            return '{"safe": false, "reason": "Test mode - always fails for safety"}'

        # Create a response that includes the original prompt
        response = f"[TEST RESPONSE] Echo of prompt: '{prompt}'"

        # If temperature is specified, include that info
        temp_used = temperature if temperature is not None else self.temperature
        if temp_used > 0:
            response += f" | Temperature: {temp_used}"

        return response
