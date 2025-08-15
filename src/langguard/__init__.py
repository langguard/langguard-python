"""LangGuard - A library for language security."""

__version__ = "0.6.0"

# Primary interface
from .agent import GuardAgent, GuardResponse

__all__ = ["GuardAgent", "GuardResponse", "__version__"]
