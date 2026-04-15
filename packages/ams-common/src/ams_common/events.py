"""Event publishing and subscription for inter-service communication."""

from dataclasses import dataclass, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Callable, Optional
from uuid import UUID, uuid4

from ams_common.celery_app import get_celery_app
from ams_common.config import ServiceSettings
from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class EventType(str, Enum):
    """Domain events across AMS-AI."""
    # Agent events
    AGENT_CREATED = "agent.created"
    AGENT_UPDATED = "agent.updated"
    AGENT_STATUS_CHANGED = "agent.status_changed"
    AGENT_DELETED = "agent.deleted"

    # Tool events
    TOOL_CREATED = "tool.created"
    TOOL_UPDATED = "tool.updated"
    TOOL_HEALTH_CHECK = "tool.health_check"

    # Orchestration events
    ORCHESTRATION_CREATED = "orchestration.created"
    ORCHESTRATION_COMPILED = "orchestration.compiled"
    ORCHESTRATION_PUBLISHED = "orchestration.published"

    # Execution events
    EXECUTION_STARTED = "execution.started"
    EXECUTION_PROGRESS = "execution.progress"
    EXECUTION_COMPLETED = "execution.completed"
    EXECUTION_FAILED = "execution.failed"


@dataclass
class DomainEvent:
    """Base class for domain events."""
    event_type: EventType
    aggregate_id: UUID
    aggregate_type: str  # "agent", "orchestration", "execution", etc.
    data: dict[str, Any]
    timestamp: datetime
    event_id: UUID = None  # type: ignore

    def __post_init__(self):
        if self.event_id is None:
            self.event_id = uuid4()

    def to_dict(self) -> dict[str, Any]:
        """Serialize event to dictionary."""
        return {
            "event_id": str(self.event_id),
            "event_type": self.event_type.value,
            "aggregate_id": str(self.aggregate_id),
            "aggregate_type": self.aggregate_type,
            "data": self.data,
            "timestamp": self.timestamp.isoformat(),
        }


class EventPublisher:
    """Publish domain events for inter-service subscriptions."""

    def __init__(self, settings: ServiceSettings):
        self.settings = settings
        self.celery_app = get_celery_app(settings)
        self._log = get_logger(f"{__name__}.{self.__class__.__name__}")

    async def publish(self, event: DomainEvent) -> str:
        """Publish a domain event."""
        event_data = event.to_dict()
        self._log.info(
            "event_published",
            event_type=event.event_type.value,
            aggregate_id=str(event.aggregate_id),
        )

        # Send via Celery for async handling
        task_name = f"ams_ai.events.{event.event_type.value}"
        task = self.celery_app.send_task(task_name, kwargs={"event_data": event_data})
        return task.id

    async def publish_agent_created(self, agent_id: UUID, agent_data: dict[str, Any]) -> str:
        """Publish agent created event."""
        event = DomainEvent(
            event_type=EventType.AGENT_CREATED,
            aggregate_id=agent_id,
            aggregate_type="agent",
            data=agent_data,
            timestamp=datetime.utcnow(),
        )
        return await self.publish(event)

    async def publish_orchestration_compiled(
        self, orch_id: UUID, orch_data: dict[str, Any]
    ) -> str:
        """Publish orchestration compiled event."""
        event = DomainEvent(
            event_type=EventType.ORCHESTRATION_COMPILED,
            aggregate_id=orch_id,
            aggregate_type="orchestration",
            data=orch_data,
            timestamp=datetime.utcnow(),
        )
        return await self.publish(event)

    async def publish_execution_started(self, exec_id: UUID, exec_data: dict[str, Any]) -> str:
        """Publish execution started event."""
        event = DomainEvent(
            event_type=EventType.EXECUTION_STARTED,
            aggregate_id=exec_id,
            aggregate_type="execution",
            data=exec_data,
            timestamp=datetime.utcnow(),
        )
        return await self.publish(event)

    async def publish_execution_completed(self, exec_id: UUID, exec_data: dict[str, Any]) -> str:
        """Publish execution completed event."""
        event = DomainEvent(
            event_type=EventType.EXECUTION_COMPLETED,
            aggregate_id=exec_id,
            aggregate_type="execution",
            data=exec_data,
            timestamp=datetime.utcnow(),
        )
        return await self.publish(event)

    async def publish_execution_failed(
        self, exec_id: UUID, error: str, exec_data: Optional[dict[str, Any]] = None
    ) -> str:
        """Publish execution failed event."""
        data = exec_data or {}
        data["error"] = error
        event = DomainEvent(
            event_type=EventType.EXECUTION_FAILED,
            aggregate_id=exec_id,
            aggregate_type="execution",
            data=data,
            timestamp=datetime.utcnow(),
        )
        return await self.publish(event)


class EventHandler:
    """Handle incoming domain events (to be implemented by consuming services)."""

    async def handle(self, event: DomainEvent) -> None:
        """Handle a domain event. Override in subclasses."""
        raise NotImplementedError
