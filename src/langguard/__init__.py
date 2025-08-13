"""LangGuard - A Python library for language security."""

__version__ = "0.0.1"

from .core import hello, LangGuard
from .agent import GuardAgent, GuardResponse

__all__ = ["hello", "LangGuard", "GuardAgent", "GuardResponse", "__version__"]