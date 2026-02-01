from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings

LLMProvider = Literal["gemini", "groq"]


class Settings(BaseSettings):
    # LLM settings
    llm_provider: LLMProvider = "gemini"
    llm_temperature: float = 0.1

    # Provider-specific model names
    gemini_model: str = "gemini-2.5-flash"
    groq_model: str = "qwen/qwen3-32b"

    # Database
    database_path: Path = Path("marketplace_data.db")
    data_dir: Path = Path("data")

    # Debug mode - set DEBUG=true in .env to enable verbose logging
    debug: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
