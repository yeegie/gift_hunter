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
from app.utils.functions.build_settings import build_settings_text

from aiogram.fsm.state import StatesGroup, State


class ConfirmSupplyStates(StatesGroup):
    value = State()


@user_router.callback_query(ControlsCallback.filter(F.action == "set_max_supply"))
async def set_supply(callback: CallbackQuery, bot: Bot, state: FSMContext, user_service: UserService) -> None:
    user = await user_service.get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=(
            "<b>Введите саплай</b>\n\n"
            "💡 Саплай — это тираж выпущенных подарков, чем меньше тираж тем более ценным и дорогим считается подарок\n\n"
            "Если не знаешь, что написать, вот тебе пример, обычно подарки выпускаются тиражами числом в 500К, 250К, самые дорогие бывают 1-20К\n\n"
            f"💎 <b>Текущий саплай {user.settings.supply_limit}</b>"
        ),
        reply_markup=to_settings()
    )
    await state.set_state(ConfirmSupplyStates.value)


@user_router.message(ConfirmSupplyStates.value)
async def process_custom_supply(message: Message, state: FSMContext, user_service: UserService, user: UserSchema):
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
            supply_limit=amount
        )
    )
    await state.clear()
    await message.answer(build_settings_text(
        auto_buy_current_status=user.settings.auto_buy,
        min_price=user.settings.price_min,
        max_price=user.settings.price_max,
        supply_limit=user.settings.supply_limit,
        cycles=user.settings.cycles,
        quantity=user.settings.quantity,
    ), reply_markup=controls_keyboard(user.settings.auto_buy))
