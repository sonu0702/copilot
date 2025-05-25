# This file makes the 'models' directory a Python package.

from .gemini_llm import get_gemini_llm
from .ollama_llm import get_ollama_llm_config

__all__ = [
    "get_gemini_llm",
    "get_ollama_llm_config"
]
