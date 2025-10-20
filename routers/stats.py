from typing import Dict
from fastapi import APIRouter
from database import tasks_db
from contracts.tasks import TaskQuadrant, TaskStatus

router = APIRouter(
    prefix="/stats",
    tags=["stats"]
)

@router.get("")
async def get_tasks_stats() -> dict:
    total = len(tasks_db)
    by_quadrant: Dict[TaskQuadrant, int] = {q: 0 for q in TaskQuadrant}
    by_status: Dict[TaskStatus, int] = {q: 0 for q in TaskStatus}

    for task in tasks_db:
        by_quadrant[task.quadrant] += 1
        by_status[task.status] += 1

    return {
        "total_tasks": total,
        "by_quadrant": by_quadrant,
        "by_status": by_status
    }
