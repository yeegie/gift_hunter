__all__ = ["UserRepository"]

from .UserRepository import UserRepository

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import selectinload

from app.repositories.models import User
from app.repositories.schemas.user import (
    UserCreateSchema,
    UserUpdateSchema
)

from typing import Optional, List

from logging import Logger


class UserRepository(UserRepository):
    def __init__(self, session: AsyncSession, logger: Logger) -> None:
        self.__session = session
        self.__logger = logger

    async def __commit_and_refresh(self, instance: User) -> None:
        await self.__session.commit()
        await self.__session.refresh(instance)

    async def create(self, dto: UserCreateSchema) -> User:
        user = User(
            user_id=dto.user_id,
            fullname=dto.fullname,
            username=dto.username
        )
        self.__session.add(user)
        await self.__commit_and_refresh(user)
        
        self.__logger.info(f"- [USER] user_id={user.user_id} CREATED")
        return user

    async def get(self, user_id: int) -> Optional[User]:
        result = await self.__session.execute(
            select(User)
            .options(selectinload(User.settings))
            .where(User.user_id == user_id)
        )
        return result.scalar_one_or_none()

    async def update(self, user_id: int, dto: UserUpdateSchema) -> bool:
        user = await self.get(user_id)

        if not user:
            return False

        # Update only not-none fields
        for field, value in dto.model_dump(exclude_unset=True).items():
            setattr(user, field, value)

        try:
            await self.__commit_and_refresh(user)
            self.__logger.info(f"- [USER] user_id={user_id} UPDATED")
            return True
        except SQLAlchemyError as ex:
            self.__logger.error(f"- [USER] UPDATE ERROR: {ex}")
            await self.__session.rollback()
            return False

    async def delete(self, user_id: int) -> bool:
        try:
            result = await self.__session.execute(
                delete(User).where(User.id == id)
            )
            await self.__session.commit()
            return result.rowcount > 0  # Return True if deleted
        except SQLAlchemyError as ex:
            self.__logger.error(f"- [USER] DELETION ERROR: {ex}")
            await self.__session.rollback()
            return False

    async def all(self) -> List[User]:
        try:
            result = await self.__session.execute(select(User))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            self.__logger.error(f"[USER] FETCH ALL ERROR: {ex}")
            return []
    
    async def update_settings(self, user_id: int, dto: UserUpdateSchema) -> bool:
        user = self.read(user_id)

        if user is None:
            return False
        
        
        return True
    
    async def change_balance(self, user_id: int, amount: int) -> bool:
        """
        Надёжно изменить баланс пользователя:
        - Поддерживает положительное и отрицательное значение amount.
        - Блокирует строку в БД для защиты от race conditions.
        - Защищает от отрицательного баланса.

        :param user_id: ID пользователя
        :param amount: Сумма для изменения (может быть < 0)
        :return: True, если баланс успешно изменён
        """
        if amount == 0:
            return True

        try:
            result = await self.__session.execute(
                select(User).where(User.user_id == user_id).with_for_update()
            )
            user = result.scalar()

            if not user:
                self.__logger.warning(
                    f"- [USER] User not found for balance change: {user_id}")
                return False

            new_balance = user.balance + amount
            if new_balance < 0:
                self.__logger.warning(
                    f"- [USER] Negative balance rejected: user_id={user_id}, attempted={new_balance}")
                return False

            user.balance = new_balance
            await self.__commit_and_refresh(user)
            self.__logger.info(
                f"- [USER] user_id={user_id} BALANCE CHANGED BY {amount} → {new_balance}")
            return True

        except SQLAlchemyError as ex:
            await self.__session.rollback()
            self.__logger.error(f"- [USER] BALANCE CHANGE ERROR: {ex}")
            return False
