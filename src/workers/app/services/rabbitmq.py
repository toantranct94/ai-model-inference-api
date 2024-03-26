import asyncio
import logging
import os
from typing import Callable

from aio_pika import Message, connect, ExchangeType
from aiormq import AMQPConnectionError
from cores import singleton

logging.basicConfig(level=logging.INFO)


@singleton
class RabbitMQClient():
    def __init__(self):
        self.amqp_url = os.getenv("AMQP_URL", "amqp://guest:guest@localhost/")
        self.connection = None
        self.channel = None
        self.retry_attempts = 10
        self.retry_delay = 5

    async def connect(self):
        for attempt in range(self.retry_attempts):
            try:
                self.connection = await connect(self.amqp_url)
                self.channel = await self.connection.channel()
                self.dlx = await self.channel.declare_exchange(
                    'dlx', ExchangeType.DIRECT)
                self.dlq = await self.channel.declare_queue(
                    'dlq', arguments={
                        'x-message-ttl': 5000,
                        'x-dead-letter-exchange': 'amq.direct',
                        'x-dead-letter-routing-key': 'pgdb'
                    })
                await self.dlq.bind(self.dlx, 'dlq')
                logging.info("Connected to RabbitMQ")
                break
            except AMQPConnectionError:
                logging.error(
                    (f"Connection attempt {attempt + 1} failed."
                        f"Retrying in {self.retry_delay} seconds..."))
                self.retry_delay *= 2
                await asyncio.sleep(self.retry_delay)

    async def close(self):
        await self.connection.close()
        logging.info("Disconnected from RabbitMQ")

    async def publish_message(self, message: Message, routing_key: str = "pgdb"):
        try:
            await self.channel.default_exchange.publish(
                message,
                routing_key=routing_key
            )
            logging.info(f"Message published to {routing_key}")
        except Exception as e:
            logging.error(f"Failed to publish message: {e}")

    async def consume_messages(self, queue_name: str, callback: Callable):
        try:
            queue = await self.channel.declare_queue(queue_name)
            await queue.consume(callback)
            logging.info(f"Message consumed from {queue_name}")
        except Exception as e:
            logging.error(f"Failed to consume messages: {e}")


rabbitmq_client = RabbitMQClient()
