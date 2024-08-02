from abc import ABC, abstractmethod
from collections.abc import AsyncGenerator
from datetime import date, datetime

from pydantic import BaseModel, Field


class AdMonCost(BaseModel):
    id: int = Field(..., alias="ID Заказа")
    # offerId: str = Field(..., alias='Статус')
    time: datetime = Field(..., alias="Создан")
    status: str = Field(..., alias="Статус")
    comment: str | None = Field(..., alias="Комментарий")
    totalPrice: float = Field(..., alias="Сумма")
    reward: float = Field(..., alias="Комиссия")
    hold: str = Field(..., alias="Hold")
    goal: str = Field(..., alias="Тип конверсии")
    updated: datetime = Field(..., alias="Обновлен")
    conversionWindowTime: str = Field(..., alias="Окно конверсии")


"""
Названия полей в csv могут отличаться от определенных в gql
{
	"fieldsToInclude[]": [
		"id",
		"city",
		"status",
		"hold",
		"totalPrice",
		"priceWithoutReturns",
		"websites",
		"reward",
		"time",
		"coupon",
		"referer",
		"conversionWindowTime",
		"updated",
		"offerId",
		"comment",
		"isPaid",
		"goal",
		"users",
		"partner",
		"partnerId"
	]
}
"""


class ConversionPage(BaseModel):
    count: int
    rows: list[AdMonCost]


class Connector(ABC):
    @abstractmethod
    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        pass

    @abstractmethod
    async def load(self, date_from: date, date_to: date) -> AsyncGenerator[AdMonCost]:
        pass
