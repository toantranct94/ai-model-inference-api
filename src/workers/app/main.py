import asyncio
import logging
import pickle

from ai import ModelFactory
from aio_pika import IncomingMessage, Message
from services import rabbitmq_client, redis_client

logging.basicConfig(level=logging.INFO)
model = ModelFactory.create_model()
MAX_RETRY = 5


async def main():
    await rabbitmq_client.connect()
    queue = await rabbitmq_client.channel.declare_queue(
        "pgdb", arguments={
            'x-message-ttl' : 5000,
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
        retry_count = message.headers.get('x-retry-count', 0)
        retry_count += 1

        if retry_count > MAX_RETRY:
            logging.info(
                f"Message {request_id} has reached the maximum retry count.")
            return

        message.headers['x-retry-count'] = retry_count
        await rabbitmq_client.publish_message(
            Message(
                body=message.body,
                headers=message.headers,
                delivery_mode=message.delivery_mode,
            ),
            routing_key='dlq'
        )


if __name__ == "__main__":
    logging.info("Start consuming messages")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
