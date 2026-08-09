import os

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

from utils.config import load_secrets

DEFAULT_MODEL = "openrouter/free"
# A vision-capable model on OpenRouter. Override via OPENROUTER_VISION_MODEL
# (secret/env) to switch between free and paid without code changes.
DEFAULT_VISION_MODEL = "meta-llama/llama-3.2-11b-vision-instruct:free"


def initialize_llm(model=None):
    load_dotenv()
    load_secrets()

    return ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.getenv("OPENROUTER_API_KEY"),
        model=model or os.getenv("OPENROUTER_MODEL", DEFAULT_MODEL),
    )


def initialize_vision_llm():
    """Return a multimodal (image-capable) chat model."""
    return initialize_llm(os.getenv("OPENROUTER_VISION_MODEL", DEFAULT_VISION_MODEL))
