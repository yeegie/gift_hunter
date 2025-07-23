__all__ = ["UserRepository"]

from app.repositories.CrudRepository import CrudRepository

from abc import ABC, abstractmethod
from typing import Optional, List

from app.repositories.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema


class CrudUserRepository(CrudRepository, ABC):
    @abstractmethod
    async def create(self, dto: UserCreateSchema) -> UserSchema:
        raise NotImplementedError()

    @abstractmethod
    async def read(self, user_id: int) -> Optional[UserSchema]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, user_id: int, dto: UserUpdateSchema) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def all(self) -> List[UserSchema]:
        raise NotImplementedError()
