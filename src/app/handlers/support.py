from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.helpers.fabric.controls import ControlsCallback

from app.handlers.routers import user_router

from app.helpers.keyboards.inline.controls.main_menu import to_menu


@user_router.message(Command(commands=["support", "help"]))
async def support(message: Message):
    await message.answer("@yeegie 👈🏻 сюда")


@user_router.callback_query(ControlsCallback.filter(F.action == "show_support"))
async def support(callback_query: CallbackQuery, bot: Bot):
    await callback_query.message.answer("@yeegie 👈🏻 сюда")
    await bot.answer_callback_query(callback_query.id)
