from functools import lru_cache
from typing import Dict
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    user_ids: str = ""
    bot_token: str = ""
    openai_api_key: str = ""

    user_timezone: Dict[str, str] = {}
    sessions: Dict[str, str] = {}

    class Config:
        env_file = ".env"
        extra = "ignore"


settings = Settings()


@lru_cache
def get_settings():
    return settings
