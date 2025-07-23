from aiogram import Bot, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
import random

from app.handlers.routers import user_router

from app.helpers.keyboards.inline.controls.main_menu import to_menu


@user_router.message(CommandStart())
async def welcome(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(random.choice('🤖 💎 👀 👻 👾 🎁 📦 ⭐️'.split(' ')))
    await message.answer(f"Привет, {message.from_user.first_name} 👋", reply_markup=to_menu())
