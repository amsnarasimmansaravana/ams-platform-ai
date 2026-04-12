"""Agent Registry microservice (A2A, CRUD — extend here)."""

from functools import lru_cache

from ams_common.config import ServiceSettings
from ams_common.service_app import create_domain_service_app


@lru_cache
def get_settings() -> ServiceSettings:
    return ServiceSettings(service_name="agent-service")


app = create_domain_service_app(
    title="AMS Agent Registry Service",
    resource="agents",
    settings_factory=get_settings,
)
