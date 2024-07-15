from abc import ABC, abstractmethod
from datetime import date
from pydantic import BaseModel
from typing import Any


    
class AdMonCost(BaseModel):
    id: int
    offerId: int
    date: date
    status: str
    comment: str
    totalPrice: float
    reward: float
    hold: bool
    type: str #Enum?
   
class ConversionPage(BaseModel):
    count: int
    rows: list[AdMonCost]

class Connector(ABC):
    @abstractmethod
    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        pass

    @abstractmethod
    async def load(self, date_from: date, date_to: date) -> list[AdMonCost]:
        pass
