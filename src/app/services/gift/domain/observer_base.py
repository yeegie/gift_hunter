from .observer_interface import IObserver
from .subscriber_interface import ISubscriber
from aiogram.types import Gift


class BaseObserver:
    def __init__(self):
        self.__subscribers: dict[int, ISubscriber] = {}

    def add_subscriber(self, subscriber: ISubscriber) -> bool:
        """Add a subscriber who needs to be notified about the arrival of a gift"""
        if subscriber.user_id not in self.__subscribers:
            self.__subscribers[subscriber.user_id] = subscriber
            return True
        return False

    def remove_subscriber(self, user_id: int) -> bool:
        """Remove subscriber"""
        if user_id in self.__subscribers:
            del self.__subscribers[user_id]
            return True
        return False

    def notify_subscribers(self, gifts: list[Gift]) -> None:
        """Notify subscribers"""
        for subscriber in self.__subscribers.values():
            subscriber.notify(gifts)

    @property
    def subscribers_count(self):
        return len(self.__subscribers)
