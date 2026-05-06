from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from typing import AsyncGenerator

from logger.logger import get_logger
from config import settings
from packages.ai.claude import ClaudeProvider
from packages.ai.dummy import MockProvider
from packages.ai.base import BaseLLMProvider


app = FastAPI()
logger = get_logger("main")





def get_provider() -> BaseLLMProvider:
    if settings.LLM_PROVIDER == "claude":
        return ClaudeProvider()
    # elif settings.LLM_PROVIDER == "openai":
    #     return OpenAIProvider()
    elif settings.LLM_PROVIDER == "mock":
        return MockProvider()
    else:
        raise ValueError("Unsupported provider")

async def stream_chat(message: str) -> AsyncGenerator[str, None]:
    provider = get_provider()

    async for token in provider.stream_chat(message):
        yield f"data: {token}\n\n"

    yield "data: [DONE]\n\n"

@app.post("/chat")
async def chat(request: Request):
    body = await request.json()
    message = body.get("message", "")

    logger.info(f"Incoming message: {message}")

    return StreamingResponse(
        stream_chat(message),
        media_type="text/event-stream"
    )