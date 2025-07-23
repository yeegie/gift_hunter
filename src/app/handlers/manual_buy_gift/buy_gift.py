from aiogram import Bot, F
from aiogram.types import Message
from aiogram.filters import Command

from app.handlers.routers import user_router
from app.helpers.keyboards.gifts_catalog.keyboard import gift_catalog_keyboard
from app.helpers.keyboards.payments.keyboard import payment_confirm_keyboard

from app.helpers.fabric.gift import GiftCallback
from aiogram.types import CallbackQuery

from app.repositories.schemas.user import UserSchema


@user_router.callback_query(GiftCallback.filter(F.action == "buy_gift"))
async def buy_gift(callback: CallbackQuery, callback_data: GiftCallback, bot: Bot, user: UserSchema):
    gift_price = int(callback_data.value.split("-")[1])

    if user.balance < gift_price:
        price_difference = (user.balance-gift_price) * -1
        await callback.message.answer(f"Не хватает {price_difference} ⭐️", )  # тут остановился
    else:
        await callback.message.answer("щя будет")
    await bot.answer_callback_query(callback.id)
