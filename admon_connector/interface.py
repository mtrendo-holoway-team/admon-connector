from abc import ABC, abstractmethod
from collections.abc import Iterator
from datetime import date

from pydantic import BaseModel


class AdMonCost(BaseModel):
    id: str
    offerId: str
    date: date
    status: int
    comment: str | None
    totalPrice: float
    reward: float
    hold: bool
    type: str


class AdMonCalc(BaseModel):
    date: date
    reward: float


class ConversionPage(BaseModel):
    count: int
    rows: list[AdMonCost] | list[AdMonCalc]


class Connector(ABC):
    @abstractmethod
    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        pass

    @abstractmethod
    async def load(self, date_from: date, date_to: date) -> Iterator[AdMonCost]:
        pass
