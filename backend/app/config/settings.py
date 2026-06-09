from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "NeuroTutor"
    app_env: str = "local"
    database_url: str = "sqlite:///./neurotutor.db"
    openai_api_key: str | None = None
    groq_api_key: str | None = None
    jwt_secret: str = Field(default="local-dev-secret", min_length=8)
    frontend_origin: str = "http://localhost:3000"
    fast_model: str = "llama3-8b-8192"
    reasoning_model: str = "gpt-4o"
    request_timeout_seconds: int = 30

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()
