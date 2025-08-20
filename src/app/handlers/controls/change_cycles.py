from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.inline.controls.settings import controls_keyboard, to_settings

from app.services.user.user import UserService
from app.repositories.schemas.user import UserUpdateSchema, UserSchema
from app.repositories.schemas.settings import SettingsUpdateSchema

from app.handlers.routers import user_router
from app.helpers.prepared_messages.send_settings_menu import send_settings_menu

from aiogram.fsm.state import StatesGroup, State

from app.repositories.models.user import User


class ConfirmCyclesStates(StatesGroup):
    value = State()


@user_router.callback_query(ControlsCallback.filter(F.action == "set_max_cycles"))
async def set_cycle(callback: CallbackQuery, bot: Bot, state: FSMContext, user: User) -> None:
    await callback.message.edit_text(
        text=(
            "✨ <b>Введите количество циклов</b>\n\n"
            "🔄 Циклы — это то, сколько раз бот будет проходить по списку подарков, подходящих под ваши настройки.\n\n"
            "💡 Например: есть 3 подходящих подарка, а вы указали 2 цикла — бот пройдётся по списку дважды и купит столько подарков, сколько указано в поле <b>«количество»</b>\n\n"
            f"<b>Текущее значение {user.settings.cycles}</b>"
        ),
        reply_markup=to_settings()
    )
    await state.set_state(ConfirmCyclesStates.value)


@user_router.message(ConfirmCyclesStates.value)
async def process_custom_cycles(message: Message, state: FSMContext, user_service: UserService, user: User):
    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer("Значение должна быть положительным числом, напиши еще раз")
            return
    except ValueError:
        await message.answer("Это не число, введи ещё раз")
        return
    
    await user_service.change_user_settings(
        message.from_user.id,
        SettingsUpdateSchema(
            cycles=amount
        )
    )

    await state.clear()
    await send_settings_menu(message, user)
    
