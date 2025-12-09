from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from contracts.admin import UserWithTasksResponse
from database.database import get_database_session
from database.tables.task import Task
from database.tables.user import User
from utils.dependencies import get_current_admin

router = APIRouter(
    prefix="/admin",
    tags=["admin"],
)

@router.get(
    "/users",
    response_model=List[UserWithTasksResponse],
    summary="Список всех пользователей с количеством их задач (только для администраторов)",
)
async def get_users_with_tasks_stats(
        current_admin: User = Depends(get_current_admin),
        database: AsyncSession = Depends(get_database_session),
) -> List[UserWithTasksResponse]:
    stmt = (
        select(
            User.id,
            User.username,
            User.email,
            User.role,
            func.count(Task.id).label("tasks_count"),
        )
        .outerjoin(Task, Task.user_id == User.id)
        .group_by(User.id, User.username, User.email, User.role)
        .order_by(User.id)
    )

    result = await database.execute(stmt)
    rows = result.all()

    items: List[UserWithTasksResponse] = []

    for row in rows:
        items.append(
            UserWithTasksResponse(
                id=row.id,
                username=row.username,
                email=row.email,
                role=row.role,
                tasks_count=row.tasks_count,
            )
        )

    return items