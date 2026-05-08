from qdrant_client import QdrantClient
import uuid

class QdrantVectorStore(BaseVectorStore):
    def __init__(self, url: str, collection: str):
        self.client = QdrantClient(url=url)
        self.collection = collection

    def add(self, vectors, payloads):
        points = []
        for i, vec in enumerate(vectors):
            points.append({
                "id": str(uuid.uuid4()),
                "vector": vec,
                "payload": payloads[i],
            })

        self.client.upsert(
            collection_name=self.collection,
            points=points
        )

    def search(self, vector, k=5):
        results = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=k
        )
        return [r.payload for r in results]