import logging
from config.settings import get_settings

logger = logging.getLogger(__name__)

try:
    settings = get_settings()
except ValueError as e:
    logger.critical(f"CRITICAL CONFIGURATION ERROR in ollama_llm.py: {e}")
    raise
def get_ollama_llm_config():
    """
    Returns a configuration dictionary for the Ollama LLM.
    This can be expanded to return an instance of an OllamaLLM class if needed.
    """
    OLLAMA_API_URL = getattr(settings, 'OLLAMA_API_URL', 'http://127.0.0.1:11434')
    OLLAMA_MODEL_NAME = getattr(settings, 'OLLAMA_MODEL_NAME', 'ollama/llama3.2:latest')

    return {
        "model_name": "ollama/llama3.2:latest",
        "api_url": "http://127.0.0.1:11434",
        "type": "ollama" 
    }
