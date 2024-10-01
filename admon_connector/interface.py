from abc import ABC, abstractmethod
from collections.abc import AsyncIterator
from datetime import date, datetime

from pydantic import BaseModel, Field


class AdMonCost(BaseModel):
    id: int = Field(..., alias="ID Заказа")
    status: str = Field(..., alias="Статус")
    hold: str = Field(..., alias="Hold")
    totalPrice: float = Field(..., alias="Сумма")
    websites: str = Field(..., alias="Площадки")
    reward: float = Field(..., alias="Комиссия")
    time: datetime = Field(..., alias="Создан")


class ConversionPage(BaseModel):
    count: int
    rows: list[AdMonCost]


class Connector(ABC):
    @abstractmethod
    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        pass

    @abstractmethod
    def load(self, date_from: date, date_to: date) -> AsyncIterator[AdMonCost]:
        pass
