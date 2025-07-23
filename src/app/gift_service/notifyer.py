__all__ = [
    "GiftNotifyer"
]

from aiogram import Bot
from typing import List
from aiogram.types import Gifts
from app.services.user.user import UserService


class GiftNotifyer():
    def __init__(
        self,
        bot: Bot,
        user_service: UserService
    ):
        super().__init__()
        self.__bot = bot
        self.__user_service = user_service

    async def notify(self, new_gifts: Gifts) -> None:
        users = await self.__user_service.get_all_users_by_notify(notify=True)

        if not users:
            return
        
        for user in users:
            try:
                await self.__bot.send_message(
                    user.user_id,
                    f"New gifts available: {', '.join(gift.title for gift in new_gifts.gifts)}"
                )
            except Exception as e:
                print(f"Failed to notify user {user.user_id}: {e}")