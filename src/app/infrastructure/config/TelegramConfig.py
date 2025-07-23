__all__ = [
    "TelegramConfig"
]

from pydantic import BaseModel, SecretStr


class TelegramConfig(BaseModel):
    support: str
    token: SecretStr
