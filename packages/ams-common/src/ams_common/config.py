"""Base settings for all microservices (env prefix AMS_)."""

from typing import Literal

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ServiceSettings(BaseSettings):
    """12-factor settings shared by gateway and domain services."""

    model_config = SettingsConfigDict(
        env_prefix="AMS_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    service_name: str = "ams-service"
    environment: Literal["development", "staging", "production"] = "development"
    debug: bool = False
    log_level: str = "INFO"
    log_json: bool = Field(
        default=False,
        description="JSON logs (recommended in containers)",
    )
    api_prefix: str = "/api/v1"

    @property
    def is_production(self) -> bool:
        return self.environment == "production"
