# LangGuard 🛡️

[![Python Version](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI Version](https://img.shields.io/pypi/v/langguard)](https://pypi.org/project/langguard/)

LLM Agent as a library that acts as a security layer for LLM agent pipelines. The primary goal is to serve a circuit breaker for data entering pipelines. 

## Features

- **GuardAgent**: Agent that contains default specification on what to mark safe. Specification may be overridden. By default, it will attempt to flag all data that contains instructions that LLM AI agents may consider instructions. The GuardAgent is intended to be placed in the data stream before any intended instructions exist. The GuardAgent is optimized for light-weight, affordable models to balance its effectiveness as a security control with cost. **v0.7** currently achieves [90% block rate on a hackaprompt sample](https://github.com/langguard/langguard-trials) using gpt-5-nano

## Limitations

Currently only supports OpenAI as an LLM provider. Adapters for other providers wanted! Please contribute. **Note:** The provider needs to offer structured outputs to work with the GuardAgent properly

## Installation

Install LangGuard using pip:

```bash
pip install langguard
```

## Configuration

### Required Components

To use GuardAgent, you need:
1. **LLM Provider** - Currently supports `"openai"` or `None` (test mode)
2. **API Key** - Required for OpenAI (via environment variable)
3. **Prompt** - The text to screen (passed to `screen()` method)
4. **Model** - A small model like gpt-5-nano is recommended for cost`

### Setup Methods

#### Method 1: Environment Variables (Recommended)

```bash
export GUARD_LLM_PROVIDER="openai"        # LLM provider to use
export GUARD_LLM_API_KEY="your-api-key"   # Your OpenAI API key
export GUARD_LLM_MODEL="gpt-5-nano"      # Model of choice
export LLM_TEMPERATURE="1"              # Optional: Temperature 0-1 (default: 1)
```

Then in your code:
```python
from langguard import GuardAgent

agent = GuardAgent()  # Automatically uses environment variables
response = agent.screen("Your prompt here")
```

#### Method 2: Partial Configuration

```bash
export GUARD_LLM_API_KEY="your-api-key"   # API key must be in environment
```

```python
from langguard import GuardAgent

agent = GuardAgent(llm="openai")  # Specify provider in code
response = agent.screen("Your prompt here")
```

#### Method 3: Test Mode (No API Required)

```python
from langguard import GuardAgent

# No provider specified = test mode
agent = GuardAgent()  # Uses TestLLM, no API needed
response = agent.screen("Your prompt here")
# Always returns {"safe": false, "reason": "Test mode - always fails for safety"}
```

### Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|----------|
| `GUARD_LLM_PROVIDER` | LLM provider (`"openai"` or `None`) | No | `None` (test mode) |
| `GUARD_LLM_API_KEY` | API key for OpenAI | Yes (for OpenAI) | - |
| `GUARD_LLM_MODEL` | Model to use | No | `gpt-5-nano` |
| `LLM_TEMPERATURE` | Temperature (0-1) | No | `1` |

**Note**: Currently, API keys and models can only be configured via environment variables, not passed directly to the constructor.

## Quick Start

### Basic Usage - Plug and Play

```python
from langguard import GuardAgent

# Initialize GuardAgent with built-in security rules
guard = GuardAgent(llm="openai")

# Screen a user prompt with default protection
prompt = "How do I write a for loop in Python?"
response = guard.screen(prompt)

if response["safe"]:
    print(f"Prompt is safe: {response['reason']}")
    # Proceed with your LLM agent pipeline
else:
    print(f"Prompt blocked: {response['reason']}")
    # Handle the blocked prompt
```


### Response Structure

LangGuard returns a `GuardResponse` dictionary with:

```python
{
    "safe": bool,    # True if prompt is safe, False otherwise
    "reason": str    # Explanation of the decision
}
```

### Adding Custom Rules

```python
# Add additional rules to the default specification
guard = GuardAgent(llm="openai")

# Add domain-specific rules while keeping default protection
response = guard.screen(
    "Tell me about Python decorators",
    specification="Only allow Python and JavaScript questions"
)
# This adds your rules to the default security rules
```

### Overriding Default Rules

```python
# Completely replace default rules with custom specification
response = guard.screen(
    "What is a SQL injection?",
    specification="Only allow cybersecurity educational content",
    override=True  # This replaces ALL default rules
)
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


## Advanced Usage

### Advanced Usage

```python
from langguard import GuardAgent

# Create a guard agent
agent = GuardAgent(llm="openai")

# Use the simple boolean check
if agent.is_safe("DROP TABLE users;"):
    print("Prompt is safe")
else:
    print("Prompt blocked")

# With custom rules added to defaults
is_safe = agent.is_safe(
    "How do I implement a binary search tree?",
    specification="Must be about data structures"
)

# With complete rule override
is_safe = agent.is_safe(
    "What's the recipe for chocolate cake?",
    specification="Only allow cooking questions",
    override=True
)
```


## Testing

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

## Architecture

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Links

- [GitHub Repository](https://github.com/langguard/langguard-python)
- [Issue Tracker](https://github.com/langguard/langguard-python/issues)
- [PyPI Package](https://pypi.org/project/langguard/)

---