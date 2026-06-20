from pydantic_settings import BaseSettings
from pydantic import HttpUrl


class Settings(BaseSettings):
    DB_SERVICE_URL: HttpUrl = "http://localhost:8001"


settings = Settings()
