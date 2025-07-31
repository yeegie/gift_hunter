from aiogram import Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.inline.controls.settings import to_settings

from app.services.user.user import UserService
from app.repositories.schemas.user import UserSchema
from app.repositories.schemas.settings import SettingsUpdateSchema

from app.utils.functions.build_settings import build_settings_text
from app.helpers.keyboards.inline.controls.settings import controls_keyboard

from app.handlers.routers import user_router

from aiogram.fsm.state import StatesGroup, State


class ConfirmMinPriceStates(StatesGroup):
    value = State()


@user_router.callback_query(ControlsCallback.filter(F.action == "set_min_price"))
async def set_min_price(callback: CallbackQuery, bot: Bot, user_service: UserService, state: FSMContext) -> None:
    user = await user_service.get_user(callback.from_user.id)

    await callback.message.edit_text(
        text=(
            "Введите минимальную цену в звёздах для автопокупки\n\n"
            f"⭐️ <b>Текущее значение {user.settings.price_min}</b>"
        ),
        reply_markup=to_settings()
    )
    await state.set_state(ConfirmMinPriceStates.value)

@user_router.message(ConfirmMinPriceStates.value)
async def process_custom_min_price(message: Message, state: FSMContext, user_service: UserService):
    user = await user_service.get_user(message.from_user.id)

    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer("Значение должно быть положительным числом, напиши еще раз", reply_markup=to_settings())
            return
        elif amount > user.settings.price_max:
            await message.answer(f"Минимальная цена не может быть больше максимальной - <b>{user.settings.price_max}</b>, введи ещё раз", reply_markup=to_settings())
            return
    except ValueError:
        await message.answer("Это не число, введи ещё раз")
        return

    await user_service.change_user_settings(
        message.from_user.id,
        SettingsUpdateSchema(
            price_min=amount
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
