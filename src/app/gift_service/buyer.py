__all__ = [
    "GiftBuyer"
]

from aiogram import Bot
from .observer import GiftObserver
import logging
from app.repositories.schemas.user import UserSchema, UserSettingsSchema


class GiftBuyer:
    def __init__(self, bot: Bot, gift_observer: GiftObserver, logger: logging.Logger) -> None:
        self.__bot = bot
        self.__observer = gift_observer
        self.__logger = logger

        self.__auto_buy_running: bool = False
        

    async def send_gift_by_id(self, gift_id: str, user_id: int, quantity: int = 1) -> bool:
        try:
            for _ in range(quantity):
                await self.__bot.send_gift(gift_id=gift_id, user_id=user_id)
            return True
        except Exception as e:
            self.__logger.error(f"[GiftBuyer] Failed to send gift {gift_id} to {user_id}: {e}")
            return False
        

    async def start_auto_buy(self, user: UserSchema) -> None:
        if self.__auto_buy_running:
            self.__logger.info("[GiftBuyer] Auto-buy already running")
            return

        self.__auto_buy_running = True
        self.__logger.info("[GiftBuyer] Auto-buy started")

        try:
            while self.__auto_buy_running:
                new_gifts = await self.__observer.start_auto_check()
                filtered_gifts = [
                    gift for gift in new_gifts
                    if user.settings.price_min <= gift.star_count <= user.settings.price_max
                    and gift.total_count <= user.settings.supply_limit
                ]

                for cycle in range(user.settings.cycles):
                    for gift in filtered_gifts:
                        success  = await self.send_gift_by_id(
                            gift_id=gift.id,
                            user_id=user.user_id,
                            quantity=user.settings.quantity
                        )
                        if success:
                            self.__logger.info(f"[GiftBuyer] Successfully sent gift {gift.id} to user {user.user_id}")

        except Exception as e:
            self.__auto_buy_running = False
            self.__logger.info(f"[GiftBuyer] Auto-buy error: {e}")
    

    async def stop_auto_buy(self) -> None:
        self.__auto_buy_running = False
        self.__logger.info("[GiftBuyer] Auto-buy manually stopped")
    
    
    @property
    def auto_buy(self) -> bool:
        return self.__auto_buy_running

    async def toggle_auto_buy(self, user: UserSchema) -> bool:
        if self.__auto_buy_running:
            await self.stop_auto_buy()
        else:
            await self.start_auto_buy(user)
        return self.__auto_buy_running
