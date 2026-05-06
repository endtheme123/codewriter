from typing import AsyncGenerator
from anthropic import AsyncAnthropic
from packages.ai.base import BaseLLMProvider
from config import settings
from logger.logger import get_logger

logger = get_logger("claude")

class ClaudeProvider(BaseLLMProvider):
    def __init__(self):
        self.client = AsyncAnthropic(
            api_key=settings.ANTHROPIC_API_KEY
        )

    async def stream_chat(self, message: str) -> AsyncGenerator[str, None]:
        logger.info("Calling Claude")

        stream = await self.client.messages.create(
            model=settings.CLAUDE_MODEL,
            max_tokens=1024,
            messages=[
                {"role": "user", "content": message}
            ],
            stream=True,
        )

        async for event in stream:
            # Claude streaming events are structured
            if event.type == "content_block_delta":
                delta = event.delta.text
                if delta:
                    yield delta