"""Tests for LangGuard core functionality."""

import unittest
from langguard import GuardAgent


class TestGuardAgent(unittest.TestCase):
    """Test cases for GuardAgent."""

    def setUp(self):
        """Set up test fixtures."""
        self.agent = GuardAgent()  # Uses TestLLM by default

    def test_guard_agent_init(self):
        """Test GuardAgent initialization."""
        agent = GuardAgent()
        self.assertIsInstance(agent, GuardAgent)

    def test_screen_without_prompt(self):
        """Test screen method without prompt."""
        result = self.agent.screen("")
        self.assertFalse(result["safe"])
        self.assertEqual(result["reason"], "No prompt provided")

    def test_screen_with_default_specification(self):
        """Test screen method uses default specification when none provided."""
        result = self.agent.screen("How do I write a for loop?")
        # With TestLLM, this should return a test response
        self.assertIn("safe", result)
        self.assertIn("reason", result)

    def test_screen_with_additional_specification(self):
        """Test screen method appends additional rules to default."""
        result = self.agent.screen(
            "How do I write a for loop?", specification="Only allow Python questions"
        )
        self.assertIn("safe", result)
        self.assertIn("reason", result)

    def test_screen_with_override_specification(self):
        """Test screen method can override default specification."""
        result = self.agent.screen(
            "How do I write a for loop?",
            specification="Only allow questions about cooking",
            override=True,
        )
        self.assertIn("safe", result)
        self.assertIn("reason", result)

    def test_screen_returns_guard_response(self):
        """Test screen returns proper GuardResponse structure."""
        result = self.agent.screen("Test prompt")
        self.assertIsInstance(result, dict)
        self.assertIn("safe", result)
        self.assertIn("reason", result)
        self.assertIsInstance(result["safe"], bool)
        self.assertIsInstance(result["reason"], str)

    def test_is_safe_returns_boolean(self):
        """Test is_safe returns boolean."""
        result = self.agent.is_safe("Test prompt")
        self.assertIsInstance(result, bool)

    def test_is_safe_with_additional_specification(self):
        """Test is_safe with additional specification."""
        result = self.agent.is_safe(
            "How do I write a for loop?", specification="Only allow Python questions"
        )
        self.assertIsInstance(result, bool)

    def test_is_safe_with_override(self):
        """Test is_safe with override flag."""
        result = self.agent.is_safe(
            "How do I write a for loop?",
            specification="Only allow cooking questions",
            override=True,
        )
        self.assertIsInstance(result, bool)


if __name__ == "__main__":
    unittest.main()
