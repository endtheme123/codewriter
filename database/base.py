# domain/repositories/user_repository.py

from abc import ABC, abstractmethod
from typing import List, Optional

class RiskRepository(ABC):

    @abstractmethod
    def get_all(self) -> List[dict]:
        pass

    @abstractmethod
    def get_by_id(self, risk_id: int) -> Optional[dict]:
        pass

    @abstractmethod
    def create(self, risk_data: dict) -> dict:
        pass