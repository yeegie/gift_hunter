import json
import pika
from app.repositories.models.user import User
from ..infrastructure.buyer import Buyer
from aiogram.types import Gift


class PurchaseQueueRabbit:
    def __init__(
        self,
        buyer: Buyer,
        queue_name: str = "purchase_queue",
    ):
        self.__buyer = buyer
        self._queue_name = queue_name

        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters('localhost')
        )

        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self._queue_name, durable=True)

    def add(self, user: User, gifts: list[Gift]) -> None:
        body = json.dumps({
            "user": user.to_schema().model_dump(),
            "gifts": [gift.to_schema().model_dump() for gift in gifts]
        })
        self._channel.basic_publish(
            exchange='',
            routing_key=self._queue_name,
            body=body,
            properties=pika.BasicProperties(delivery_mode=2)
        )

    def start_processing(self):
        def callback(ch, method, properties, body):
            data = json.loads(body.decode())
            user = User(**data)
            try:
                self._buyer.buy(user)
                ch.basic_ack(delivery_tag=method.delivery_tag)
            except Exception as e:
                ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

        self._channel.basic_consume(
            queue=self._queue_name, on_message_callback=callback
        )
        self._channel.start_consuming()
