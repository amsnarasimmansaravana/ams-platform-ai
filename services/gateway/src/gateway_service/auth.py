"""Authentication middleware for API Gateway."""

from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from ams_common.logging import get_logger

_LOG = get_logger(__name__)

# Simple bearer token validation (replace with JWT in production)
VALID_API_KEYS = {"demo-key-123", "test-key-456"}


class AuthMiddleware(BaseHTTPMiddleware):
    """Basic API key authentication middleware."""

    EXCLUDED_PATHS = {"/", "/docs", "/redoc", "/openapi.json", "/health/live", "/health/ready"}

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Check authorization on protected routes."""
        # Skip auth for excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        # Extract API key from Authorization header
        auth_header = request.headers.get("Authorization")
        if not auth_header:
            _LOG.warning("missing_auth_header", path=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Missing Authorization header",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Parse bearer token
        parts = auth_header.split()
        if len(parts) != 2 or parts[0].lower() != "bearer":
            _LOG.warning("invalid_auth_format", path=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid Authorization header format",
                headers={"WWW-Authenticate": "Bearer"},
            )

        token = parts[1]

        # Validate token (TODO: implement JWT validation in production)
        if token not in VALID_API_KEYS:
            _LOG.warning("invalid_api_key", path=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid API key",
                headers={"WWW-Authenticate": "Bearer"},
            )

        # Store user info in request state for later use
        request.state.api_key = token
        response = await call_next(request)
        return response
