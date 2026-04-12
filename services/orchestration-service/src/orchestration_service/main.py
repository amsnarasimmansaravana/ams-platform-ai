"""Orchestration / workflow microservice."""

from functools import lru_cache

from ams_common.config import ServiceSettings
from ams_common.service_app import create_domain_service_app


@lru_cache
def get_settings() -> ServiceSettings:
    return ServiceSettings(service_name="orchestration-service")


app = create_domain_service_app(
    title="AMS Orchestration Service",
    resource="orchestrations",
    settings_factory=get_settings,
)
