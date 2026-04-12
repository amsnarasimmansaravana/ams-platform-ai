"""Gateway-only configuration (downstream service URLs)."""

from functools import lru_cache

from pydantic import Field
from ams_common.config import ServiceSettings


class GatewaySettings(ServiceSettings):
    """Env prefix AMS_* (inherited); URLs point to domain services on the Docker network."""

    service_name: str = "gateway"
    cors_origins: list[str] = Field(
        default_factory=lambda: ["http://127.0.0.1:3000", "http://localhost:3000"],
    )

    agent_service_url: str = Field(
        default="http://127.0.0.1:8001",
        description="Base URL for agent-service (no trailing slash)",
    )
    orchestration_service_url: str = Field(
        default="http://127.0.0.1:8002",
    )
    tool_service_url: str = Field(
        default="http://127.0.0.1:8003",
    )
    execution_service_url: str = Field(
        default="http://127.0.0.1:8004",
    )


@lru_cache
def get_gateway_settings() -> GatewaySettings:
    return GatewaySettings()
