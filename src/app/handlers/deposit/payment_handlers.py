from aiogram import Bot, F
from aiogram.types import Message, PreCheckoutQuery
from app.handlers.routers import user_router
from app.services.user.user import UserService
from app.helpers.keyboards.controls.main_menu import to_menu


@user_router.message(F.successful_payment)
async def success_payment_handler(message: Message, user_service: UserService):
    await user_service.increase_balance(user_id=message.from_user.id, amount=message.successful_payment.total_amount)

    user = await user_service.get_user(message.from_user.id)
    await message.answer(text=f"Ваш баланс {user.balance} ⭐️", reply_markup=to_menu())


@user_router.pre_checkout_query()
async def pre_checkout_handler(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.answer(ok=True)
