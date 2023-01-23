import os

from pydantic import BaseSettings
from sqlalchemy.engine.url import URL
from starlette.config import Config


class Settings(BaseSettings):
    """Config class reads settings from env"""

    config = Config()

    DB_HOST: str = os.environ.get("DB_HOST")
    DB_PASSWORD: str = os.environ.get("DB_PASSWORD")
    DB_PORT: int = os.environ.get("DB_PORT")
    DB_NAME: str = os.environ.get("DB_NAME")
    DB_USER: str = os.environ.get("DB_USER")
    API_VERSION: str = "v1"
    BASE_SHORT_URL = os.environ.get("BASE_SHORT_URL", "https://itlab.com")
    BASE_URL: str = f"/api/{API_VERSION}"
    CORS_ORIGINS: str = "localhost"
    SWAGGER_URL: str = f"{BASE_URL}/docs"
    REDOC_URL: str = f"{BASE_URL}/redocs"
    TESTING = config("TESTING", cast=bool, default=False)
    DATABASE_URL = config(
        "DATABASE_URL",
        cast=str,
        default=URL(
            drivername="asyncpg",
            username=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
            database=DB_NAME,
        ),
    )


settings = Settings()
