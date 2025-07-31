from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.helpers.fabric.controls import ControlsCallback


def controls_keyboard(auto_buy_current_status: bool):
    builder = InlineKeyboardBuilder()

    auto_buy_label = {
        True: "🌑 Выключить",
        False: "🌕 Включить"
    }

    builder.row(InlineKeyboardButton(text=auto_buy_label[auto_buy_current_status], callback_data=ControlsCallback(action="auto_buy_toggle", value="").pack()))
    builder.row(
        InlineKeyboardButton(text="⭐️ Минимум", callback_data=ControlsCallback(action="set_min_price", value="").pack()),
        InlineKeyboardButton(text="⭐️ Максимум", callback_data=ControlsCallback(action="set_max_price", value="").pack()),
    )
    builder.row(InlineKeyboardButton(text="💎 Порог саплая", callback_data=ControlsCallback(action="set_max_supply", value="").pack()))
    builder.row(InlineKeyboardButton(text="🔄 Циклы автопокупки", callback_data=ControlsCallback(action="set_max_cycles", value="").pack()))
    builder.row(InlineKeyboardButton(text="🔢 Количество", callback_data=ControlsCallback(action="set_max_quantity", value="").pack()))
    builder.row(InlineKeyboardButton(text="🔙 Назад", callback_data=ControlsCallback(action="back_main_menu", value="").pack()))

    return builder.as_markup(resize_keyboard=True)


def to_settings():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text="⚙️ Настройки", callback_data=ControlsCallback(action="auto_buy_settings", value="").pack()))

    return builder.as_markup(resize_keyboard=True)
