from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent


class Settings(BaseSettings):
    # DB
    django_database_user: str
    django_database_password: str
    django_database_db_name: str = "mydb"
    django_database_host: str = "localhost"
    django_database_port: str = "5432"

    model_config = SettingsConfigDict(
        env_file=BASE_DIR / ".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
