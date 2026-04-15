from __future__ import annotations

from pup_agent.config import DEFAULT_MODEL
from pup_agent.providers.base import BaseProvider
from pup_agent.providers.mock_provider import MockProvider
from pup_agent.providers.openai_provider import OpenAIProvider


def create_provider(provider_name: str, model: str | None = None) -> BaseProvider:
    name = provider_name.strip().lower()
    if name == "openai":
        return OpenAIProvider(model=model or DEFAULT_MODEL)
    return MockProvider()
