"""API Gateway: single public HTTP entry, forwards to domain microservices by path prefix."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import RequestResponseEndpoint
from starlette.responses import JSONResponse, Response

from ams_common.logging import configure_logging, get_logger
from ams_common.middleware import RequestIdMiddleware
from gateway_service.auth import AuthMiddleware
from gateway_service.proxy import forward_request
from gateway_service.rate_limit import RateLimitMiddleware
from gateway_service.settings import GatewaySettings, get_gateway_settings
from gateway_service.validation import RequestValidationMiddleware

_LOG = get_logger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    settings = get_gateway_settings()
    configure_logging(settings)
    app.state.http_client = httpx.AsyncClient(timeout=httpx.Timeout(60.0))
    _LOG.info("gateway_startup", service=settings.service_name)
    yield
    await app.state.http_client.aclose()
    _LOG.info("gateway_shutdown")


def create_app() -> FastAPI:
    settings = get_gateway_settings()
    app = FastAPI(
        title="AMS-AI API Gateway",
        version="0.1.0",
        description="Routes /api/v1/{agents|orchestrations|tools|executions} to domain services",
        lifespan=lifespan,
        docs_url="/docs" if not settings.is_production else None,
        redoc_url="/redoc" if not settings.is_production else None,
    )

    # Middleware stack (order matters - innermost first)
    app.add_middleware(RequestIdMiddleware)
    app.add_middleware(RequestValidationMiddleware)
    app.add_middleware(RateLimitMiddleware, requests_per_minute=100)
    app.add_middleware(AuthMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health/live", tags=["health"])
    async def live() -> dict[str, str]:
        return {"status": "ok", "component": "gateway"}

    @app.get("/health/ready", tags=["health"])
    async def ready() -> dict[str, str]:
        return {"status": "ok", "component": "gateway"}

    @app.get("/", tags=["meta"])
    async def root() -> dict[str, object]:
        return {
            "service": "ams-gateway",
            "version": "0.1.0",
            "docs": "/docs",
            "routes": "/api/v1/{agents|orchestrations|tools|executions}",
            "upstream_services": {
                "agents": settings.agent_service_url,
                "orchestrations": settings.orchestration_service_url,
                "tools": settings.tool_service_url,
                "executions": settings.execution_service_url,
            },
        }

    @app.middleware("http")
    async def proxy_middleware(
        request: Request, call_next: RequestResponseEndpoint
    ) -> Response:
        path = request.url.path

        # Pass through health and docs endpoints
        if path in ("/",) or path.startswith("/health") or path.startswith("/docs"):
            return await call_next(request)
        if path.startswith("/openapi.json") or path.startswith("/redoc"):
            return await call_next(request)

        cfg: GatewaySettings = get_gateway_settings()
        client: httpx.AsyncClient = request.app.state.http_client

        # Route to appropriate service
        if path.startswith("/api/v1/agents"):
            return await forward_request(request, cfg.agent_service_url, client)
        if path.startswith("/api/v1/orchestrations"):
            return await forward_request(request, cfg.orchestration_service_url, client)
        if path.startswith("/api/v1/tools"):
            return await forward_request(request, cfg.tool_service_url, client)
        if path.startswith("/api/v1/executions"):
            return await forward_request(request, cfg.execution_service_url, client)

        return JSONResponse(
            status_code=404, content={"detail": "Not Found", "path": path}
        )

    return app


app = create_app()
