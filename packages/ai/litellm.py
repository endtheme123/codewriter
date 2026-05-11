from typing import AsyncGenerator

import litellm

from packages.ai.base import BaseLLMProvider
from config import settings
from logger.logger import get_logger


logger = get_logger("litellm")


class LiteLLMProvider(BaseLLMProvider):
    def __init__(self):
        self.model = settings.LITELLM_MODEL

        # Optional for OpenAI-compatible endpoints like vLLM/OpenRouter
        self.api_base = settings.LITELLM_API_BASE
        self.api_key = settings.LITELLM_API_KEY

    async def stream_chat(self, message: str) -> AsyncGenerator[str, None]:
        logger.info("Calling LiteLLM (stream)")

        response = await litellm.acompletion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            api_base=self.api_base,
            api_key=self.api_key,
            max_tokens=1024,
            temperature=0.7,
            stream=True,
        )

        async for chunk in response:
            try:
                delta = chunk.choices[0].delta.content

                if delta:
                    yield delta

            except Exception as e:
                logger.error(f"Streaming error: {e}")

    async def chat(self, message: str) -> str:
        logger.info("Calling LiteLLM (non-stream)")

        response = await litellm.acompletion(
            model=self.model,
            messages=[
                {
                    "role": "user",
                    "content": message
                }
            ],
            api_base=self.api_base,
            api_key=self.api_key,
            max_tokens=1024,
            temperature=0.7,
        )

        return response.choices[0].message.content