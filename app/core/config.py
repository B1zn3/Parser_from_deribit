from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "deribit_db"
    postgres_host: str = "db" 
    postgres_port: int = 5432
    db_echo: bool = False

    deribit_base_url: str = "https://test.deribit.com/"
    deribit_timeout_seconds: int = 10

    celery_broker_url: str = "redis:/redis/localhost:6379/0" 

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()