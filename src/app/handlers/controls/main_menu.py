from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.inline.controls.main_menu import menu_keyboard

from app.handlers.routers import user_router

from app.repositories.schemas.user import UserSchema

from app.utils.functions.build_main_menu import build_main_menu_text


@user_router.message(Command(commands=["menu"]))
async def show_main_menu(message: Message, bot: Bot, user: UserSchema):
    await message.answer(build_main_menu_text(user), reply_markup=menu_keyboard())


@user_router.callback_query(ControlsCallback.filter(F.action == "back_main_menu"))
async def back_main_menu(callback: CallbackQuery, bot: Bot, user: UserSchema):
    await callback.message.edit_text(build_main_menu_text(user), reply_markup=menu_keyboard())
    await bot.answer_callback_query(callback.id)
