from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):

    ZOOKEEPER_CLIENT_PORT: int = 2181
    KAFKA_CLIENT_PORT: int = 29092

    LogLevel: int = logging.INFO

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
logging.basicConfig(level=logging.INFO)

CLIENT_AVATAR_PATH = 'resources/clients'
