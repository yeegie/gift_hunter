__all__ = ["SettingsRepository"]

from ..CrudRepository import CrudRepository

from app.repositories.models.settings import Settings
from app.repositories.schemas.settings import (
    SettingsCreateSchema,
    SettingsUpdateSchema,
)

from typing import Optional


class SettingsRepository(CrudRepository):
    async def create(self, dto: SettingsCreateSchema) -> Settings:
        raise NotImplementedError

    async def get(self, user_id: int) -> Optional[Settings]:
        raise NotImplementedError

    async def update(self, user_id: int, dto: SettingsUpdateSchema) -> bool:
        raise NotImplementedError

    async def delete(self, user_id: int) -> bool:
        raise NotImplementedError
