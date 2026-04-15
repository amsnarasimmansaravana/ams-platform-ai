"""Agent service API routes."""

from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import (
    Agent,
    AgentStatus,
    ErrorResponse,
    PaginatedResponse,
    get_async_session,
)
from ams_common.domain_schemas import AgentCreate, AgentResponse, AgentUpdate
from ams_common.logging import get_logger

from agent_service.repository import AgentRepository

_LOG = get_logger(__name__)

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])


async def get_agent_repository(
    session: AsyncSession = Depends(lambda: get_async_session())  # type: ignore
) -> AgentRepository:
    """Dependency injection for agent repository."""
    return AgentRepository(session)


@router.get("", response_model=PaginatedResponse[AgentResponse])
async def list_agents(
    namespace: str = Query(default="default"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    """List agents with pagination."""
    repo = AgentRepository(session)
    items = await repo.list_by_namespace(namespace, skip, limit)
    total = await repo.count_by_namespace(namespace)
    return PaginatedResponse(
        items=[AgentResponse.model_validate(item) for item in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
async def create_agent(
    payload: AgentCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new agent."""
    repo = AgentRepository(session)

    # Check for existing version
    existing = await repo.get_by_name_version(payload.namespace, payload.name, payload.version)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Agent {payload.namespace}/{payload.name}:{payload.version} already exists",
        )

    agent = Agent(
        name=payload.name,
        framework=payload.framework,
        version=payload.version,
        description=payload.description,
        tags=payload.tags,
        a2a_compliant=payload.a2a_compliant,
        capabilities=payload.capabilities,
        config=payload.config,
        namespace=payload.namespace,
        status=AgentStatus.DRAFT,
    )
    created = await repo.create(agent)
    await session.commit()
    _LOG.info("agent_created_via_api", agent_id=str(created.id))
    return AgentResponse.model_validate(created)


@router.get("/name/{namespace}/{name}", response_model=list[AgentResponse])
async def get_agent_versions(
    namespace: str,
    name: str,
    session: AsyncSession = Depends(get_async_session),
):
    """Get all versions of an agent."""
    repo = AgentRepository(session)
    versions = await repo.list_versions(namespace, name)
    if not versions:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {namespace}/{name} not found",
        )
    return [AgentResponse.model_validate(v) for v in versions]


@router.get("/{agent_id}", response_model=AgentResponse)
async def get_agent(
    agent_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get a specific agent by ID."""
    repo = AgentRepository(session)
    agent = await repo.get_by_id(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found",
        )
    return AgentResponse.model_validate(agent)


@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(
    agent_id: UUID,
    payload: AgentUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Update an agent."""
    repo = AgentRepository(session)
    agent = await repo.get_by_id(agent_id)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found",
        )

    # Update fields
    if payload.description is not None:
        agent.description = payload.description
    if payload.status is not None:
        agent.status = payload.status
    if payload.tags is not None:
        agent.tags = payload.tags
    if payload.config is not None:
        agent.config = payload.config

    updated = await repo.update(agent)
    await session.commit()
    _LOG.info("agent_updated_via_api", agent_id=str(agent_id))
    return AgentResponse.model_validate(updated)


@router.patch("/{agent_id}/status", response_model=AgentResponse)
async def update_agent_status(
    agent_id: UUID,
    status: AgentStatus,
    session: AsyncSession = Depends(get_async_session),
):
    """Update agent status (transition agent lifecycle)."""
    repo = AgentRepository(session)
    agent = await repo.update_status(agent_id, status)
    if not agent:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found",
        )
    await session.commit()
    _LOG.info("agent_status_updated_via_api", agent_id=str(agent_id), status=status.value)
    return AgentResponse.model_validate(agent)


@router.delete("/{agent_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_agent(
    agent_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Delete an agent."""
    repo = AgentRepository(session)
    deleted = await repo.delete(agent_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Agent {agent_id} not found",
        )
    await session.commit()
    _LOG.info("agent_deleted_via_api", agent_id=str(agent_id))
