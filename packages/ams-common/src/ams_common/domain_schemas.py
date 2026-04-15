"""Pydantic schemas for request/response validation and serialization."""

from datetime import datetime
from typing import Any
from uuid import UUID

from pydantic import BaseModel, Field

from ams_common.models import (
    AgentStatus,
    ExecutionPhase,
    ExecutionStatus,
    OrchestrationStatus,
    ToolCategory,
)
from ams_common.schemas import BaseSchema


# --- Agent Schemas ---


class AgentCreate(BaseModel):
    """Create agent request."""
    name: str
    framework: str
    version: str = "1.0.0"
    description: str | None = None
    tags: list[str] = []
    a2a_compliant: bool = False
    capabilities: dict[str, Any] = {}
    config: dict[str, Any] = {}
    namespace: str = "default"


class AgentUpdate(BaseModel):
    """Update agent request."""
    description: str | None = None
    status: AgentStatus | None = None
    tags: list[str] | None = None
    config: dict[str, Any] | None = None


class AgentResponse(BaseSchema):
    """Agent response schema."""
    id: UUID
    name: str
    version: str
    framework: str
    status: AgentStatus
    description: str | None = None
    tags: list[str]
    a2a_compliant: bool
    capabilities: dict[str, Any]
    created_at: datetime
    updated_at: datetime


# --- Tool Schemas ---


class ToolCreate(BaseModel):
    """Create tool request."""
    name: str
    category: ToolCategory
    version: str = "1.0.0"
    description: str | None = None
    input_schema: dict[str, Any] = {}
    output_schema: dict[str, Any] = {}
    config: dict[str, Any] = {}
    auth_type: str | None = None
    auth_config: dict[str, Any] = {}
    health_check_enabled: bool = True
    health_check_url: str | None = None
    rate_limit: int | None = None
    namespace: str = "default"


class ToolUpdate(BaseModel):
    """Update tool request."""
    description: str | None = None
    input_schema: dict[str, Any] | None = None
    output_schema: dict[str, Any] | None = None
    config: dict[str, Any] | None = None
    is_healthy: bool | None = None
    rate_limit: int | None = None


class ToolResponse(BaseSchema):
    """Tool response schema."""
    id: UUID
    name: str
    category: ToolCategory
    version: str
    description: str | None = None
    input_schema: dict[str, Any]
    output_schema: dict[str, Any]
    auth_type: str | None = None
    health_check_enabled: bool
    is_healthy: bool
    created_at: datetime
    updated_at: datetime


# --- Orchestration Schemas ---


class OrchestrationCreate(BaseModel):
    """Create orchestration request."""
    name: str
    version: str = "1.0.0"
    description: str | None = None
    pattern: str  # "sequential", "parallel", "conditional", etc.
    dag: dict[str, Any] = {}
    tags: list[str] = []
    config: dict[str, Any] = {}
    namespace: str = "default"


class OrchestrationUpdate(BaseModel):
    """Update orchestration request."""
    description: str | None = None
    status: OrchestrationStatus | None = None
    dag: dict[str, Any] | None = None
    tags: list[str] | None = None
    config: dict[str, Any] | None = None


class OrchestrationResponse(BaseSchema):
    """Orchestration response schema."""
    id: UUID
    name: str
    version: str
    status: OrchestrationStatus
    description: str | None = None
    pattern: str
    dag: dict[str, Any]
    tags: list[str]
    compiled: bool
    created_at: datetime
    updated_at: datetime


# --- Execution Schemas ---


class ExecutionCreate(BaseModel):
    """Create execution request."""
    orchestration_id: UUID
    input_data: dict[str, Any] = {}
    triggered_by: str | None = None


class ExecutionResponse(BaseSchema):
    """Execution response schema."""
    id: UUID
    orchestration_id: UUID
    status: ExecutionStatus
    phase: ExecutionPhase
    input_data: dict[str, Any]
    output_data: dict[str, Any] | None = None
    error: str | None = None
    started_at: datetime | None = None
    ended_at: datetime | None = None
    duration_ms: int | None = None
    trace_id: str
    created_at: datetime
    updated_at: datetime


class ExecutionDetailResponse(ExecutionResponse):
    """Detailed execution response with full context."""
    state: dict[str, Any]
    context: dict[str, Any]
    error_details: dict[str, Any] | None = None


# --- Audit Log Schemas ---


class AuditLogResponse(BaseSchema):
    """Audit log response schema."""
    id: UUID
    entity_type: str
    entity_id: UUID | None = None
    action: str
    changes: dict[str, Any]
    user_id: str | None = None
    request_id: str | None = None
    created_at: datetime
