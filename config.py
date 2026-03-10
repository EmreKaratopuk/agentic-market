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

    # Vector store
    qdrant_path: Path = Path("qdrant_storage")
    qdrant_collection: str = "marketplace_docs"
    docs_dir: Path = Path("docs")

    # Embeddings
    embedding_model: str = "gemini-embedding-001"

    debug: bool = True


@lru_cache
def get_settings() -> Settings:
    return Settings()
