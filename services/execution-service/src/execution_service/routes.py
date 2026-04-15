"""Execution service API routes."""

from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from ams_common import (
    Execution,
    ExecutionStatus,
    PaginatedResponse,
    get_async_session,
)
from ams_common.domain_schemas import ExecutionCreate, ExecutionResponse, ExecutionDetailResponse
from ams_common.logging import get_logger

from execution_service.repository import ExecutionRepository

_LOG = get_logger(__name__)

router = APIRouter(prefix="/api/v1/executions", tags=["executions"])


@router.get("", response_model=PaginatedResponse[ExecutionResponse])
async def list_executions(
    orchestration_id: UUID | None = Query(default=None),
    status_filter: ExecutionStatus | None = Query(default=None),
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
):
    """List executions with optional filtering."""
    repo = ExecutionRepository(session)

    if orchestration_id:
        items = await repo.list_by_orchestration(orchestration_id, skip, limit)
        total = await repo.count_by_orchestration(orchestration_id)
    elif status_filter:
        items = await repo.list_by_status(status_filter, skip, limit)
        total = len(items)  # TODO: Add count method
    else:
        items = []
        total = 0

    return PaginatedResponse(
        items=[ExecutionResponse.model_validate(item) for item in items],
        total=total,
        skip=skip,
        limit=limit,
    )


@router.post("", response_model=ExecutionResponse, status_code=status.HTTP_201_CREATED)
async def create_execution(
    payload: ExecutionCreate,
    session: AsyncSession = Depends(get_async_session),
):
    """Create and trigger a new execution."""
    repo = ExecutionRepository(session)

    # TODO: Validate orchestration exists

    execution = Execution(
        orchestration_id=payload.orchestration_id,
        input_data=payload.input_data,
        triggered_by=payload.triggered_by,
        status=ExecutionStatus.PENDING,
    )
    created = await repo.create(execution)
    await session.commit()
    _LOG.info("execution_created_via_api", exec_id=str(created.id), orch_id=str(payload.orchestration_id))

    # TODO: Trigger Celery task to execute

    return ExecutionResponse.model_validate(created)


@router.get("/{exec_id}", response_model=ExecutionDetailResponse)
async def get_execution(
    exec_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get execution details."""
    repo = ExecutionRepository(session)
    execution = await repo.get_by_id(exec_id)
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Execution {exec_id} not found",
        )
    return ExecutionDetailResponse.model_validate(execution)


@router.get("/{exec_id}/status", response_model=dict)
async def get_execution_status(
    exec_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Get only the execution status."""
    repo = ExecutionRepository(session)
    execution = await repo.get_by_id(exec_id)
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Execution {exec_id} not found",
        )
    return {
        "id": execution.id,
        "status": execution.status.value,
        "phase": execution.phase.value,
        "started_at": execution.started_at,
        "ended_at": execution.ended_at,
        "duration_ms": execution.duration_ms,
    }


@router.post("/{exec_id}/cancel", response_model=ExecutionResponse)
async def cancel_execution(
    exec_id: UUID,
    session: AsyncSession = Depends(get_async_session),
):
    """Cancel an execution."""
    repo = ExecutionRepository(session)
    execution = await repo.update_status(exec_id, ExecutionStatus.CANCELLED)
    if not execution:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Execution {exec_id} not found",
        )
    await session.commit()
    _LOG.info("execution_cancelled_via_api", exec_id=str(exec_id))
    return ExecutionResponse.model_validate(execution)
