"""Orchestration service repository."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import Orchestration, OrchestrationStatus
from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class OrchestrationRepository:
    """Data access layer for orchestrations."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._log = get_logger(f"{__name__}.{self.__class__.__name__}")

    async def create(self, orch: Orchestration) -> Orchestration:
        """Create a new orchestration."""
        self.session.add(orch)
        await self.session.flush()
        self._log.info("orchestration_created", orch_id=str(orch.id), name=orch.name)
        return orch

    async def get_by_id(self, orch_id: UUID) -> Optional[Orchestration]:
        """Get orchestration by ID."""
        stmt = select(Orchestration).where(Orchestration.id == orch_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name_version(
        self, namespace: str, name: str, version: str
    ) -> Optional[Orchestration]:
        """Get orchestration by namespace, name, and version."""
        stmt = select(Orchestration).where(
            (Orchestration.namespace == namespace)
            & (Orchestration.name == name)
            & (Orchestration.version == version)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_namespace(self, namespace: str, skip: int = 0, limit: int = 20):
        """List orchestrations by namespace with pagination."""
        stmt = (
            select(Orchestration)
            .where(Orchestration.namespace == namespace)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_versions(self, namespace: str, name: str) -> list[Orchestration]:
        """List all versions of an orchestration."""
        stmt = select(Orchestration).where(
            (Orchestration.namespace == namespace) & (Orchestration.name == name)
        ).order_by(Orchestration.version.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, orch: Orchestration) -> Orchestration:
        """Update an existing orchestration."""
        await self.session.merge(orch)
        await self.session.flush()
        self._log.info("orchestration_updated", orch_id=str(orch.id))
        return orch

    async def update_status(
        self, orch_id: UUID, status: OrchestrationStatus
    ) -> Optional[Orchestration]:
        """Update orchestration status."""
        orch = await self.get_by_id(orch_id)
        if orch:
            orch.status = status
            await self.update(orch)
        return orch

    async def compile(self, orch_id: UUID, compiled_plan: dict) -> Optional[Orchestration]:
        """Compile and store execution plan."""
        orch = await self.get_by_id(orch_id)
        if orch:
            orch.compiled = True
            orch.compiled_plan = compiled_plan
            await self.update(orch)
            self._log.info("orchestration_compiled", orch_id=str(orch_id))
        return orch

    async def delete(self, orch_id: UUID) -> bool:
        """Delete an orchestration."""
        orch = await self.get_by_id(orch_id)
        if orch:
            await self.session.delete(orch)
            await self.session.flush()
            self._log.info("orchestration_deleted", orch_id=str(orch_id))
            return True
        return False

    async def count_by_namespace(self, namespace: str) -> int:
        """Count orchestrations in a namespace."""
        stmt = select(Orchestration).where(Orchestration.namespace == namespace)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())
