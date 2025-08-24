# Standard library imports
from functools import lru_cache
import json
from typing import Any

# Third-party imports
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )


    DATABASE_URL: str
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    ENV: str
    DEBUG: bool


    API_V1_PREFIX: str = "/api/v1"
    CORS_ORIGINS: list[str] = ["*"]
    ALLOW_HOSTS: list[str] = ["*"]
    DOCS_ENABLED: bool = True
    GZIP_ENABLED: bool = True

    @field_validator("CORS_ORIGINS", "ALLOW_HOSTS", mode="before")
    @classmethod
    def parse_list_env(cls, values: Any) -> Any:
        if isinstance(values, list):
            return [str(item).strip() for item in values]

        if isinstance(values, str):
            clean_value = values.strip()

            if not clean_value or clean_value.lower() in {"[]", "none", "null"}:
                return []

            if clean_value.startswith("[") and clean_value.endswith("]"):
                try:
                    parsed = json.loads(clean_value)
                    if isinstance(parsed, list):
                        return [str(item).strip() for item in parsed]
                except Exception:
                    pass
            return [item.strip() for item in clean_value.split(",") if item.strip()]

        return values


@lru_cache
def get_settings() -> Settings:
    return Settings()
