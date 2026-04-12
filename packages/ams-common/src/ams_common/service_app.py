"""Minimal FastAPI app factory for domain microservices (health + one list stub)."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Callable

from fastapi import FastAPI

from ams_common.config import ServiceSettings
from ams_common.logging import configure_logging, get_logger
from ams_common.middleware import RequestIdMiddleware


def create_domain_service_app(
    *,
    title: str,
    resource: str,
    version: str = "0.1.0",
    settings_factory: Callable[[], ServiceSettings],
) -> FastAPI:
    """Build a small service exposing ``GET /api/v1/{resource}`` and health probes."""

    _log = get_logger(__name__)

    @asynccontextmanager
    async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
        s = settings_factory()
        configure_logging(s)
        _log.info("service_startup", service=s.service_name)
        yield
        _log.info("service_shutdown", service=s.service_name)

    app = FastAPI(title=title, version=version, lifespan=lifespan)
    app.add_middleware(RequestIdMiddleware)
    prefix = "/api/v1"

    @app.get("/health/live", tags=["health"])
    async def live() -> dict[str, str]:
        return {"status": "ok", "service": settings_factory().service_name}

    @app.get("/health/ready", tags=["health"])
    async def ready() -> dict[str, str]:
        s = settings_factory()
        return {"status": "ok", "service": s.service_name, "environment": s.environment}

    @app.get(f"{prefix}/{resource}", tags=[resource])
    async def list_stub() -> dict[str, object]:
        s = settings_factory()
        return {"service": s.service_name, "resource": resource, "items": []}

    return app
