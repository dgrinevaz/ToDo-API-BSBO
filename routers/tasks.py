from typing import List
from fastapi import APIRouter, Query, HTTPException
from contracts.tasks import Task, TaskQuadrant, TaskStatus
from database import tasks_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("")
async def get_tasks_by_filter(
        query: str = Query(default=None, min_length=2),
        quadrant: TaskQuadrant = Query(default=None),
        status: TaskStatus = Query(default=None)) -> List[Task]:
    tasks = tasks_db
    if query:
        tasks = [task for task in tasks
                 if query.lower() in task.title.lower() or query.lower() in task.description.lower()]

    if quadrant:
        tasks = [task for task in tasks if task.quadrant == quadrant]

    if status:
        tasks = [task for task in tasks if task.status == status]

    return tasks

@router.get("/{task_id}")
async def get_task_by_id(id: int) -> Task:
    task = next(task for task in tasks_db if task.id == id)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task
