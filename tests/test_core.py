"""Tests for LangGuard core functionality."""

import unittest
from langguard import GuardAgent


class TestGuardAgent(unittest.TestCase):
    """Test cases for GuardAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = GuardAgent()  # Uses TestLLM by default
        self.agent_with_config = GuardAgent(
            config={"default_specification": "Only allow technical questions"}
        )

    def test_guard_agent_init(self):
        """Test GuardAgent initialization."""
        agent = GuardAgent()
        self.assertIsInstance(agent, GuardAgent)
        self.assertIsNone(agent.default_specification)

    def test_guard_agent_with_config(self):
        """Test GuardAgent with configuration."""
        config = {"default_specification": "Only allow safe content"}
        agent = GuardAgent(config=config)
        self.assertEqual(agent.config, config)
        self.assertEqual(agent.default_specification, "Only allow safe content")

    def test_screen_without_prompt(self):
        """Test screen method without prompt."""
        result = self.agent.screen("", "Some specification")
        self.assertFalse(result["prompt_pass"])
        self.assertEqual(result["reason"], "No prompt provided")

    def test_screen_without_specification(self):
        """Test screen method without specification."""
        result = self.agent.screen("Test prompt")
        self.assertFalse(result["prompt_pass"])
        self.assertIn("No specification provided", result["reason"])

    def test_screen_with_default_specification(self):
        """Test screen method uses default specification."""
        result = self.agent_with_config.screen("How do I write a for loop?")
        # With TestLLM, this should return a test response
        self.assertIn("prompt_pass", result)
        self.assertIn("reason", result)

    def test_screen_returns_guard_response(self):
        """Test screen returns proper GuardResponse structure."""
        result = self.agent.screen("Test prompt", "Test specification")
        self.assertIsInstance(result, dict)
        self.assertIn("prompt_pass", result)
        self.assertIn("reason", result)
        self.assertIsInstance(result["prompt_pass"], bool)
        self.assertIsInstance(result["reason"], str)

    def test_is_safe_returns_boolean(self):
        """Test is_safe returns boolean."""
        result = self.agent.is_safe("Test prompt", "Test specification")
        self.assertIsInstance(result, bool)

    def test_is_safe_without_specification(self):
        """Test is_safe without specification."""
        result = self.agent.is_safe("Test prompt")
        self.assertFalse(result)

    def test_is_safe_with_default_specification(self):
        """Test is_safe uses default specification."""
        result = self.agent_with_config.is_safe("How do I write a for loop?")
        self.assertIsInstance(result, bool)


if __name__ == "__main__":
    unittest.main()
