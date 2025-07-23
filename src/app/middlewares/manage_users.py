from typing import Callable, Dict, Any, Awaitable, Union

from aiogram import BaseMiddleware, Bot
from aiogram.types import Message, CallbackQuery

from app.utils.ioc import ioc

from app.services.user.user import UserService
from app.repositories.schemas.user import (
    UserCreateSchema
)


class ManageUserMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Union[Message, CallbackQuery], Dict[str, Any]], Awaitable[Any]],
        event: Union[Message, CallbackQuery],
        data: Dict[str, Any]
    ) -> Any:
        user_service = ioc.get(UserService)

        user = await user_service.get_user(event.from_user.id)

        is_bot = False
        if isinstance(event, Message):
            is_bot = event.from_user.is_bot
        elif isinstance(event, CallbackQuery):
            is_bot = event.message.from_user.is_bot

        if not is_bot:
            bot: Bot = data['bot']
            if user is None:
                # New user
                await user_service.create_user(
                    UserCreateSchema(
                        user_id=event.from_user.id,
                        fullname=event.from_user.full_name,
                        username=event.from_user.username,
                    )
                )

        data['user'] = user
        data['user_service'] = user_service

        return await handler(event, data)
