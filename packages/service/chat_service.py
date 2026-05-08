from packages.ai.base import BaseLLMProvider
from knowledge_base.main import KnowledgeBase


class ChatService:
    def __init__(
        self,
        provider: BaseLLMProvider,
        knowledge_base: KnowledgeBase
    ):
        self.provider = provider
        self.knowledge_base = knowledge_base

    async def chat(self, message: str):
        chunks = self.knowledge_base.search(
            message,
            k=5
        )

        context = "\n\n".join([
            chunk["text"]
            for chunk in chunks
        ])

        prompt = f"""
        Use the following knowledge base context to answer.

        KNOWLEDGE BASE:
        {context}

        USER QUESTION:
        {message}

        Rules:
        - Prefer knowledge base information
        - If information is missing, say unknown
        """

        return await self.provider.chat(prompt)

    async def stream_chat(self, message: str):
        chunks = self.knowledge_base.search(
            message,
            k=5
        )

        context = "\n\n".join([
            chunk["text"]
            for chunk in chunks
        ])

        prompt = f"""
        Use the following knowledge base context to answer.

        KNOWLEDGE BASE:
        {context}

        USER QUESTION:
        {message}
        """

        async for token in self.provider.stream_chat(prompt):
            yield token