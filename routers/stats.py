from datetime import timezone
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from contracts.stats import *
from database.database import get_database_session
from contracts.tasks import TaskQuadrant, TaskStatus
from database.tables.task import Task

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get("")
async def get_tasks_stats(database: AsyncSession = Depends(get_database_session)) -> dict:
    total_result = await database.execute(
        select(func.count()).select_from(Task))
    total = total_result.scalar_one()

    by_quadrant: Dict[TaskQuadrant, int] = {q: 0 for q in TaskQuadrant}

    quadrant_result = await database.execute(
        select(Task.quadrant, func.count()).group_by(Task.quadrant)
    )

    for quadrant_value, count in quadrant_result.all():
        q_enum = TaskQuadrant(quadrant_value)
        by_quadrant[q_enum] = count

    by_status: Dict[TaskStatus, int] = {s: 0 for s in TaskStatus}

    status_result = await database.execute(
        select(Task.status, func.count())
        .group_by(Task.status)
    )

    for status_value, count in status_result.all():
        s_enum = TaskStatus(status_value)
        by_status[s_enum] = count

    return {
        "total_tasks": total,
        "by_quadrant": by_quadrant,
        "by_status": by_status,
    }

@router.get(
    "/deadlines",
    response_model=List[PendingTaskDeadlineResponse],
    summary="Статистика по срокам выполнения задач со статусом Pending",
)
async def get_pending_deadlines(
    database: AsyncSession = Depends(get_database_session),
) -> List[PendingTaskDeadlineResponse]:
    stmt = select(
        Task.title,
        Task.description,
        Task.created_at,
        Task.deadline_at,
    ).where(
        Task.status == TaskStatus.Pending.value
    )

    result = await database.execute(stmt)
    rows = result.all()

    today = datetime.now(timezone.utc).date()
    items: List[PendingTaskDeadlineResponse] = []

    for title, description, created_at, deadline_at in rows:
        remaining_days = (deadline_at.date() - today).days

        items.append(
            PendingTaskDeadlineResponse(
                title=title,
                description=description,
                start_date=created_at,
                deadline_at=deadline_at,
                remaining_days=remaining_days,
            )
        )

    return items
