from abc import ABC, abstractmethod
from typing import List, Optional


class CrudRepository(ABC):
    @abstractmethod
    async def create(self, dto: any) -> any:
        raise NotImplementedError()

    @abstractmethod
    async def get(self, user_id: int) -> Optional[any]:
        raise NotImplementedError()

    @abstractmethod
    async def update(self, user_id: int, dto: any) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def delete(self, user_id: int) -> bool:
        raise NotImplementedError()

    @abstractmethod
    async def all(self) -> List[any]:
        raise NotImplementedError()
