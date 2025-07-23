__all__ = [
    "GiftCallback"
]

from aiogram.filters.callback_data import CallbackData


class GiftCallback(CallbackData, prefix='cb'):
    action: str
    value: str