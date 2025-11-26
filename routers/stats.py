from typing import Dict
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
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
