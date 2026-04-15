"""Tool service repository and routes."""

from datetime import datetime
from typing import Optional
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import Tool
from ams_common.logging import get_logger

_LOG = get_logger(__name__)


class ToolRepository:
    """Data access layer for tools."""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._log = get_logger(f"{__name__}.{self.__class__.__name__}")

    async def create(self, tool: Tool) -> Tool:
        """Create a new tool."""
        self.session.add(tool)
        await self.session.flush()
        self._log.info("tool_created", tool_id=str(tool.id), name=tool.name)
        return tool

    async def get_by_id(self, tool_id: UUID) -> Optional[Tool]:
        """Get tool by ID."""
        stmt = select(Tool).where(Tool.id == tool_id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_by_name(self, namespace: str, name: str) -> Optional[Tool]:
        """Get tool by namespace and name."""
        stmt = select(Tool).where(
            (Tool.namespace == namespace) & (Tool.name == name)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def list_by_namespace(self, namespace: str, skip: int = 0, limit: int = 20):
        """List tools by namespace with pagination."""
        stmt = (
            select(Tool)
            .where(Tool.namespace == namespace)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def list_by_category(self, category: str, skip: int = 0, limit: int = 20):
        """List tools by category."""
        stmt = (
            select(Tool)
            .where(Tool.category == category)
            .offset(skip)
            .limit(limit)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def update(self, tool: Tool) -> Tool:
        """Update an existing tool."""
        await self.session.merge(tool)
        await self.session.flush()
        self._log.info("tool_updated", tool_id=str(tool.id), name=tool.name)
        return tool

    async def delete(self, tool_id: UUID) -> bool:
        """Delete a tool."""
        tool = await self.get_by_id(tool_id)
        if tool:
            await self.session.delete(tool)
            await self.session.flush()
            self._log.info("tool_deleted", tool_id=str(tool_id))
            return True
        return False

    async def update_health(self, tool_id: UUID, is_healthy: bool) -> Optional[Tool]:
        """Update tool health status."""
        tool = await self.get_by_id(tool_id)
        if tool:
            tool.is_healthy = is_healthy
            tool.last_health_check = datetime.utcnow()
            await self.update(tool)
        return tool

    async def count_by_namespace(self, namespace: str) -> int:
        """Count tools in a namespace."""
        stmt = select(Tool).where(Tool.namespace == namespace)
        result = await self.session.execute(stmt)
        return len(result.scalars().all())
