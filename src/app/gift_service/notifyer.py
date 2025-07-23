__all__ = [
    "GiftNotifyer"
]

from aiogram import Bot
from typing import List
from aiogram.types import Gifts


class GiftNotifyer():
    def __init__(self, bot: Bot):
        super().__init__()
        self.__bot = bot

    async def notify(self, new_gifts: Gifts) -> None:
        await self.__bot.send_message("@yeegie", "Hi")
