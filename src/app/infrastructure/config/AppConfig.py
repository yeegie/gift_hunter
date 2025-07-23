__all__ = [
    "AppConfig"
]

from pydantic import BaseModel


class AppConfig(BaseModel):
    allow_payments: bool = False
    allow_buy_gifts: bool = False
