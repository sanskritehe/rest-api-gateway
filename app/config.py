from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DB_SERVICE_URL: str = "http://localhost:8001"


settings = Settings()
