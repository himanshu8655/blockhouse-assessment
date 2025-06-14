from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    redis_url: str = "redis://localhost:6379/0"
    db_url: str = "postgresql+psycopg2://root:root@localhost:5432/blockhouse"
    class Config:
        env_file = ".env"

settings = Settings()
