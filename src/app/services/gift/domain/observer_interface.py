from abc import ABC, abstractmethod
from .subscriber_interface import ISubscriber


class IObserver(ABC):
    @abstractmethod
    async def initialize(self) -> None:
        """Initialization of subscribers when the application starts"""
        raise NotImplementedError

    @abstractmethod
    async def restore_subscribers(self) -> dict[int, ISubscriber]:
        """Fills the list with subscribers (those who have auto-purchase enabled in the database entry). Used only once - when the application is launched, when the list is empty and needs to be restored"""
        raise NotImplementedError
