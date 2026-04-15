"""Core domain models for AMS-AI services."""

from datetime import datetime
from enum import Enum
from typing import Any
from uuid import UUID, uuid4

from sqlalchemy import JSON, Column, DateTime, Enum as SQLEnum
from sqlalchemy import ForeignKey, Index, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from ams_common.db import Base


# --- Enums ---


class AgentStatus(str, Enum):
    """Agent lifecycle status."""
    DRAFT = "draft"
    ACTIVE = "active"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class ToolCategory(str, Enum):
    """Tool/API categories."""
    HTTP = "http"
    DATABASE = "database"
    FILESYSTEM = "filesystem"
    MESSAGING = "messaging"
    CUSTOM = "custom"


class OrchestrationStatus(str, Enum):
    """Orchestration lifecycle status."""
    DRAFT = "draft"
    PUBLISHED = "published"
    DEPRECATED = "deprecated"
    ARCHIVED = "archived"


class ExecutionStatus(str, Enum):
    """Execution runtime status."""
    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    CANCELLED = "cancelled"
    TIMEOUT = "timeout"


class ExecutionPhase(str, Enum):
    """Execution workflow phase."""
    QUEUED = "queued"
    INITIALIZING = "initializing"
    EXECUTING = "executing"
    FINALIZING = "finalizing"
    COMPLETED = "completed"


# --- Base Time Mixin ---


class TimestampMixin:
    """Mixin for created_at and updated_at columns."""
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


# --- Models ---


