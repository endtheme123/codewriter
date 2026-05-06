from typing import AsyncGenerator
import asyncio
from packages.ai.base import BaseLLMProvider

class MockProvider(BaseLLMProvider):
    async def stream_chat(self, message: str) -> AsyncGenerator[str, None]:
        for word in f"Mock response: {message}".split():
            await asyncio.sleep(0.2)
            yield word + " "