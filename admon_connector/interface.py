from abc import ABC, abstractmethod
from datetime import date
from pydantic import BaseModel
from typing import Optional


    
class AdMonCost(BaseModel):
    id: str
    offerId: str
    date: date
    status: int
    comment: Optional[str]
    totalPrice: float
    reward: float
    hold: bool
    type: str
    
class AdMonCalc(BaseModel):
    date: date
    reward: float
   
class ConversionPage(BaseModel):
    count: int
    rows: list[AdMonCost | AdMonCalc]

class Connector(ABC):
    @abstractmethod
    async def check(self, date_from: date, date_to: date) -> dict[date, float]:
        pass

    @abstractmethod
    async def load(self, date_from: date, date_to: date) -> list[AdMonCost]:
        pass
