from typing import List
from fastapi import APIRouter, Query, HTTPException
from contracts.tasks import *
from database import tasks_db

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("")
async def get_tasks_by_filter(
        query: str = Query(default=None, min_length=2),
        quadrants: List[TaskQuadrant] = Query(default=None),
        statuses: List[TaskStatus] = Query(default=None)) -> List[Task]:
    tasks = tasks_db
    if query:
        tasks = [task for task in tasks
                 if query.lower() in task.title.lower()
                    or (task.description and query.lower() in task.description.lower())]

    if quadrants:
        tasks = [task for task in tasks if task.quadrant in quadrants]

    if statuses:
        tasks = [task for task in tasks if task.status in statuses]

    return tasks

@router.get("/{task_id}")
async def get_task_by_id(task_id: int) -> Task:
    task = next(filter(lambda t: t.id == task_id, tasks_db), None)
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task

@router.post("/")
async def create_task(create_request: CreateTaskRequest) -> CreateTaskResponse:
    if create_request is None:
        raise HTTPException(status_code=400, detail="Запрос создания задачи не может быть null.")

    new_id = tasks_db[-1].id + 1
    created_task = Task(
        id=new_id,
        title=create_request.title,
        description=create_request.description,
        quadrant=create_request.quadrant,
        status=create_request.status,
        created_at=datetime.now(),
        completed_at=None)

    tasks_db.append(created_task)
    return CreateTaskResponse(id=new_id)

@router.put("/")
async def update_task(update_request: UpdateTaskRequest):
    if update_request is None:
        raise HTTPException(status_code=400, detail="Запрос редактирования задачи не может быть null.")

    task_to_update = await get_task_by_id(update_request.id)

    if update_request.title and task_to_update.title != update_request.title:
        task_to_update.title = update_request.title

    if update_request.description and task_to_update.description != update_request.description:
        task_to_update.description = update_request.description

    if update_request.quadrant and task_to_update.quadrant != update_request.quadrant:
        task_to_update.quadrant = update_request.quadrant

    if update_request.status and task_to_update.status != update_request.status:
        task_to_update.status = update_request.status

        if update_request.status == TaskStatus.Completed:
            task_to_update.completed_at = datetime.now()

@router.delete("/{task_id}")
async def delete_task_by_id(task_id: int):
    task_to_delete = await get_task_by_id(task_id)
    tasks_db.remove(task_to_delete)