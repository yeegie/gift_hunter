__all__ = [
    "AppConfig"
]

from pydantic import BaseModel


class AppConfig(BaseModel):
    allow_buy_gifts: bool = False
