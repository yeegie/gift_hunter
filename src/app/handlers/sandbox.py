from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.types import Message, MessageEntity, ContentType

from app.handlers.routers import user_router

from app.utils.ioc import ioc
from app.gift_service import GiftObserver

# @user_router.message()
# async def sandbox(message: Message): 
#     observer: GiftObserver = ioc.get(GiftObserver)

#     new_gifts = await observer.get_new_gifts()

#     # print(f"New gifts({len(new_gifts)}): {new_gifts}")
