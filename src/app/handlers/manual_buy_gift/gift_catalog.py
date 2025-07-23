from aiogram import Bot, F
from aiogram.types import Message
from aiogram.filters import Command

from app.handlers.routers import user_router
from app.helpers.keyboards.gifts_catalog.keyboard import gift_catalog_keyboard

from app.helpers.fabric.gift import GiftCallback
from app.helpers.fabric.controls import ControlsCallback
from aiogram.types import CallbackQuery

from app.utils.ioc import ioc
from app.gift_service.observer import GiftObserver


@user_router.message(Command(commands=['catalog']))
async def gift_catalog(message: Message, bot: Bot):
    gifts = await ioc.get(GiftObserver).get_all_gifts()
    await message.answer(f"<b>🎁 Купить вручную</b>", reply_markup=gift_catalog_keyboard(gifts))
    

@user_router.callback_query(ControlsCallback.filter(F.action == "show_catalog"))
async def gift_catalog(callback: CallbackQuery, bot: Bot):
    gifts = await ioc.get(GiftObserver).get_all_gifts()
    await callback.message.answer(f"<b>🎁 Купить вручную</b>", reply_markup=gift_catalog_keyboard(gifts))
    bot.answer_callback_query(callback.id)
