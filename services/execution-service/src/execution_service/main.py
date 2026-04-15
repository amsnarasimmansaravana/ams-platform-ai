"""Execution engine microservice (runs, workers — extend here)."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from functools import lru_cache

from fastapi import FastAPI

from ams_common.config import ServiceSettings
from ams_common.db import Base, get_async_engine
from ams_common.logging import configure_logging, get_logger
from ams_common.middleware import RequestIdMiddleware

from execution_service.routes import router

_LOG = get_logger(__name__)


@lru_cache
def get_settings() -> ServiceSettings:
    return ServiceSettings(service_name="execution-service")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Startup and shutdown lifecycle."""
    settings = get_settings()
    configure_logging(settings)

    # Connect to database
    engine = get_async_engine(settings)
    async with engine.begin() as conn:
        _LOG.info("database_connected", db_url=settings.db_url)

    _LOG.info("service_startup", service=settings.service_name)
    yield
    _LOG.info("service_shutdown", service=settings.service_name)


app = FastAPI(
    title="AMS Execution Service",
    version="0.1.0",
    description="Execution engine and workflow runner microservice",
    lifespan=lifespan,
)

app.add_middleware(RequestIdMiddleware)
app.include_router(router)


@app.get("/health/live", tags=["health"])
async def live() -> dict[str, str]:
    return {"status": "ok", "service": get_settings().service_name}


@app.get("/health/ready", tags=["health"])
async def ready() -> dict[str, str]:
    s = get_settings()
    return {"status": "ok", "service": s.service_name, "environment": s.environment}
