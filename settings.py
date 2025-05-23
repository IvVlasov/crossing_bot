from functools import lru_cache

from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BOT_TOKEN: str
    DB_PATH: str = "database.db"
    ADMIN_CHAT_ID: int = 0
    SETTINGS_FILE_PATH: str = "settings.xlsx"
    CHANNEL_ID: int
    MANAGER_CHAT_ID: int

    LATITUDE: float = 66.52
    LONGITUDE: float = 66.61

    WIND_SPEED_LIMIT: float = 17  # in m/s
    VISIBILITY_LIMIT: float = 1000  # in meters

    model_config = SettingsConfigDict(env_file=".env")

    @field_validator("ADMIN_CHAT_ID", mode="before")
    @classmethod
    def validate_admin_chat_ids(cls, value) -> int:
        if isinstance(value, int):
            return value
        return int(value)


@lru_cache()
def get_settings():
    return Settings()
