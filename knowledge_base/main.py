from knowledge_base.embedding.base import BaseEmbedder
from knowledge_base.vector_db.base import BaseVectorStore
from knowledge_base.utils import chunk_text


class KnowledgeBase:
    def __init__(
        self,
        embedder: BaseEmbedder,
        vector_store: BaseVectorStore
    ):
        self.embedder = embedder
        self.vector_store = vector_store

    def add_documents(self, documents: list[dict]):
        if not documents:
            print("No documents to add")
            return
        texts = []
        payloads = []

        for doc in documents:
            chunks = chunk_text(doc["text"])

            for chunk in chunks:
                texts.append(chunk)
                payloads.append({
                    "text": chunk,
                    **doc.get("metadata", {})
                })

        vectors = self.embedder.embed(texts)

        self.vector_store.add(vectors, payloads)

    def search(self, query: str, k=5):
        vector = self.embedder.embed([query])[0]
        return self.vector_store.search(vector, k)