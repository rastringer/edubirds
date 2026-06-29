from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    DEBUG: bool = False
    MAX_TEXT_SIZE_KB: int = 500 # small payloads
    CACHE_MAX_AGE: int = 3600
    ALLOWED_ORIGINS: list = ["*"] # to alter later

    @field_validator("DEBUG", mode="before")
    @classmethod
    def parse_debug(cls, value):
        if isinstance(value, str):
            value = value.strip().lower()
            if value in {"release", "production", "prod"}:
                return False
            if value in {"debug", "development", "dev"}:
                return True
        return value

settings = Settings() 
