from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class SettingsSchema(BaseModel):
    user_id: int
    auto_buy: bool = False
    price_min: int = 0
    price_max: int = 0
    supply_limit: int = 0
    cycles: int = 0
    quantity: int = 0


class SettingsCreateSchema(BaseModel):
    user_id: int
    auto_buy: bool = False
    price_min: int = 15
    price_max: int = 100
    supply_limit: int = 500000
    cycles: int = 1
    quantity: int = 1


class SettingsUpdateSchema(BaseModel):
    auto_buy: Optional[bool] = None
    price_min: Optional[int] = None
    price_max: Optional[int] = None
    supply_limit: Optional[int] = None
    cycles: Optional[int] = None
    quantity: Optional[int] = None
