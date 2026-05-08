from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse

from container import chat_service


app = FastAPI()


async def stream_chat(message: str):
    async for token in chat_service.stream_chat(message):
        yield f"data: {token}\n\n"

    yield "data: [DONE]\n\n"


@app.post("/chat")
async def chat(request: Request):
    body = await request.json()

    result = await chat_service.chat(
        body["message"]
    )

    return {
        "response": result
    }


@app.post("/chat_stream")
async def chat_stream(request: Request):
    body = await request.json()

    return StreamingResponse(
        stream_chat(body["message"]),
        media_type="text/event-stream"
    )