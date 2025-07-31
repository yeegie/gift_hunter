__all__ = ["UserRepository"]

from app.repositories.CrudRepository import CrudRepository

from abc import ABC, abstractmethod
from typing import Optional, List

from app.repositories.models import User
from app.repositories.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema
)


class UserRepository(CrudRepository, ABC):
    @abstractmethod
    async def create(self, dto: UserCreateSchema) -> User:
        """
        Create a new user in the repository.
        """
        raise NotImplementedError()

    @abstractmethod
    async def get(self, user_id: int) -> Optional[User]:
        """
        Read a user from the repository.
        """
        raise NotImplementedError()

    @abstractmethod
    async def update(self, user_id: int, dto: UserUpdateSchema) -> bool:
        """
        Update a user in the repository.
        """
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        """
        Delete a user from the repository.
        """
        raise NotImplementedError()

    # Other methods
    @abstractmethod
    async def all(self) -> List[User]:
        """
        Get all users from the repository
        """
        raise NotImplementedError()

    @abstractmethod
    async def change_balance(self, user_id: int, amount: int) -> bool:
        """
        Change the balance of a user in the repository.
        """
        raise NotImplementedError()
