from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton

from app.helpers.fabric.controls import ControlsCallback

from app.helpers.texts import menu


def menu_keyboard(auto_buy_enabled):
    builder = InlineKeyboardBuilder()

    auto_buy_label = "🟢 Автопокупка" if auto_buy_enabled else "🔴 Автопокупка"

    builder.row(InlineKeyboardButton(text=auto_buy_label, callback_data=ControlsCallback(action="", value="").pack()))
    builder.row(InlineKeyboardButton(text="👤 Профиль", callback_data=ControlsCallback(action="show_profile", value="").pack()))
    builder.row(
        InlineKeyboardButton(text="⭐️ Пополнить баланс", callback_data=ControlsCallback(action="show_deposit_dialog", value="").pack()),
        InlineKeyboardButton(text="⚙️ Настройки автопокупки", callback_data=ControlsCallback(action="auto_buy_settings", value="").pack())
    )
    builder.row(InlineKeyboardButton(text="🎁 Каталог", callback_data=ControlsCallback(action="show_catalog", value="").pack()))
    builder.row(InlineKeyboardButton(text="🆘 Связь", callback_data=ControlsCallback(action="show_support", value="").pack()))

    return builder.as_markup(resize_keyboard=True)


def to_menu():
    builder = InlineKeyboardBuilder()
    builder.add(InlineKeyboardButton(text=menu.MAIN_MENU, callback_data=ControlsCallback(action="back_main_menu", value="").pack()))

    return builder.as_markup(resize_keyboard=True)
