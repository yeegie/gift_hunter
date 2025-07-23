from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.inline.controls.settings import to_settings

from app.helpers.states.confirm_value import ConfirmAmountStates

from app.services.user.user import UserService
from app.repositories.schemas.user import UserUpdateSchema, UserSettingsUpdateSchema

from app.handlers.routers import user_router


@user_router.callback_query(ControlsCallback.filter(F.action == "set_max_supply"))
async def set_supply(callback: CallbackQuery, bot: Bot, state: FSMContext) -> None:
    await callback.message.edit_text(
        text="Введите саплай",
        reply_markup=to_settings()
    )
    await state.set_state(ConfirmAmountStates.amount)


@user_router.message(ConfirmAmountStates.amount)
async def process_custom_amount(message: Message, state: FSMContext, user_service: UserService):
    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer("Значение должна быть положительным числом, напиши еще раз")
            return
    except ValueError:
        await message.answer("Это не число, введи ещё раз")
        return
    
    await user_service.change_settings(
        user_id=message.from_user.id,
        settings=UserSettingsUpdateSchema(max_supply=amount)
    )
    await state.clear()
