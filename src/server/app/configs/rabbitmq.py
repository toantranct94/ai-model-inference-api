from pydantic_settings import BaseSettings


class RabbitMQSettings(BaseSettings):

    AMQP_URL: str
