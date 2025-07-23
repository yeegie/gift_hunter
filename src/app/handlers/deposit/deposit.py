from aiogram import Bot, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command

from app.handlers.routers import user_router
from app.helpers.keyboards.payments import payment_keyboard, payment_confirm_keyboard

from app.helpers.fabric.payment import PaymentCallback
from app.helpers.fabric.controls import ControlsCallback
from aiogram.types import CallbackQuery

from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from app.utils.functions.build_deposit_dialog import build_deposit_dialog_text


class PaymentStates(StatesGroup):
    waiting_for_custom_amount = State()

# "Другая сумма"
@user_router.callback_query(PaymentCallback.filter(F.action == "buy_other_value"))
async def buy_other_value(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Введи сумму (целое число)")
    await state.set_state(PaymentStates.waiting_for_custom_amount)
    await bot.answer_callback_query(callback.id)


@user_router.message(PaymentStates.waiting_for_custom_amount)
async def process_custom_amount(message: Message, state: FSMContext, bot: Bot):
    try:
        amount = int(message.text)
        if amount <= 0:
            await message.answer("Сумма должна быть положительным числом. Попробуй еще раз:")
            return
    except ValueError:
        await message.answer("Это не число. Введи сумму цифрами:")
        return

    await message.answer(f"Вы ввели сумму: {amount} ⭐️\nГотовим счёт для оплаты...")

    prices = [LabeledPrice(label="Пожертвование", amount=amount)]
    await message.answer_invoice(
        title="Пополнение баланса",
        description=f"└─ + {amount} ⭐️",
        prices=prices,
        provider_token="",
        payload=f"custom_{amount}",
        currency="XTR",
        reply_markup=payment_confirm_keyboard(amount)
    )

    await state.clear()

# Обычное пополнение
@user_router.callback_query(PaymentCallback.filter(F.action == "buy"))
async def send_invoice_handler(callback: CallbackQuery, callback_data: PaymentCallback, bot: Bot):
    prices = [LabeledPrice(label="XTR", amount=callback_data.value)]
    await callback.message.answer_invoice(
        title="Пополнение баланса",
        description=f"└─ + {callback_data.value} ⭐️",
        prices=prices,
        provider_token="",
        payload=f"buy_{callback_data.value}_stars",
        currency="XTR",
        reply_markup=payment_confirm_keyboard(callback_data.value),
    )
    await bot.answer_callback_query(callback.id)


@user_router.message(Command(commands=['deposit']))
async def payments(message: Message, bot: Bot):
    current_balance = (await bot.get_my_star_balance()).amount

    await message.answer(build_deposit_dialog_text(current_balance), reply_markup=payment_keyboard())
    

@user_router.callback_query(ControlsCallback.filter(F.action == "show_deposit_dialog"))
async def payments(callback: CallbackQuery, bot: Bot):
    current_balance = (await bot.get_my_star_balance()).amount

    await callback.message.edit_text(build_deposit_dialog_text(current_balance), reply_markup=payment_keyboard(from_main_menu=True))
