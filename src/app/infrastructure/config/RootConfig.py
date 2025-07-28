__all__ = [
    "RootConfig"
]


from pydantic import BaseModel
import typing as t

from .DatabaseConfig import DatabaseConfig
from .TelegramConfig import TelegramConfig
from .WebhookConfig import WebhookConfig
from .PaymentConfig import PaymentConfig


class RootConfig(BaseModel):
    telegram: TelegramConfig
    database: DatabaseConfig
    webhook: WebhookConfig
    payment: PaymentConfig
