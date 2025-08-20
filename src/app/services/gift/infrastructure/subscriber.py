from ..domain.subscriber_interface import ISubscriber
from ..infrastructure.purchase_queue import PurchaseQueueRabbit
from app.repositories.models.user import User
from aiogram.types import Gift


class Subscriber(ISubscriber):
    def __init__(
        self,
        user: User,
        purchase_queue: PurchaseQueueRabbit,
    ) -> None:
        self.user = user
        self.purchase_queue = purchase_queue

    def notify(self, gifts: list[Gift]) -> None:
        self.purchase_queue.add(self.user, gifts)
