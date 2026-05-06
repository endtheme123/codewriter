from typing import AsyncGenerator
from openai import AsyncOpenAI
from packages.ai.base import BaseLLMProvider
from config import settings
from logger.logger import get_logger

logger = get_logger("openai")

class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)

    async def stream_chat(self, message: str) -> AsyncGenerator[str, None]:
        logger.info("Calling OpenAI")

        stream = await self.client.chat.completions.create(
            model=settings.OPENAI_MODEL,
            messages=[{"role": "user", "content": message}],
            stream=True,
        )

        async for chunk in stream:
            delta = chunk.choices[0].delta.content
            if delta:
                yield delta