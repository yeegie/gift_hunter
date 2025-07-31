__all__ = ["SettingsService"]

from typing import Optional
from app.repositories.settings.repository import SettingsRepository
from app.repositories.schemas.settings import (
    SettingsSchema,
    SettingsUpdateSchema,
    SettingsCreateSchema,
)


class SettingsService:
    def __init__(self, repository: SettingsRepository):
        self.__repository = repository

    def create_settings(self, dto: SettingsCreateSchema) -> SettingsSchema:
        return self.__repository.create(dto)
    
    def get_settings(self, user_id: int) -> Optional[SettingsSchema]:
        return self.__repository.get(user_id)
    
    def update_settings(self, user_id: int, dto: SettingsUpdateSchema) -> bool:
        return self.__repository.update(user_id, dto)
    
    def delete_settings(self, user_id: int) -> bool:
        return self.__repository.delete(user_id)
