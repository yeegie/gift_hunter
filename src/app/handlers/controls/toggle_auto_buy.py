from aiogram import Bot, F
from aiogram.types import CallbackQuery

from app.helpers.fabric.controls import ControlsCallback
from app.helpers.keyboards.inline.controls.settings import controls_keyboard

from app.repositories.schemas.user import UserSchema
from app.repositories.schemas.settings import SettingsUpdateSchema

from app.handlers.routers import user_router

from app.utils.ioc import ioc
from app.gift_service.buyer import GiftBuyer

from app.services.user.user import UserService

from app.helpers.prepared_messages.send_settings_menu import send_settings_menu


@user_router.callback_query(ControlsCallback.filter(F.action == "auto_buy_toggle"))
async def toggle_auto_buy(callback: CallbackQuery, bot: Bot, user_service: UserService):
    # buyer = ioc.get(GiftBuyer)
    # await buyer.toggle_auto_buy(user)

    user = await user_service.get_user(callback.from_user.id)

    await user_service.change_user_settings(
        user.user_id,
        SettingsUpdateSchema(
            auto_buy=not user.settings.auto_buy
        )
    )

    await send_settings_menu(callback, user)
    await bot.answer_callback_query(callback.id)
