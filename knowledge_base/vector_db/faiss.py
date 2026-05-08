import faiss
import numpy as np
import uuid

from knowledge_base.vector_db.base import BaseVectorStore

class FaissVectorStore(BaseVectorStore):
    def __init__(self, dimension: int):
        self.dimension = dimension

        self.index = faiss.IndexFlatL2(dimension)
        print("FAISS dim:", self.index.d)
        

        # store metadata separately
        self.payloads = []
        self.ids = []

    def add(self, vectors, payloads):
        vectors = np.array(vectors).astype("float32")
        # if vectors.ndim == 1:
            # vectors = vectors.reshape(1, -1)
        print(vectors.shape)
        self.index.add(vectors)

        for payload in payloads:
            self.ids.append(str(uuid.uuid4()))
            self.payloads.append(payload)

    def search(self, vector, k=5):
        vector = np.array([vector]).astype("float32")

        scores, indices = self.index.search(vector, k)

        results = []

        for idx in indices[0]:
            if idx < len(self.payloads):
                results.append(self.payloads[idx])

        return results