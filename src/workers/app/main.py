import asyncio
import logging
import pickle

from ai import InferenceModel
from aio_pika import IncomingMessage
from services import rabbitmq_client, redis_client

logging.basicConfig(level=logging.INFO)
model = InferenceModel()


async def main():
    await rabbitmq_client.connect()
    queue = await rabbitmq_client.channel.declare_queue("pgdb")
    await queue.consume(on_message)


async def on_message(message: IncomingMessage):
    logging.info(f"Received message: {message}")

    request_id = message.headers.get("request_id", "")

    if not request_id:
        return

    image = pickle.loads(message.body)
    x = InferenceModel.preprocess_image(image)
    label = model(x)
    logging.info(f"Inference result: {label}")

    redis_client.set(request_id, label)
    await message.ack()


if __name__ == "__main__":
    logging.info("Start consuming messages")
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
