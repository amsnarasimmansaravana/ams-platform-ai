"""Request validation middleware."""

from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class RequestValidationMiddleware(BaseHTTPMiddleware):
    """Validate incoming requests (content-type, payload size, etc.)."""

    # Maximum payload size in bytes (10 MB)
    MAX_PAYLOAD_SIZE = 10 * 1024 * 1024

    # Non-GET methods that require JSON
    JSON_REQUIRED_METHODS = {"POST", "PUT", "PATCH"}

    EXCLUDED_PATHS = {"/", "/docs", "/redoc", "/openapi.json", "/health/live", "/health/ready"}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Validate incoming requests."""
        # Skip validation for excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        # Check Content-Length for payload size
        content_length = request.headers.get("Content-Length")
        if content_length:
            try:
                size = int(content_length)
                if size > self.MAX_PAYLOAD_SIZE:
                    _LOG.warning("payload_too_large", path=request.url.path, size=size)
                    raise HTTPException(
                        status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                        detail=f"Payload too large (max {self.MAX_PAYLOAD_SIZE} bytes)",
                    )
            except ValueError:
                pass

        # Validate content-type for POST/PUT/PATCH
        if request.method in self.JSON_REQUIRED_METHODS:
            content_type = request.headers.get("Content-Type", "")
            if request.method in self.JSON_REQUIRED_METHODS and not content_type.startswith(
                "application/json"
            ):
                _LOG.warning(
                    "invalid_content_type",
                    path=request.url.path,
                    method=request.method,
                    content_type=content_type,
                )
                raise HTTPException(
                    status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
                    detail="Content-Type must be application/json",
                )

        response = await call_next(request)
        return response
