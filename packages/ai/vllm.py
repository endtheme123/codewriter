from typing import AsyncGenerator
from openai import AsyncOpenAI
from packages.ai.base import BaseLLMProvider
from config import settings
from logger.logger import get_logger

logger = get_logger("vllm")

class VLLMProvider(BaseLLMProvider):
    def __init__(self):
        # vLLM exposes OpenAI-compatible API
        self.client = AsyncOpenAI(
            api_key="EMPTY",  # vLLM ignores this
            base_url=settings.VLLM_BASE_URL  # e.g. http://localhost:8000/v1
        )

    async def stream_chat(self, message: str) -> AsyncGenerator[str, None]:
        logger.info("Calling vLLM")

        stream = await self.client.chat.completions.create(
            model=settings.VLLM_MODEL,  # e.g. "Qwen/Qwen2-1.5B-Instruct"
            messages=[
                {"role": "user", "content": message}
            ],
            max_tokens=1024,
            temperature=0.7,
            stream=True,
        )

        async for chunk in stream:
            # OpenAI/vLLM streaming format
            if chunk.choices:
                delta = chunk.choices[0].delta.content
                if delta:
                    yield delta

    async def chat(self, message: str) -> str:
        logger.info("Calling vLLM (non-stream)")

        response = await self.client.chat.completions.create(
            model=settings.VLLM_MODEL,
            messages=[
                {"role": "user", "content": message}
            ],
            max_tokens=1024,
            temperature=0.7,
        )

        return response.choices[0].message.content