from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    db_url: str = "postgresql+psycopg2://root:root@localhost:5432/blockhouse"
    kafka_bootstrap_servers: str = "localhost:9092"
    provider: str = "yahoo_finance"
    
    class Config:
        env_file = ".env"

settings = Settings()
