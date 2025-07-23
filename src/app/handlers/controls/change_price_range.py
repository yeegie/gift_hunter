from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.controls.settings import to_settings

from app.handlers.routers import user_router


@user_router.callback_query(ControlsCallback.filter(F.action == "set_min_price"))
async def set_min_price(callback: CallbackQuery, bot: Bot) -> None:
    await callback.message.edit_text(
        text="Введите минимальную цену для автопокупки",
        reply_markup=to_settings()
    )

@user_router.callback_query(ControlsCallback.filter(F.action == "set_max_price"))
async def set_max_price(callback: CallbackQuery, bot: Bot) -> None:
    await callback.message.edit_text(
        text="Введите максимальную цену для автопокупки",
        reply_markup=to_settings()
    )
