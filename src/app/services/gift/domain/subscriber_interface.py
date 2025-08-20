from abc import ABC, abstractmethod
from aiogram.types import Gift


class ISubscriber(ABC):
    @abstractmethod
    def notify(self, gifts: list[Gift]) -> None:
        """Notify subscriber about new gift"""
        raise NotImplementedError
    
    @abstractmethod
    def buy(self) -> bool:
        """Process the purchase of the gift"""
        raise NotImplementedError
