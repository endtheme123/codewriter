from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseLLMProvider(ABC):

    @abstractmethod
    async def stream_chat(self, message: str) -> AsyncGenerator[str, None]:
        pass