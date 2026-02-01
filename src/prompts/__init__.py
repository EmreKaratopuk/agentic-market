"""Prompt loader and agent prompt composers."""

from functools import lru_cache
from pathlib import Path

PROMPTS_DIR = Path(__file__).parent


def load(*parts: str) -> str:
    """
    Load and concatenate prompt markdown files.

    Args:
        *parts: File paths relative to prompts dir (without .md extension).

    Returns:
        Concatenated prompt text with sections separated by double newlines.

    Raises:
        FileNotFoundError: If any prompt file doesn't exist.

    """
    sections = []
    for part in parts:
        path = PROMPTS_DIR / f"{part}.md"
        if not path.exists():
            raise FileNotFoundError(f"Prompt not found: {path}")
        sections.append(path.read_text().strip())
    return "\n\n".join(sections)


@lru_cache
def get_supervisor_prompt() -> str:
    """Load and compose the supervisor agent's system prompt."""
    return load(
        # Beginning (high attention) - identity and thinking
        "supervisor/role",
        "shared/chain_of_thought",
        # Middle (low attention) - reference material
        "supervisor/routing",
        "supervisor/examples",
        # End (high attention) - output and constraints
        "shared/output_format",
        "shared/verification",
        "shared/avoid",
    )


@lru_cache
def get_customer_prompt() -> str:
    """Load and compose the customer agent's system prompt."""
    return load(
        # Beginning (high attention) - identity and thinking
        "customer/role",
        "shared/chain_of_thought",
        # Middle (low attention) - reference material
        "customer/tools",
        "shared/clarification",
        "customer/examples",
        # End (high attention) - output and constraints
        "shared/output_format",
        "shared/verification",
        "shared/avoid",
    )


@lru_cache
def get_seller_prompt() -> str:
    """Load and compose the seller agent's system prompt."""
    return load(
        # Beginning (high attention) - identity and thinking
        "seller/role",
        "shared/chain_of_thought",
        # Middle (low attention) - reference material
        "seller/tools",
        "shared/clarification",
        "seller/examples",
        # End (high attention) - output and constraints
        "shared/output_format",
        "shared/verification",
        "shared/avoid",
    )
