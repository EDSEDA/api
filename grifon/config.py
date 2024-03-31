import logging

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    VIDEO_ANALYSIS_TOPIC: str = "video_analysis"
    RECOMMENDATION_TOPIC: str = "recommendation"

    KAFKA_CLIENT_PORT: int = 9092

    LogLevel: int = logging.INFO
    LogFormat: str = "%(asctime)s - %(levelname)s - [%(funcName)s] - %(message)s"

    DB_HOST: str = 'localhost'
    DB_PORT: int = 5432
    DB_DATABASE: str = 'postgres'
    DB_USER: str = 'postgres'
    DB_PASSWORD: str = 'mysecretpassword'
    DB_DIALECT: str = 'postgresql+psycopg'

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
logging.basicConfig(level=settings.LogLevel, format=settings.LogFormat)

