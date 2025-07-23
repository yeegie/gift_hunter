__all__ = [
    "ControlsCallback"
]

from aiogram.filters.callback_data import CallbackData


class ControlsCallback(CallbackData, prefix='cb'):
    action: str
    value: str
