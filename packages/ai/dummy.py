from typing import AsyncGenerator
import asyncio
from packages.ai.base import BaseLLMProvider

class MockProvider(BaseLLMProvider):
    async def stream_chat(self, message: str) -> AsyncGenerator[str, None]:
        for word in f"Mock response: {message}".split():
            await asyncio.sleep(0.2)
            yield word + " "
    async def chat(self, message: str) -> str:
        await asyncio.sleep(1)
        return f"Mock response: {message}"