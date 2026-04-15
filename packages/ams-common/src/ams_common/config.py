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

    # Database
    db_url: str = "postgresql+psycopg2://ams:ams@localhost:5432/ams_ai"
    db_echo: bool = False
    db_pool_size: int = 20
    db_max_overflow: int = 10

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Celery
    celery_broker_url: str = Field(default_factory=lambda: None)
    celery_result_backend: str = Field(default_factory=lambda: None)

    @property
    def is_production(self) -> bool:
        return self.environment == "production"

    def __init__(self, **data):
        super().__init__(**data)
        # Default Celery to Redis if not set
        if not self.celery_broker_url:
            self.celery_broker_url = self.redis_url
        if not self.celery_result_backend:
            self.celery_result_backend = self.redis_url
