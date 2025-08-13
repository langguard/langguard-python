"""Tests for LangGuard core functionality."""

import unittest
from langguard import hello, LangGuard


class TestLangGuard(unittest.TestCase):
    """Test cases for LangGuard library."""
    
    def test_hello_default(self):
        """Test hello function with default parameter."""
        result = hello()
        self.assertEqual(result, "Hello, World! Welcome to LangGuard!")
    
    def test_hello_custom_name(self):
        """Test hello function with custom name."""
        result = hello("Alice")
        self.assertEqual(result, "Hello, Alice! Welcome to LangGuard!")
    
    def test_langguard_class_init(self):
        """Test LangGuard class initialization."""
        lg = LangGuard()
        self.assertIsInstance(lg, LangGuard)
        self.assertEqual(lg.config, {})
    
    def test_langguard_class_with_config(self):
        """Test LangGuard class with configuration."""
        config = {"setting": "value"}
        lg = LangGuard(config)
        self.assertEqual(lg.config, config)
    
    def test_langguard_greet_method(self):
        """Test LangGuard greet method."""
        lg = LangGuard()
        result = lg.greet("Bob")
        self.assertEqual(result, "Hello, Bob! Welcome to LangGuard!")


if __name__ == '__main__':
    unittest.main()