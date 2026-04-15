"""Agent repository for database operations."""

from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import Agent, AgentStatus
from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class AgentRepository:
    """Data access layer for agents."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._log = get_logger(f"{__name__}.{self.__class__.__name__}")

    async def create(self, agent: Agent) -> Agent:
        """Create a new agent."""
        self.session.add(agent)
        await self.session.flush()
        self._log.info("agent_created", agent_id=str(agent.id), name=agent.name)
        return agent

    async def get_by_id(self, agent_id: UUID) -> Optional[Agent]:
        """Get agent by ID."""
        stmt = select(Agent).where(Agent.id == agent_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name_version(
        self, namespace: str, name: str, version: str
    ) -> Optional[Agent]:
        """Get agent by namespace, name, and version."""
        stmt = select(Agent).where(
            (Agent.namespace == namespace)
            & (Agent.name == name)
            & (Agent.version == version)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_namespace(self, namespace: str, skip: int = 0, limit: int = 20):
        """List agents by namespace with pagination."""
        stmt = (
            select(Agent)
            .where(Agent.namespace == namespace)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_versions(self, namespace: str, name: str) -> list[Agent]:
        """List all versions of an agent."""
        stmt = select(Agent).where(
            (Agent.namespace == namespace) & (Agent.name == name)
        ).order_by(Agent.version.desc())
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, agent: Agent) -> Agent:
        """Update an existing agent."""
        await self.session.merge(agent)
        await self.session.flush()
        self._log.info("agent_updated", agent_id=str(agent.id), name=agent.name)
        return agent

    async def update_status(self, agent_id: UUID, status: AgentStatus) -> Optional[Agent]:
        """Update agent status."""
        agent = await self.get_by_id(agent_id)
        if agent:
            agent.status = status
            await self.update(agent)
            self._log.info("agent_status_updated", agent_id=str(agent_id), status=status.value)
        return agent

    async def delete(self, agent_id: UUID) -> bool:
        """Delete an agent (soft delete via ARCHIVED status preferred)."""
        agent = await self.get_by_id(agent_id)
        if agent:
            await self.session.delete(agent)
            await self.session.flush()
            self._log.info("agent_deleted", agent_id=str(agent_id))
            return True
        return False

    async def count_by_namespace(self, namespace: str) -> int:
        """Count agents in a namespace."""
        stmt = select(Agent).where(Agent.namespace == namespace)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())
