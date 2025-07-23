__all__ = ["UserService"]

from typing import Optional, List
from app.repositories.user.repository import UserRepository
from app.repositories.schemas.user import (
    UserSchema,
    UserCreateSchema,
    UserUpdateSchema,
    UserSettingsUpdateSchema
)


class UserService:
    def __init__(self, repository: UserRepository):
        self.__repository = repository

    async def create_user(self, dto: UserCreateSchema) -> UserSchema:
        return await self.__repository.create(dto)

    async def get_user(self, user_id: int) -> Optional[UserSchema]:
        return await self.__repository.read(user_id)

    async def update_user(self, user_id: int, dto: UserUpdateSchema) -> bool:
        return await self.__repository.update(user_id, dto)

    async def delete_user(self, user_id: int) -> bool:
        return await self.__repository.delete(user_id)

    async def list_users(self) -> List[UserSchema]:
        return await self.__repository.all()
    
    async def change_settings(self, user_id: int, settings: UserSettingsUpdateSchema) -> bool:
        user = await self.get_user(user_id)

        if not user:
            return False
        
        update_dto = UserUpdateSchema(settings=settings)
        return await self.update_user(user_id, update_dto)

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