class Agent(Base, TimestampMixin):
    """Agent registry model."""
    __tablename__ = "agents"
    __table_args__ = (
        Index("idx_agent_name", "name"),
        Index("idx_agent_status", "status"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Core fields
    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")
    framework: Mapped[str] = mapped_column(String(100))  # e.g., "langchain", "autogen", "crewai"
    status: Mapped[AgentStatus] = mapped_column(SQLEnum(AgentStatus), default=AgentStatus.DRAFT)

    # Description and metadata
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    tags: Mapped[list[str]] = mapped_column(JSON, default=[])

    # A2A Protocol
    a2a_compliant: Mapped[bool] = mapped_column(default=False)
    capabilities: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Configuration
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Ownership
    owner_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    namespace: Mapped[str] = mapped_column(String(100), default="default")

    __table_args__ = (
        UniqueConstraint("namespace", "name", "version", name="uc_agent_ns_name_version"),
    )


class Tool(Base, TimestampMixin):
    """Tool & API registry model."""
    __tablename__ = "tools"
    __table_args__ = (
        Index("idx_tool_name", "name"),
        Index("idx_tool_category", "category"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Core fields
    name: Mapped[str] = mapped_column(String(255))
    category: Mapped[ToolCategory] = mapped_column(SQLEnum(ToolCategory))
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")

    # Description
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Schema
    input_schema: Mapped[dict[str, Any]] = mapped_column(JSON, default={})
    output_schema: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Configuration
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Authentication
    auth_type: Mapped[str | None] = mapped_column(String(50), nullable=True)  # "api_key", "oauth", etc.
    auth_config: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Health & monitoring
    health_check_enabled: Mapped[bool] = mapped_column(default=True)
    health_check_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    last_health_check: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    is_healthy: Mapped[bool] = mapped_column(default=True)

    # Rate limiting
    rate_limit: Mapped[int | None] = mapped_column(nullable=True)
    namespace: Mapped[str] = mapped_column(String(100), default="default")


class Orchestration(Base, TimestampMixin):
    """Orchestration/Workflow DAG model."""
    __tablename__ = "orchestrations"
    __table_args__ = (
        Index("idx_orchestration_name", "name"),
        Index("idx_orchestration_status", "status"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Core fields
    name: Mapped[str] = mapped_column(String(255))
    version: Mapped[str] = mapped_column(String(50), default="1.0.0")
    status: Mapped[OrchestrationStatus] = mapped_column(
        SQLEnum(OrchestrationStatus), default=OrchestrationStatus.DRAFT
    )

    # Description
    description: Mapped[str | None] = mapped_column(Text, nullable=True)

    # DAG definition
    dag: Mapped[dict[str, Any]] = mapped_column(JSON)  # nodes, edges, execution plan

    # Patterns and metadata
    pattern: Mapped[str] = mapped_column(String(50))  # "sequential", "parallel", "conditional", etc.
    tags: Mapped[list[str]] = mapped_column(JSON, default=[])

    # Configuration
    config: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Ownership
    owner_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
    namespace: Mapped[str] = mapped_column(String(100), default="default")

    # Is compiled
    compiled: Mapped[bool] = mapped_column(default=False)
    compiled_plan: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)


class Execution(Base, TimestampMixin):
    """Execution/Run instance model."""
    __tablename__ = "executions"
    __table_args__ = (
        Index("idx_execution_status", "status"),
        Index("idx_execution_orchestration", "orchestration_id"),
        ForeignKey("orchestration_id", "orchestrations.id"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Relationship
    orchestration_id: Mapped[UUID] = mapped_column(ForeignKey("orchestrations.id"))

    # Status
    status: Mapped[ExecutionStatus] = mapped_column(
        SQLEnum(ExecutionStatus), default=ExecutionStatus.PENDING
    )
    phase: Mapped[ExecutionPhase] = mapped_column(
        SQLEnum(ExecutionPhase), default=ExecutionPhase.QUEUED
    )

    # Execution details
    input_data: Mapped[dict[str, Any]] = mapped_column(JSON, default={})
    output_data: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # State and context
    state: Mapped[dict[str, Any]] = mapped_column(JSON, default={})
    context: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Error tracking
    error: Mapped[str | None] = mapped_column(Text, nullable=True)
    error_details: Mapped[dict[str, Any] | None] = mapped_column(JSON, nullable=True)

    # Execution metrics
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    ended_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    duration_ms: Mapped[int | None] = mapped_column(nullable=True)

    # Ownership
    triggered_by: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Tracing
    parent_execution_id: Mapped[UUID | None] = mapped_column(
        ForeignKey("executions.id"), nullable=True
    )
    trace_id: Mapped[str] = mapped_column(String(255), default=lambda: str(uuid4()))


class ExecutionLog(Base, TimestampMixin):
    """Execution logs for debugging and auditing."""
    __tablename__ = "execution_logs"
    __table_args__ = (
        Index("idx_execution_log_execution", "execution_id"),
        ForeignKey("execution_id", "executions.id"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Relationship
    execution_id: Mapped[UUID] = mapped_column(ForeignKey("executions.id"))

    # Log content
    level: Mapped[str] = mapped_column(String(20))  # DEBUG, INFO, WARNING, ERROR
    message: Mapped[str] = mapped_column(Text)

    # Structured data
    context: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # Step/node reference
    node_id: Mapped[str | None] = mapped_column(String(255), nullable=True)


class AuditLog(Base, TimestampMixin):
    """Immutable audit logs for compliance."""
    __tablename__ = "audit_logs"
    __table_args__ = (
        Index("idx_audit_entity_type", "entity_type"),
        Index("idx_audit_entity_id", "entity_id"),
    )

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid4)

    # Entity reference
    entity_type: Mapped[str] = mapped_column(String(50))  # "agent", "orchestration", "execution", etc.
    entity_id: Mapped[UUID] = mapped_column(ForeignKey, nullable=True)

    # Change tracking
    action: Mapped[str] = mapped_column(String(50))  # "created", "updated", "deleted", "executed"
    changes: Mapped[dict[str, Any]] = mapped_column(JSON, default={})

    # User tracking
    user_id: Mapped[str | None] = mapped_column(String(255), nullable=True)

    # Request tracking
    request_id: Mapped[str | None] = mapped_column(String(255), nullable=True)
