__all__ = [
    "PaymentCallback"
]

from aiogram.filters.callback_data import CallbackData


class PaymentCallback(CallbackData, prefix='cb'):
    action: str
    value: int
