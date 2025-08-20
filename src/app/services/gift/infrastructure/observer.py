from ..domain.observer_base import BaseObserver
from ..domain.observer_interface import IObserver
from .purchase_queue import PurchaseQueueRabbit
from .subscriber import Subscriber

from app.services.user.user import UserService
from app.repositories.models.user import User

from aiogram import Bot
from aiogram.types import Gift

import asyncio
import logging


class Observer(BaseObserver, IObserver):
    __default_gift_ids: set[str] = {
        "5170145012310081615", "5170233102089322756", "5170250947678437525",
        "5168103777563050263", "5170144170496491616", "5170314324215857265",
        "5170564780938756245", "5168043875654172773", "5170690322832818290",
        "5170521118301225164", "6028601630662853006"
    }  # 💝 🧸 🎁 🌹 🎂 💐 🚀 🏆 💍 💎 🍾

    def __init__(
        self,
        user_service: UserService,
        purchase_queue: PurchaseQueueRabbit,
        bot: Bot,
        logger: logging.Logger,
    ) -> None:
        super().__init__()
        self.__purchase_queue = purchase_queue
        self.__user_service = user_service
        self.__bot = bot
        self.__logger = logger

        self.__autocheck_running = False

        asyncio.run(self.initialize())
        self.start_auto_check() if not self.__autocheck_running else None

    async def initialize(self) -> None:
        """Initialization of subscribers when the application starts."""
        self.__subscribers = await self.restore_subscribers()

    async def restore_subscribers(self) -> dict[int, Subscriber]:
        """Fills the list with subscribers (those who have auto-purchase enabled in the database entry). Used only once - when the application is launched, when the list is empty and needs to be restored."""
        users: list[User] = await self.__user_service.get_all_users_by_autobuy()
        subscribers = {user.user_id: Subscriber(user, self.__purchase_queue) for user in users}
        return subscribers
    
    async def get_all_gifts(self) -> list[Gift]:
        return (await self.__bot.get_available_gifts()).gifts
    
    async def get_new_gifts(self, notify_users: bool = False) -> list[Gift]:
        filtered_gifts = [gift for gift in await self.get_all_gifts() if gift.id not in self.__default_gift_ids]

        if filtered_gifts and notify_users:
            self.__notifyer.notify(filtered_gifts)

        return filtered_gifts
    
    def stop_auto_check(self) -> None:
        self.__autocheck_running = False

    async def start_auto_check(self, delay: float = 0.5, error_delay: float = 1) -> list[Gift]:
        self.__autocheck_running = True
        self.__logger.info(f"[GiftObserver] Auto-check started")
        while self.__autocheck_running:
            try:
                new_gifts = await self.get_new_gifts()

                if new_gifts:
                    self.__logger.info(f"[GiftObserver] New gifts")
                    self.stop_auto_check()

                    # Notify users about new gifts
                    super().notify_subscribers(new_gifts)
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
