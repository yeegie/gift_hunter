__all__ = ["SettingsRepository"]

from sqlalchemy import select, delete
from sqlalchemy.exc import SQLAlchemyError

from .SettingsRepository import SettingsRepository as BaseSettingsRepository
from logging import Logger
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.repositories.schemas.settings import (
    SettingsCreateSchema,
    SettingsUpdateSchema,
)

from app.repositories.models.settings import Settings


class SettingsRepository(BaseSettingsRepository):
    def __init__(self, session: AsyncSession, logger: Logger) -> None:
        self.__session = session
        self.__logger = logger

    async def __commit_and_refresh(self, instance: Settings) -> None:
        try:
            await self.__session.commit()
            await self.__session.refresh(instance)
        except SQLAlchemyError as ex:
            await self.__session.rollback()
            self.__logger.error(f"[SETTINGS] Commit and refresh error: {ex}")
            raise

    async def create(self, dto: SettingsCreateSchema) -> Settings:
        settings = Settings(
            user_id=dto.user_id,
            auto_buy=dto.auto_buy,
            price_min=dto.price_min,
            price_max=dto.price_max,
            supply_limit=dto.supply_limit,
            cycles=dto.cycles,
            quantity=dto.quantity
        )
        self.__session.add(settings)
        await self.__commit_and_refresh(settings)
        return settings

    async def get(self, user_id: int) -> Optional[Settings]:
        result = await self.__session.execute(
            select(Settings)
            .where(Settings.user_id == user_id)
        )
        return result.scalar_one_or_none()
        

    async def update(self, user_id: int, dto: SettingsUpdateSchema) -> bool:
        settings = await self.get(user_id)

        if not settings:
            return False

        # Update only not-none fields
        for field, value in dto.model_dump(exclude_unset=True).items():
            self.__logger.debug(f"{settings}, field: {field}={value}")
            setattr(settings, field, value)

        try:
            await self.__commit_and_refresh(settings)
            self.__logger.info(f"[SETTINGS] user_id={user_id} UPDATED")
            return True
        except SQLAlchemyError as ex:
            self.__logger.error(f"[SETTINGS] UPDATE ERROR: {ex}")
            await self.__session.rollback()
            return False

    async def delete(self, user_id: int) -> bool:
        try:
            result = await self.__session.execute(select(Settings).where(Settings.user_id == user_id))
            settings = result.scalar_one_or_none()
            if not settings:
                return False
            await self.__session.delete(settings)
            await self.__session.commit()
            self.__logger.info(f"[SETTINGS] user_id={user_id} DELETED")
            return True
        except SQLAlchemyError as ex:
            self.__logger.error(f"[SETTINGS] DELETE ERROR: {ex}")
            await self.__session.rollback()
            return False

    async def all(self) -> List[Settings]:
        try:
            result = await self.__session.execute(select(Settings))
            return result.scalars().all()
        except SQLAlchemyError as ex:
            self.__logger.error(f"[SETTINGS] FETCH ALL ERROR: {ex}")
            return []
