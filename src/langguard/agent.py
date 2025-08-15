from langguard.models import set_llm
import backoff
import json
from typing import TypedDict, Optional


class GuardResponse(TypedDict):
    prompt_pass: bool
    reason: str


class GuardAgent:
    """Guard Agent that screens prompts entering AI agent pipelines."""

    def __init__(self, llm=None, config: dict = None):
        self.llm = set_llm(llm)
        self.config = config or {}
        self.default_specification = (
            config.get("default_specification") if config else None
        )

    def _llm_generate_with_retry(
        self,
        prompt: str,
        timeout: float = 30,
        temperature: Optional[float] = None,
        json_schema: Optional[dict] = None,
    ) -> str:

        def _call():
            try:
                return self.llm.generate(
                    prompt, temperature=temperature, json_schema=json_schema
                )
            except Exception as e:
                raise RuntimeError(f"LLM generation failed: {e}")

        @backoff.on_exception(
            backoff.expo,
            RuntimeError,
            max_tries=3,
            max_time=timeout,
            jitter=backoff.full_jitter,
        )
        def _retry_call():
            return _call()

        return _retry_call()

    def screen(
        self, prompt: str, specification: str = None, temperature: float = None
    ) -> GuardResponse:
        """Screen a prompt against a security specification.

        Args:
            prompt: The user prompt to validate
            specification: Security specification to check against
                         (uses default_specification if not provided)
            temperature: LLM temperature for generation (default: 0.1)

        Returns:
            GuardResponse with 'prompt_pass' (bool) and 'reason' (str)
        """
        if not prompt:
            return {"prompt_pass": False, "reason": "No prompt provided"}

        spec_to_use = specification or self.default_specification
        if not spec_to_use:
            return {
                "prompt_pass": False,
                "reason": "No specification provided and no default specification configured",
            }

        # Define the output schema for structured JSON
        output_schema = {
            "type": "object",
            "properties": {
                "prompt_pass": {"type": "boolean"},
                "reason": {"type": "string"},
            },
            "required": ["prompt_pass", "reason"],
            "additionalProperties": False,
        }

        system_prompt = f"""You are a security guard for AI systems. Analyze the user prompt against the specification.

Specification: {spec_to_use}

User Prompt: {prompt}

Determine if the prompt is safe and complies with the specification."""

        try:
            response = self._llm_generate_with_retry(
                system_prompt, temperature=temperature, json_schema=output_schema
            )

            # Parse the JSON response
            parsed_response = json.loads(response.strip())

            # With structured outputs, we can trust the schema is correct
            # Just validate the types as a safety check
            if isinstance(parsed_response.get("prompt_pass"), bool) and isinstance(
                parsed_response.get("reason"), str
            ):
                return parsed_response
            else:
                return {
                    "prompt_pass": False,
                    "reason": "Invalid response types from LLM",
                }

        except json.JSONDecodeError:
            return {"prompt_pass": False, "reason": "LLM returned invalid JSON"}
        except Exception as e:
            return {
                "prompt_pass": False,
                "reason": f"Error processing LLM response: {str(e)}",
            }

    def is_safe(self, prompt: str, specification: str = None) -> bool:
        """
        Simple boolean validation of a prompt.

        Args:
            prompt: The user prompt to validate
            specification: Security specification to check against

        Returns:
            True if prompt passes, False otherwise
        """
        result = self.screen(prompt, specification)
        return result["prompt_pass"]
