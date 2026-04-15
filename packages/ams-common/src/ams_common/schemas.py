"""Shared Pydantic schemas for common patterns across services."""

from datetime import datetime
from typing import Generic, TypeVar
from uuid import UUID

from pydantic import BaseModel, Field

T = TypeVar("T")


class BaseSchema(BaseModel):
    """Base schema with common fields."""
    class Config:
        from_attributes = True
        json_encoders = {UUID: str, datetime: str}


class PaginationParams(BaseModel):
    """Pagination parameters."""
    skip: int = Field(default=0, ge=0, description="Number of items to skip")
    limit: int = Field(default=20, ge=1, le=100, description="Number of items to return")


class PaginatedResponse(BaseModel, Generic[T]):
    """Generic paginated response wrapper."""
    items: list[T]
    total: int
    skip: int
    limit: int


class HealthResponse(BaseModel):
    """Health check response."""
    status: str = "ok"
    service: str
    environment: str | None = None


class ErrorResponse(BaseModel):
    """Standard error response."""
    detail: str
    error_code: str | None = None
    request_id: str | None = None
