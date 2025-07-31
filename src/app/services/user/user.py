__all__ = ["UserService"]

from typing import Optional, List
from app.repositories.user.repository import UserRepository
from app.repositories.settings.repository import SettingsRepository

from app.repositories.models.user import User

from app.repositories.schemas.user import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
)
from app.repositories.schemas.settings import (
    SettingsCreateSchema,
    SettingsUpdateSchema
)


class UserService:
    def __init__(self, repository: UserRepository, settings_repository: SettingsRepository):
        self.__user_repository = repository
        self.__settings_repository = settings_repository

    async def create_user(self, dto: UserCreateSchema) -> User:
        return await self.__user_repository.create(dto)

    async def create_user_with_settings(self, user_dto: UserCreateSchema) -> User:
        user = await self.__user_repository.create(user_dto)
        await self.__settings_repository.create(SettingsCreateSchema(user_id=user.user_id))
        return await self.get_user(user.user_id)
    
    async def change_user_settings(self, user_id: int, settings_dto: SettingsCreateSchema) -> bool:
        return await self.__settings_repository.update(user_id, settings_dto)

    async def get_user(self, user_id: int) -> Optional[User]:
        return await self.__user_repository.get(user_id)

    async def update_user(self, user_id: int, dto: UserUpdateSchema) -> bool:
        return await self.__user_repository.update(user_id, dto)

    async def delete_user(self, user_id: int) -> bool:
        return await self.__user_repository.delete(user_id)

    async def list_users(self) -> List[User]:
        return await self.__user_repository.all()

    async def increase_balance(self, user_id: int, amount: int) -> bool:
        user = await self.get_user(user_id)

        if not user:
            return False

        new_balance = (user.balance or 0) + amount
        update_dto = UserUpdateSchema(balance=new_balance)

        return await self.update_user(user_id, update_dto)

    async def decrease_balance(self, user_id: int, amount: int) -> bool:
        user = await self.get_user(user_id)

        if not user or (user.balance or 0) < amount:
            return False

        new_balance = user.balance - amount
        update_dto = UserUpdateSchema(balance=new_balance)

        return await self.update_user(user_id, update_dto)

    async def get_all_users_by_notify(self, notify: bool) -> List[User]:
        users = await self.list_users()
        return [user for user in users if user.notify == notify]
