import google.generativeai as genai
from config.settings import get_settings
import logging

logger = logging.getLogger(__name__)

try:
    settings = get_settings()
except ValueError as e:
    logger.critical(f"CRITICAL CONFIGURATION ERROR in gemini_llm.py: {e}")
    raise

try:
    genai.configure(api_key=settings.GEMINI_API_KEY)
except Exception as e:
    logger.critical(f"Failed to configure Google Generative AI SDK: {e}")
    raise

def get_gemini_llm():
    llm_config = {
        "model": "gemini/gemini-1.5-flash-latest",
        "google_api_key": settings.GEMINI_API_KEY
    }
    return llm_config
