__all__ = ["send_settings_menu"]

from aiogram import Bot
from aiogram.types import Message, CallbackQuery
from app.repositories.models.user import User
from app.helpers.keyboards.inline.controls.settings import controls_keyboard
from typing import Union


def build_menu(user: User) -> str:
    return (
        f"⚙️ <b>Настройки</b>\n"
        f"\n"
        f"🤖 <b>Автопокупка</b>\n"
        f"  └─ {'работает' if user.settings.auto_buy else 'не работает'}\n"
        f"\n"
        f"💰 <b>Лимит цены</b>\n"
        f"  └─ От {user.settings.price_min} до {user.settings.price_max} ⭐️\n"
        f"\n"
        f"💎 <b>Лимит саплая</b>\n"
        f"  └─ {user.settings.supply_limit}\n"
        f"\n"
        f"🔄 <b>Количество циклов</b>\n"
        f"  └─ {user.settings.cycles}\n"
        f"\n"
        f"🔢 <b>Сколько раз купить</b>\n"
        f"  └─ {user.settings.quantity}\n"
    )


async def send_settings_menu(
        event: Union[Message, CallbackQuery],
        user: User,
):
    text = build_menu(user)

    if isinstance(event, Message):
        await event.edit_text(
            text=text,
            reply_markup=controls_keyboard(user.settings.auto_buy),
        )
    elif isinstance(event, CallbackQuery):
        await event.message.edit_text(
            text=text,
            reply_markup=controls_keyboard(user.settings.auto_buy),
        )
