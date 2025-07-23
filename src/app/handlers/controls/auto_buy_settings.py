from aiogram import Bot, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.inline.controls.settings import controls_keyboard

from app.handlers.routers import user_router

from app.repositories.schemas.user import UserSchema
from app.utils.ioc import ioc
from app.gift_service.buyer import GiftBuyer

from app.utils.functions.build_settings import build_settings_text

import asyncio


@user_router.message(Command(commands=["settings"]))
async def show_auto_buy(message: Message, user: UserSchema):
    buyer = ioc.get(GiftBuyer)

    await message.answer(build_settings_text(
        auto_buy_current_status=buyer.auto_buy,
        min_price=user.settings.price_min,
        max_price=user.settings.price_max,
        supply_limit=user.settings.supply_limit,
        cycles=user.settings.cycles,
    ), reply_markup=controls_keyboard(buyer.auto_buy))


@user_router.callback_query(ControlsCallback.filter(F.action == "auto_buy_settings"))
async def show_auto_buy_callback(callback: CallbackQuery, bot: Bot, user: UserSchema):
    buyer = ioc.get(GiftBuyer)

    await callback.message.edit_text(build_settings_text(
        auto_buy_current_status=buyer.auto_buy,
        min_price=user.settings.price_min,
        max_price=user.settings.price_max,
        supply_limit=user.settings.supply_limit,
        cycles=user.settings.cycles,
    ), reply_markup=controls_keyboard(buyer.auto_buy))
    await bot.answer_callback_query(callback.id)


@user_router.callback_query(ControlsCallback.filter(F.action == "auto_buy_toggle"))
async def toggle_auto_buy(callback: CallbackQuery, bot: Bot, user: UserSchema):
    buyer = ioc.get(GiftBuyer)

    await buyer.toggle_auto_buy(user)

    await callback.message.edit_text(build_settings_text(
        auto_buy_current_status=buyer.auto_buy,
        min_price=user.settings.price_min,
        max_price=user.settings.price_max,
        supply_limit=user.settings.supply_limit,
        cycles=user.settings.cycles,
    ), reply_markup=controls_keyboard(buyer.auto_buy))

    await bot.answer_callback_query(callback.id)
