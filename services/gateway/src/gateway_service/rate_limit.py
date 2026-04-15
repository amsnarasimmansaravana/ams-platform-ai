"""Rate limiting middleware for API Gateway."""

from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from fastapi import HTTPException, status
from starlette.middleware.base import BaseHTTPMiddleware, RequestResponseEndpoint
from starlette.requests import Request
from starlette.responses import Response

from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class RateLimiter:
    """Simple in-memory rate limiter (use Redis for distributed systems)."""

    def __init__(self, requests_per_minute: int = 100):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    def is_allowed(self, client_id: str) -> bool:
        """Check if client is within rate limit."""
        now = datetime.utcnow()
        cutoff = now - timedelta(minutes=1)

        # Clean old requests
        self.requests[client_id] = [
            req_time for req_time in self.requests[client_id] if req_time > cutoff
        ]

        # Check limit
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False

        # Add current request
        self.requests[client_id].append(now)
        return True


class RateLimitMiddleware(BaseHTTPMiddleware):
    """Rate limiting middleware using client IP."""

    EXCLUDED_PATHS = {"/", "/docs", "/redoc", "/openapi.json", "/health/live", "/health/ready"}

    def __init__(self, app, requests_per_minute: int = 100):
        super().__init__(app)
        self.limiter = RateLimiter(requests_per_minute)

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        """Apply rate limiting based on client IP."""
        # Skip rate limiting for excluded paths
        if request.url.path in self.EXCLUDED_PATHS:
            return await call_next(request)

        # Get client IP (consider X-Forwarded-For for proxies)
        client_ip = request.client.host if request.client else "unknown"
        forwarded_for = request.headers.get("X-Forwarded-For")
        if forwarded_for:
            client_ip = forwarded_for.split(",")[0].strip()

        # Check rate limit
        if not self.limiter.is_allowed(client_ip):
            _LOG.warning("rate_limit_exceeded", client_ip=client_ip, path=request.url.path)
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail="Rate limit exceeded (100 requests per minute)",
                headers={"Retry-After": "60"},
            )

        response = await call_next(request)
        response.headers["X-RateLimit-Limit"] = "100"
        response.headers["X-RateLimit-Remaining"] = str(99 - len(self.limiter.requests[client_ip]))
        return response
