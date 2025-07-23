from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.controls.main_menu import menu_keyboard, to_menu

from app.handlers.routers import user_router

from app.utils.functions.build_profile import build_profile_text

from app.repositories.schemas.user import UserSchema


@user_router.message(Command(commands=["profile"]))
async def show_profile(message: Message, user: UserSchema):
    await message.answer(build_profile_text(user), reply_markup=to_menu())


@user_router.callback_query(ControlsCallback.filter(F.action == "show_profile"))
async def back_main_menu(callback: CallbackQuery, bot: Bot, user: UserSchema):
    await callback.message.edit_text(build_profile_text(user), reply_markup=to_menu())
    await bot.answer_callback_query(callback.id)
