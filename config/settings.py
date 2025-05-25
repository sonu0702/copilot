import os
from dotenv import load_dotenv
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    GEMINI_API_KEY: str
    KNOWLEDGE_BASE_PATH: str = "knowledgebase/navadr.txt"
    OLLAMA_API_URL: str = "http://127.0.0.1:11434/api/chat"
    OLLAMA_MODEL_NAME: str = "llama3.2:latest"
    LLM_PROVIDER: str = "ollama"  # Default to gemini, can be "ollama"

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = 'ignore'

_settings_instance = None

def get_settings():
    global _settings_instance
    if _settings_instance is None:
        project_root = Path(__file__).parent.parent
        dotenv_path = project_root / ".env"

        if dotenv_path.exists():
            load_dotenv(dotenv_path=dotenv_path)
        else:
            # In a production setting, you might want to raise an error if .env is critical
            # or rely purely on environment variables set in the deployment environment.
            # For now, we'll just log a warning if it's missing.
            # Consider using a more robust logging setup for production.
            pass


        _settings_instance = Settings()
        if not _settings_instance.GEMINI_API_KEY or _settings_instance.GEMINI_API_KEY == "YOUR_GEMINI_API_KEY_HERE":
            raise ValueError(
                "GEMINI_API_KEY not found or not set. Please set it in environment variables or .env file."
            )
    return _settings_instance
