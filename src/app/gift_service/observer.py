__all__ = [
    "GiftObserver"
]

import asyncio
import logging

from aiogram import Bot
from aiogram.types import Gift, Gifts
from typing import Optional, List

from .notifyer import GiftNotifyer


class GiftObserver():
    __default_gift_ids: set[str] = {
        "5170145012310081615", "5170233102089322756", "5170250947678437525",
        "5168103777563050263", "5170144170496491616", "5170314324215857265",
        "5170564780938756245", "5168043875654172773", "5170690322832818290",
        "5170521118301225164", "6028601630662853006"
    }  # 💝 🧸 🎁 🌹 🎂 💐 🚀 🏆 💍 💎 🍾

    def __init__(
        self,
        bot: Bot,
        gift_notifyer: GiftNotifyer,
        logger: logging.Logger,
    ):
        self.__bot = bot
        self.__notifyer = gift_notifyer

        self.__logger = logger

        self.__autocheck_running = False

    async def get_all_gifts(self) -> List[Gift]:
        return (await self.__bot.get_available_gifts()).gifts

    async def get_new_gifts(self, notify_users: bool = False) -> List[Gift]:
        filtered_gifts = [gift for gift in await self.get_all_gifts() if gift.id not in self.__default_gift_ids]

        if filtered_gifts and notify_users:
            self.__notifyer.notify(filtered_gifts)

        return filtered_gifts

    def stop_auto_check(self) -> None:
        self.__autocheck_running = False

    async def start_auto_check(self, delay: float = 0.5, error_delay: float = 1) -> List[Gift]:
        self.__autocheck_running = True
        self.__logger.info(f"[GiftObserver] Auto-check started")
        while self.__autocheck_running:
            try:
                new_gifts = await self.get_new_gifts()

                if new_gifts:
                    self.__logger.info(f"[GiftObserver] New gifts")
                    self.stop_auto_check()
                    return new_gifts

                self.__logger.info(
                    f"[GiftObserver] New gifts not found delay {delay}")

                await asyncio.sleep(delay)
            except Exception as e:
                self.__logger.error(f"[GiftObserver] Check gifts error {e}")
                await asyncio.sleep(error_delay)

    @property
    def autocheck_running(self) -> bool:
        return self.__autocheck_running
