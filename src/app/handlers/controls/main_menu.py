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
    await message.answer(build_main_menu_text(user), reply_markup=menu_keyboard(user.settings.auto_buy))


@user_router.callback_query(ControlsCallback.filter(F.action == "auto_buy_status"))
async def autobuy_status_label(callback: CallbackQuery, bot: Bot):
    await callback.answer("Это статус, изменение автопокупки в настройках")


@user_router.callback_query(ControlsCallback.filter(F.action == "back_main_menu"))
async def back_main_menu(callback: CallbackQuery, bot: Bot, user: UserSchema):
    await callback.message.edit_text(build_main_menu_text(user), reply_markup=menu_keyboard(user.settings.auto_buy))
    await bot.answer_callback_query(callback.id)
