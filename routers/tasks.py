from typing import List
from fastapi import APIRouter, Query, HTTPException, Response, status, Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from contracts.tasks import *
from database.database import get_database_session
from database.tables.task import *

router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)

@router.get("/")
async def get_tasks_by_filter(
        query: str = Query(default=None, min_length=2),
        quadrants: List[TaskQuadrant] = Query(default=None),
        statuses: List[TaskStatus] = Query(default=None),
        database: AsyncSession = Depends(get_database_session)) -> List[TaskResponse]:
    tasks = select(Task)
    if query:
        lower_query = query.strip().lower()
        tasks = tasks.where(lower_query in Task.title.lower()
                    or (Task.description and lower_query in Task.description.lower()))

    if quadrants:
        tasks = tasks.where(Task.quadrant.in_(quadrants))

    if statuses:
        tasks = tasks.where(Task.status.in_(statuses))

    result = await database.execute(tasks)
    tasks = result.scalars().all()

    return [TaskResponse.model_validate(t) for t in tasks]

@router.get("/{task_id}")
async def get_task_by_id(
        task_id: int,
        database: AsyncSession = Depends(get_database_session)) -> TaskResponse:
    result = await database.execute(select(Task).where(Task.id == task_id))
    task = result.scalar_one_or_none()
    if not task:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    return task

@router.post("/")
async def create_task(
        create_request: CreateTaskRequest,
        database: AsyncSession = Depends(get_database_session)) -> CreateTaskResponse:
    if create_request is None:
        raise HTTPException(status_code=400, detail="Запрос создания задачи не может быть null.")

    new_task = Task(
        title=create_request.title,
        description=create_request.description,
        quadrant=create_request.quadrant,
        status=create_request.status,
        created_at=datetime.now(),
        completed_at=None,
    )

    database.add(new_task)
    await database.commit()
    await database.refresh(new_task)

    return CreateTaskResponse(id=new_task.id)

@router.put("/")
async def update_task(
        update_request: UpdateTaskRequest,
        database: AsyncSession = Depends(get_database_session)):
    if update_request is None:
        raise HTTPException(status_code=400, detail="Запрос редактирования задачи не может быть null.")

    result = await database.execute(
        select(Task).where(Task.id == update_request.id))
    task_to_update = result.scalar_one_or_none()

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

    await database.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{task_id}")
async def delete_task_by_id(
        task_id: int,
        database: AsyncSession = Depends(get_database_session)):
    result = await database.execute(
        select(Task).where(Task.id == task_id))
    task_to_delete = result.scalar_one_or_none()
    if task_to_delete is None:
        raise HTTPException(status_code=404, detail="Задача не найдена")

    await database.delete(task_to_delete)
    await database.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)