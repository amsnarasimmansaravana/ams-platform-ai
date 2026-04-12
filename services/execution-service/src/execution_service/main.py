"""Execution engine microservice (runs, workers — extend here)."""

from functools import lru_cache

from ams_common.config import ServiceSettings
from ams_common.service_app import create_domain_service_app


@lru_cache
def get_settings() -> ServiceSettings:
    return ServiceSettings(service_name="execution-service")


app = create_domain_service_app(
    title="AMS Execution Service",
    resource="executions",
    settings_factory=get_settings,
)
