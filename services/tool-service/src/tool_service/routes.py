"""Tool service API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import (
    ErrorResponse,
    PaginatedResponse,
    ToolCategory,
    get_async_session,
)
from ams_common.domain_schemas import ToolCreate, ToolResponse, ToolUpdate
from ams_common.logging import get_logger

from tool_service.repository import ToolRepository

_LOG = get_logger(__name__)

router = APIRouter(prefix="/api/v1/tools", tags=["tools"])


@router.get("", response_model=PaginatedResponse[ToolResponse])
async def list_tools(
    namespace: str = Query(default="default"),
    category: ToolCategory | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    """List tools with optional filtering by category."""
    repo = ToolRepository(session)
    if category:
        items = await repo.list_by_category(category.value, skip, limit)
    else:
        items = await repo.list_by_namespace(namespace, skip, limit)
    total = await repo.count_by_namespace(namespace)
    return PaginatedResponse(
        items=[ToolResponse.model_validate(item) for item in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=ToolResponse, status_code=status.HTTP_201_CREATED)
async def create_tool(
    payload: ToolCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new tool."""
    repo = ToolRepository(session)

    # Check for existing
    existing = await repo.get_by_name(payload.namespace, payload.name)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Tool {payload.namespace}/{payload.name} already exists",
        )

    from ams_common import Tool

    tool = Tool(
        name=payload.name,
        category=payload.category,
        version=payload.version,
        description=payload.description,
        input_schema=payload.input_schema,
        output_schema=payload.output_schema,
        config=payload.config,
        auth_type=payload.auth_type,
        auth_config=payload.auth_config,
        health_check_enabled=payload.health_check_enabled,
        health_check_url=payload.health_check_url,
        rate_limit=payload.rate_limit,
        namespace=payload.namespace,
    )
    created = await repo.create(tool)
    await session.commit()
    _LOG.info("tool_created_via_api", tool_id=str(created.id))
    return ToolResponse.model_validate(created)


@router.get("/{tool_id}", response_model=ToolResponse)
async def get_tool(
    tool_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get a specific tool by ID."""
    repo = ToolRepository(session)
    tool = await repo.get_by_id(tool_id)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool {tool_id} not found",
        )
    return ToolResponse.model_validate(tool)


@router.put("/{tool_id}", response_model=ToolResponse)
async def update_tool(
    tool_id: UUID,
    payload: ToolUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Update a tool."""
    repo = ToolRepository(session)
    tool = await repo.get_by_id(tool_id)
    if not tool:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool {tool_id} not found",
        )

    # Update fields
    if payload.description is not None:
        tool.description = payload.description
    if payload.input_schema is not None:
        tool.input_schema = payload.input_schema
    if payload.output_schema is not None:
        tool.output_schema = payload.output_schema
    if payload.config is not None:
        tool.config = payload.config
    if payload.is_healthy is not None:
        tool.is_healthy = payload.is_healthy
    if payload.rate_limit is not None:
        tool.rate_limit = payload.rate_limit

    updated = await repo.update(tool)
    await session.commit()
    _LOG.info("tool_updated_via_api", tool_id=str(tool_id))
    return ToolResponse.model_validate(updated)


@router.delete("/{tool_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_tool(
    tool_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Delete a tool."""
    repo = ToolRepository(session)
    deleted = await repo.delete(tool_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tool {tool_id} not found",
        )
    await session.commit()
    _LOG.info("tool_deleted_via_api", tool_id=str(tool_id))
