"""Shared configuration, logging, and HTTP middleware for AMS-AI services."""

__version__ = "0.1.0"

from ams_common.celery_app import get_celery_app
from ams_common.config import ServiceSettings
from ams_common.db import Base, get_async_session, get_async_session_factory, get_sync_session_factory
from ams_common.models import (
    Agent,
    AgentStatus,
    AuditLog,
    Execution,
    ExecutionLog,
    ExecutionPhase,
    ExecutionStatus,
    Orchestration,
    OrchestrationStatus,
    Tool,
    ToolCategory,
)
from ams_common.schemas import BaseSchema, ErrorResponse, HealthResponse, PaginatedResponse, PaginationParams

__all__ = [
    "ServiceSettings",
    "Base",
    "get_async_session",
    "get_async_session_factory",
    "get_sync_session_factory",
    "get_celery_app",
    # Models
    "Agent",
    "AgentStatus",
    "Tool",
    "ToolCategory",
    "Orchestration",
    "OrchestrationStatus",
    "Execution",
    "ExecutionStatus",
    "ExecutionPhase",
    "ExecutionLog",
    "AuditLog",
    # Schemas
    "BaseSchema",
    "PaginationParams",
    "PaginatedResponse",
    "HealthResponse",
    "ErrorResponse",
]
