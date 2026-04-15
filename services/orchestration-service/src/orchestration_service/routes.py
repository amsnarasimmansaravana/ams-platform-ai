"""Orchestration service API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import (
    Orchestration,
    OrchestrationStatus,
    PaginatedResponse,
    get_async_session,
)
from ams_common.domain_schemas import (
    OrchestrationCreate,
    OrchestrationResponse,
    OrchestrationUpdate,
)
from ams_common.logging import get_logger

from orchestration_service.repository import OrchestrationRepository

_LOG = get_logger(__name__)

router = APIRouter(prefix="/api/v1/orchestrations", tags=["orchestrations"])


@router.get("", response_model=PaginatedResponse[OrchestrationResponse])
async def list_orchestrations(
    namespace: str = Query(default="default"),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    """List orchestrations with pagination."""
    repo = OrchestrationRepository(session)
    items = await repo.list_by_namespace(namespace, skip, limit)
    total = await repo.count_by_namespace(namespace)
    return PaginatedResponse(
        items=[OrchestrationResponse.model_validate(item) for item in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=OrchestrationResponse, status_code=status.HTTP_201_CREATED)
async def create_orchestration(
    payload: OrchestrationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create a new orchestration."""
    repo = OrchestrationRepository(session)

    # Check for existing version
    existing = await repo.get_by_name_version(
        payload.namespace, payload.name, payload.version
    )
    if existing:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Orchestration {payload.namespace}/{payload.name}:{payload.version} already exists",
        )

    orch = Orchestration(
        name=payload.name,
        version=payload.version,
        description=payload.description,
        pattern=payload.pattern,
        dag=payload.dag,
        tags=payload.tags,
        config=payload.config,
        namespace=payload.namespace,
        status=OrchestrationStatus.DRAFT,
    )
    created = await repo.create(orch)
    await session.commit()
    _LOG.info("orchestration_created_via_api", orch_id=str(created.id))
    return OrchestrationResponse.model_validate(created)


@router.get("/{orch_id}", response_model=OrchestrationResponse)
async def get_orchestration(
    orch_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get a specific orchestration by ID."""
    repo = OrchestrationRepository(session)
    orch = await repo.get_by_id(orch_id)
    if not orch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orchestration {orch_id} not found",
        )
    return OrchestrationResponse.model_validate(orch)


@router.put("/{orch_id}", response_model=OrchestrationResponse)
async def update_orchestration(
    orch_id: UUID,
    payload: OrchestrationUpdate,
    session: AsyncSession = Depends(get_async_session),
):
    """Update an orchestration."""
    repo = OrchestrationRepository(session)
    orch = await repo.get_by_id(orch_id)
    if not orch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orchestration {orch_id} not found",
        )

    # Update fields
    if payload.description is not None:
        orch.description = payload.description
    if payload.status is not None:
        orch.status = payload.status
    if payload.dag is not None:
        orch.dag = payload.dag
        orch.compiled = False  # Reset compiled flag
    if payload.tags is not None:
        orch.tags = payload.tags
    if payload.config is not None:
        orch.config = payload.config

    updated = await repo.update(orch)
    await session.commit()
    _LOG.info("orchestration_updated_via_api", orch_id=str(orch_id))
    return OrchestrationResponse.model_validate(updated)


@router.post("/{orch_id}/compile", response_model=OrchestrationResponse)
async def compile_orchestration(
    orch_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Compile orchestration DAG to execution plan."""
    repo = OrchestrationRepository(session)
    orch = await repo.get_by_id(orch_id)
    if not orch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orchestration {orch_id} not found",
        )

    # TODO: Implement DAG validation and compilation
    compiled_plan = {"status": "pending_implementation"}

    compiled = await repo.compile(orch_id, compiled_plan)
    await session.commit()
    _LOG.info("orchestration_compiled_via_api", orch_id=str(orch_id))
    return OrchestrationResponse.model_validate(compiled)


@router.patch("/{orch_id}/status", response_model=OrchestrationResponse)
async def update_orchestration_status(
    orch_id: UUID,
    status: OrchestrationStatus,
    session: AsyncSession = Depends(get_async_session),
):
    """Update orchestration status."""
    repo = OrchestrationRepository(session)
    orch = await repo.update_status(orch_id, status)
    if not orch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orchestration {orch_id} not found",
        )
    await session.commit()
    _LOG.info("orchestration_status_updated_via_api", orch_id=str(orch_id), status=status.value)
    return OrchestrationResponse.model_validate(orch)


@router.delete("/{orch_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_orchestration(
    orch_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Delete an orchestration."""
    repo = OrchestrationRepository(session)
    deleted = await repo.delete(orch_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orchestration {orch_id} not found",
        )
    await session.commit()
    _LOG.info("orchestration_deleted_via_api", orch_id=str(orch_id))
