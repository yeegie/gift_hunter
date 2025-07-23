from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.helpers.fabric.payment import PaymentCallback
from app.helpers.fabric.controls import ControlsCallback


def payment_keyboard(from_main_menu: bool = False):
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text="⭐️ 50", callback_data=PaymentCallback(action="buy", value=50).pack()))
    builder.row(InlineKeyboardButton(text="⭐️ 100", callback_data=PaymentCallback(action="buy", value=100).pack()))
    builder.row(InlineKeyboardButton(text="⭐️ 200", callback_data=PaymentCallback(action="buy", value=200).pack()))
    builder.row(InlineKeyboardButton(text="⭐️ 500", callback_data=PaymentCallback(action="buy", value=500).pack()))
    builder.row(InlineKeyboardButton(text="⭐️ 1000", callback_data=PaymentCallback(action="buy", value=1000).pack()))
    builder.row(InlineKeyboardButton(text="Другая сумма", callback_data=PaymentCallback(action="buy_other_value", value=999).pack()))

    if from_main_menu:
        builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=ControlsCallback(action="back_main_menu", value="").pack()))

    return builder.as_markup(resize_keyboard=True)


def payment_confirm_keyboard(value: int):
    builder = InlineKeyboardBuilder()
    
    builder.row(InlineKeyboardButton(text=f"⭐️ {value} оплатить", pay=True))

    return builder.as_markup(resize_keyboard=True)
