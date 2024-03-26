import asyncio
import logging
import pickle

from ai import ModelFactory
from aio_pika import IncomingMessage, Message
from services import rabbitmq_client, redis_client

logging.basicConfig(level=logging.INFO)
model = ModelFactory.create_model()


async def main():
    await rabbitmq_client.connect()
    queue = await rabbitmq_client.channel.declare_queue(
        "pgdb", arguments={
            'x-message-ttl' : 1000,
            'x-dead-letter-exchange': 'dlx',
            'x-dead-letter-routing-key': 'dlq'
        })
    await queue.consume(on_message)
    await queue.bind(exchange='amq.direct', routing_key='pgdb')


async def on_message(message: IncomingMessage):
    logging.info(f"Received message: {message}")

    request_id = message.headers.get("request_id", "")

    if not request_id:
        return

    image = pickle.loads(message.body)
    x = model.preprocess_image(image)
    try:
        label = model.forward(x)
        logging.info(f"Inference result: {label}")
        redis_client.set(request_id, label)
        await message.ack()
    except Exception as e:
        logging.error(f"Error in model forward: {e}")
        # Send the message to the DLX
        await rabbitmq_client.publish_message(
            Message(
                body=message.body,
                headers=message.headers,
                delivery_mode=message.delivery_mode,
                expiration=10000
            ),
            routing_key='dlq'
        )


if __name__ == "__main__":
    logging.info("Start consuming messages")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
