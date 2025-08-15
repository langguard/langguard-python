# LangGuard 🛡️

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/langguard)](https://pypi.org/project/langguard/)

**LangGuard** is a Python library that acts as a security layer for LLM (Large Language Model) agent pipelines. It screens and validates language inputs before they reach your AI agents, helping prevent prompt injection, jailbreaking attempts, and ensuring compliance with your security specifications.

## 🚀 Features

- **🔍 Input Screening**: Validate prompts against custom security specifications
- **🤖 LLM-Based Analysis**: Uses language models to intelligently assess prompt safety
- **🔌 Provider Flexibility**: Support for OpenAI and custom LLM providers
- **📋 Structured Responses**: Returns typed responses with clear pass/fail status and reasoning
- **🔄 Retry Logic**: Built-in retry mechanism with exponential backoff for reliability
- **⚙️ Configurable**: Easy configuration through environment variables or code

## 📦 Installation

Install LangGuard using pip:

```bash
pip install langguard
```

## 🏃 Quick Start

### Basic Usage

```python
from langguard import GuardAgent

# Initialize GuardAgent
agent = GuardAgent(llm="openai")

# Define your security specification
specification = """
Only allow questions about programming and software development.
Reject personal information requests, harmful content, or non-technical topics.
"""

# Screen a user prompt
prompt = "How do I write a for loop in Python?"
response = agent.screen(prompt, specification)

if response["prompt_pass"]:
    print(f"✅ Prompt is safe: {response['reason']}")
    # Proceed with your LLM agent pipeline
else:
    print(f"❌ Prompt blocked: {response['reason']}")
    # Handle the blocked prompt
```

### Using Default Specification

```python
# Configure with a default specification
config = {
    "default_specification": "Only allow technical questions. Block personal or harmful content."
}

agent = GuardAgent(llm="openai", config=config)

# Now you can screen without specifying each time
response = agent.screen("What is recursion in programming?")
```

### Simple Boolean Validation

```python
# For simple pass/fail checks
is_safe = agent.is_safe(
    "Tell me about Python decorators",
    "Only allow programming questions"
)

if is_safe:
    # Process the prompt
    pass
```

## 🔧 Configuration

### Environment Variables

LangGuard can be configured using environment variables:

```bash
# LLM Provider Configuration
export GUARD_LLM_PROVIDER="openai"        # Options: "openai", or None for test mode
export GUARD_LLM_MODEL="gpt-4o-mini"      # OpenAI model to use
export GUARD_LLM_API_KEY="your-api-key"   # Your OpenAI API key
export LLM_TEMPERATURE="0.1"              # Temperature for LLM generation (0-1)
```

### Programmatic Configuration

```python
from langguard import GuardAgent

# Configure via code
agent = GuardAgent(
    llm="openai",  # or None for test mode
    config={
        "default_specification": "Your default security rules here"
    }
)
```

## 🛠️ Advanced Usage

### Advanced Usage

```python
from langguard import GuardAgent

# Create a guard agent
agent = GuardAgent(llm="openai")

# Screen a prompt with custom temperature
response = agent.screen(
    "How do I implement a binary search tree?",
    "Only allow code-related questions",
    temperature=0.1
)

print(f"Decision: {'PASS' if response['prompt_pass'] else 'FAIL'}")
print(f"Reasoning: {response['reason']}")
```

### Response Structure

LangGuard returns a `GuardResponse` dictionary with:

```python
{
    "prompt_pass": bool,  # True if prompt is safe, False otherwise
    "reason": str        # Explanation of the decision
}
```

## 🧪 Testing

The library includes comprehensive test coverage for various security scenarios:

```bash
# Run the OpenAI integration test
cd scripts
python test_openai.py

# Run unit tests
pytest tests/
```

### Example Security Scenarios

LangGuard can detect and prevent:

- **SQL Injection Attempts**: Blocks malicious database queries
- **System Command Execution**: Prevents file system access attempts
- **Personal Information Requests**: Blocks requests for PII
- **Jailbreak Attempts**: Detects attempts to bypass AI safety guidelines
- **Phishing Content Generation**: Prevents creation of deceptive content
- **Medical Advice**: Filters out specific medical diagnosis requests
- **Harmful Content**: Blocks requests for dangerous information

## 🏗️ Architecture

LangGuard follows a modular architecture:

```
langguard/
├── core.py       # Minimal core file (kept for potential future use)
├── agent.py      # GuardAgent implementation with LLM logic
├── models.py     # LLM provider implementations (OpenAI, Test)
└── __init__.py   # Package exports
```

### Components

- **GuardAgent**: Primary agent that screens prompts using LLMs
- **LLM Providers**: Pluggable LLM backends (OpenAI with structured output support)
- **GuardResponse**: Typed response structure with pass/fail status and reasoning

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🔗 Links

- [GitHub Repository](https://github.com/langguard/langguard-python)
- [Issue Tracker](https://github.com/langguard/langguard-python/issues)
- [PyPI Package](https://pypi.org/project/langguard/)

---