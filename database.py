from typing import List
from datetime import datetime
from contracts.tasks import Task, TaskQuadrant, TaskStatus

tasks_db: List[Task] = [
    Task(
        id=1,
        title="Сдать проект по FastAPI",
        description="Завершить разработку API и написать документацию",
        is_important=True,
        is_urgent=True,
        quadrant=TaskQuadrant.Q1,
        status=TaskStatus.Pending,
        created_at=datetime.now()
    ),
    Task(
        id=2,
        title="Изучить SQLAlchemy",
        description="Прочитать документацию и попробовать примеры",
        is_important=True,
        is_urgent=False,
        quadrant=TaskQuadrant.Q2,
        status=TaskStatus.Pending,
        created_at=datetime.now()
    ),
    Task(
        id=3,
        title="Сходить на лекцию",
        description=None,
        is_important=False,
        is_urgent=True,
        quadrant=TaskQuadrant.Q3,
        status=TaskStatus.Pending,
        created_at=datetime.now()
    ),
    Task(
        id=4,
        title="Посмотреть сериал",
        description="Новый сезон любимого сериала",
        is_important=False,
        is_urgent=False,
        quadrant=TaskQuadrant.Q4,
        status=TaskStatus.Pending,
        created_at=datetime.now()
    )
]
