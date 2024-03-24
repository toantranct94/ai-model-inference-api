from typing import List

from .rabbitmq import RabbitMQSettings
from .redis import RedisSettings


class Settings(RabbitMQSettings, RedisSettings):

    APP_NAME: str
    BACKEND_CORS_ORIGINS: List[str]
    API_PREFIX: str

    description: str = """
        Description
    """

    debug: bool = True

    class Config:
        case_sensitive = True
        env_file = ".env"
