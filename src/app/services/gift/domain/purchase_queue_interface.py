from abc import ABC, abstractmethod
from app.repositories.models.user import User
from aiogram.types import Gift


class IPurchaseQueue(ABC):
    """Interface for purchase queues (FIFO, LIFO, etc.)"""

    @abstractmethod
    def add(self, user: User, gifts: list[Gift]) -> None:
        """Add user to queue"""
        raise NotImplementedError

    @abstractmethod
    def remove(self) -> None:
        """Remove user from queue"""
        raise NotImplementedError

    @abstractmethod
    def get_next(self) -> User | None:
        """Get next user (depends on queue logic: FIFO/LIFO)"""
        raise NotImplementedError

    @abstractmethod
    def process_next(self) -> None:
        """Process next user (buy and remove)"""
        raise NotImplementedError
