from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseVectorStore(ABC):
    @abstractmethod
    def add(self, vectors: List[List[float]], payloads: List[Dict[str, Any]]):
        pass

    @abstractmethod
    def search(self, vector: List[float], k: int):
        pass