"""Execution service repository."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import Execution, ExecutionLog, ExecutionPhase, ExecutionStatus
from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class ExecutionRepository:
    """Data access layer for executions."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._log = get_logger(f"{__name__}.{self.__class__.__name__}")

    async def create(self, execution: Execution) -> Execution:
        """Create a new execution."""
        self.session.add(execution)
        await self.session.flush()
        self._log.info("execution_created", exec_id=str(execution.id), trace_id=execution.trace_id)
        return execution

    async def get_by_id(self, exec_id: UUID) -> Optional[Execution]:
        """Get execution by ID."""
        stmt = select(Execution).where(Execution.id == exec_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_orchestration(
        self, orch_id: UUID, skip: int = 0, limit: int = 20
    ) -> list[Execution]:
        """List executions for an orchestration."""
        stmt = (
            select(Execution)
            .where(Execution.orchestration_id == orch_id)
            .order_by(Execution.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_status(
        self, status: ExecutionStatus, skip: int = 0, limit: int = 20
    ) -> list[Execution]:
        """List executions by status."""
        stmt = (
            select(Execution)
            .where(Execution.status == status)
            .order_by(Execution.created_at.desc())
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, execution: Execution) -> Execution:
        """Update an existing execution."""
        await self.session.merge(execution)
        await self.session.flush()
        self._log.info("execution_updated", exec_id=str(execution.id))
        return execution

    async def update_status(
        self, exec_id: UUID, status: ExecutionStatus, phase: Optional[ExecutionPhase] = None
    ) -> Optional[Execution]:
        """Update execution status (and optionally phase)."""
        execution = await self.get_by_id(exec_id)
        if execution:
            execution.status = status
            if phase:
                execution.phase = phase
            await self.update(execution)
            self._log.info("execution_status_updated", exec_id=str(exec_id), status=status.value)
        return execution

    async def add_log(
        self, exec_id: UUID, level: str, message: str, context: dict, node_id: Optional[str] = None
    ) -> ExecutionLog:
        """Add a log entry for an execution."""
        log = ExecutionLog(
            execution_id=exec_id,
            level=level,
            message=message,
            context=context,
            node_id=node_id,
        )
        self.session.add(log)
        await self.session.flush()
        return log

    async def complete(
        self, exec_id: UUID, output_data: dict, status: ExecutionStatus = ExecutionStatus.SUCCESS
    ) -> Optional[Execution]:
        """Complete an execution."""
        execution = await self.get_by_id(exec_id)
        if execution:
            execution.status = status
            execution.phase = ExecutionPhase.COMPLETED
            execution.output_data = output_data
            execution.ended_at = datetime.utcnow()
            if execution.started_at:
                duration_ms = int(
                    (execution.ended_at - execution.started_at).total_seconds() * 1000
                )
                execution.duration_ms = duration_ms
            await self.update(execution)
            self._log.info(
                "execution_completed",
                exec_id=str(exec_id),
                status=status.value,
                duration_ms=execution.duration_ms,
            )
        return execution

    async def fail(
        self, exec_id: UUID, error: str, error_details: Optional[dict] = None
    ) -> Optional[Execution]:
        """Mark execution as failed."""
        execution = await self.get_by_id(exec_id)
        if execution:
            execution.status = ExecutionStatus.FAILED
            execution.phase = ExecutionPhase.COMPLETED
            execution.error = error
            execution.error_details = error_details or {}
            execution.ended_at = datetime.utcnow()
            if execution.started_at:
                duration_ms = int(
                    (execution.ended_at - execution.started_at).total_seconds() * 1000
                )
                execution.duration_ms = duration_ms
            await self.update(execution)
            self._log.error("execution_failed", exec_id=str(exec_id), error=error)
        return execution

    async def count_by_orchestration(self, orch_id: UUID) -> int:
        """Count executions for an orchestration."""
        stmt = select(Execution).where(Execution.orchestration_id == orch_id)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())
