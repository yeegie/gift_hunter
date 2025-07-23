from aiogram import Bot, F
from aiogram.types import Message, PreCheckoutQuery
from app.helpers.keyboards.inline.controls.main_menu import to_menu
from app.services.user.user import UserService

from app.handlers.routers import payment_router


@payment_router.message(F.successful_payment)
async def success_payment_handler(message: Message, user_service: UserService):
    await user_service.increase_balance(user_id=message.from_user.id, amount=message.successful_payment.total_amount)

    user = await user_service.get_user(message.from_user.id)
    await message.answer(text=f"Ваш баланс: <b>{user.balance}</b> ⭐️", reply_markup=to_menu())


@payment_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
