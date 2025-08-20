from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.inline.controls.settings import controls_keyboard

from app.handlers.routers import user_router

from app.repositories.schemas.user import UserSchema
from app.utils.ioc import ioc
from app.gift_service.buyer import GiftBuyer
from aiogram.fsm.context import FSMContext

from app.helpers.prepared_messages.send_settings_menu import send_settings_menu


@user_router.message(Command(commands=["settings"]))
async def show_auto_buy(message: Message, user: UserSchema, state: FSMContext, bot: Bot):
    await state.clear()
    buyer = ioc.get(GiftBuyer)
    await send_settings_menu(message, user)


@user_router.callback_query(ControlsCallback.filter(F.action == "auto_buy_settings"))
async def show_auto_buy_callback(callback: CallbackQuery, bot: Bot, user: UserSchema, state: FSMContext):
    await state.clear()
    buyer = ioc.get(GiftBuyer)
    await send_settings_menu(callback, user)
    await bot.answer_callback_query(callback.id)
