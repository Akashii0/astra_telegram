import logging

from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.profiles.openai import OpenAIModelProfile

from app.core.settings import get_settings

settings = get_settings()
logger = logging.getLogger(__name__)

# NVIDIA NIM uses an OpenAI-compatible API surface.
_nvidia_provider = OpenAIProvider(
    base_url=settings.NVIDIA_BASE_URL,
    api_key=settings.NVIDIA_API_KEY,
)

_model = OpenAIChatModel(
    settings.NVIDIA_MODEL,
    provider=_nvidia_provider,
    profile=OpenAIModelProfile(
        openai_chat_supports_multiple_system_messages=False,
    ),
)

assistant_agent = Agent(
    _model,
    instructions=(
        "You are Astra, a helpful assistant in a Telegram chat. "
        "Keep replies concise — Telegram messages should be easy to read. "
        "Use plain text; avoid heavy markdown unless asked. "
        "Never invent facts; if you don't know, say so."
        "You were created by Raji Abdulhakeem, also known as Akashi. A software developer"
    ),
)
