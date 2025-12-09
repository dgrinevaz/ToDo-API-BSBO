from datetime import timezone
from typing import Dict, List
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from contracts.authorization import UserRole
from contracts.stats import *
from database.database import get_database_session
from contracts.tasks import TaskQuadrant, TaskStatus
from database.tables.task import Task
from database.tables.user import User
from utils.dependencies import get_current_user

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get("")
async def get_tasks_stats(
        current_user: User = Depends(get_current_user),
        database: AsyncSession = Depends(get_database_session)) -> dict:
    user_filter = None
    if current_user.role == UserRole.USER.value:
        user_filter = Task.user_id == current_user.id

    total_query = select(func.count()).select_from(Task)
    if user_filter is not None:
        total_query = total_query.where(user_filter)
    total = (await database.execute(total_query)).scalar_one()

    by_quadrant: Dict[TaskQuadrant, int] = {q: 0 for q in TaskQuadrant}
    by_quadrant_query = select(Task.quadrant, func.count()).group_by(Task.quadrant).select_from(Task)
    if user_filter is not None:
        by_quadrant_query = by_quadrant_query.where(user_filter)

    by_quadrant_result = await database.execute(by_quadrant_query)
    for quadrant_value, count in by_quadrant_result.all():
        q_enum = TaskQuadrant(quadrant_value)
        by_quadrant[q_enum] = count

    by_status: Dict[TaskStatus, int] = {s: 0 for s in TaskStatus}
    by_status_query = select(Task.status, func.count()).group_by(Task.status).select_from(Task)
    if user_filter is not None:
        by_status_query = by_status_query.where(user_filter)

    by_status_result = await database.execute(by_status_query)
    for status_value, count in by_status_result.all():
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
        current_user: User = Depends(get_current_user),
        database: AsyncSession = Depends(get_database_session)
) -> List[PendingTaskDeadlineResponse]:
    stmt = select(
        Task.title,
        Task.description,
        Task.created_at,
        Task.deadline_at,
    ).where(
        Task.status == TaskStatus.Pending.value
    )
    if current_user.role == UserRole.USER.value:
        stmt = stmt.where(Task.user_id == current_user.id)

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
