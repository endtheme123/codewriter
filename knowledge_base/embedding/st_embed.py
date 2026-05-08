from sentence_transformers import SentenceTransformer
from knowledge_base.embedding.base import BaseEmbedder
from typing import List

class SentenceTransformerEmbedder(BaseEmbedder):
    def __init__(self, model_name="BAAI/bge-small-en-v1.5"):
        self.model = SentenceTransformer(model_name, device="cpu")

    def embed(self, texts: List[str]) -> List[List[float]]:
        return self.model.encode(
            texts,
            batch_size=32,
            normalize_embeddings=True
        ).tolist()