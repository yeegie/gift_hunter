from aiogram import Bot, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from app.handlers.routers import user_router

@user_router.callback_query(F.data == "clear_state")
async def clear_state(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await callback.message.answer("Отменил")
    await bot.answer_callback_query(callback.id)
