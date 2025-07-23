from aiogram.fsm.state import StatesGroup, State


class ConfirmAmountStates(StatesGroup):
    amount = State()
