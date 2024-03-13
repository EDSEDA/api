from pydantic_settings import BaseSettings
import logging


class Settings(BaseSettings):
    VIDEO_ANALYSIS_TOPIC: str = "video_analysis"

    ZOOKEEPER_CLIENT_PORT: int = 2181
    KAFKA_CLIENT_PORT: int = 9092

    LogLevel: int = logging.INFO

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
logging.basicConfig(level=logging.INFO)

CLIENT_AVATAR_PATH = 'resources/clients'
