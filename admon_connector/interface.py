from abc import ABC, abstractmethod
from datetime import date

from pydantic import BaseModel


class AdMonCost(BaseModel):
    cost_date: date
    source: str
    medium: str
    cost: float


class Connector(ABC):
    @abstractmethod
    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        pass

    @abstractmethod
    async def load(self, date_from: date, date_to: date) -> list[AdMonCost]:
        pass
