import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL") or "postgresql://root:root@postgres:5432/blockhouse"
    redis_url: str = os.getenv("REDIS_URL") or "redis://redis:6379/0"
    kafka_bootstrap_servers: str = os.getenv("KAFKA_BOOTSTRAP_SERVERS") or "kafka:9092"
    provider: str = os.getenv("PROVIDER") or "yfinance"

    class Config:
        env_file = os.getenv("DOTENV_PATH", ".env")
        env_file_encoding = "utf-8"

settings = Settings()
