from langchain_core.language_models.chat_models import BaseChatModel
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_groq import ChatGroq

from config import LLMProvider, get_settings


def get_llm(
    provider: LLMProvider | None = None,
    model: str | None = None,
    temperature: float | None = None,
) -> BaseChatModel:
    """
    Create an LLM instance based on the specified provider.

    Args:
        provider: LLM provider to use. Defaults to settings.llm_provider.
        model: Model name. Defaults to provider-specific setting.
        temperature: Model temperature. Defaults to settings.llm_temperature.

    Returns:
        Configured chat model instance.

    """
    settings = get_settings()
    provider = provider or settings.llm_provider
    temperature = temperature if temperature is not None else settings.llm_temperature

    match provider:
        case "gemini":
            return ChatGoogleGenerativeAI(
                model=model or settings.gemini_model,
                temperature=temperature,
                streaming=True,
            )
        case "groq":
            return ChatGroq(
                model=model or settings.groq_model,
                temperature=temperature,
                streaming=True,
            )
        case _:
            raise ValueError(f"Unknown LLM provider: {provider}")
