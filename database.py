from typing import List
from datetime import datetime
from contracts.tasks import Task, TaskQuadrant, TaskStatus

tasks_db: List[Task] = [
    Task(
        id=1,
        title="Сдать проект по FastAPI",
        description="Завершить разработку API и написать документацию",
        quadrant=TaskQuadrant.Q1,
        status=TaskStatus.Pending,
        created_at=datetime.now(),
        completed_at=None
    ),
    Task(
        id=2,
        title="Изучить SQLAlchemy",
        description="Прочитать документацию и попробовать примеры",
        quadrant=TaskQuadrant.Q2,
        status=TaskStatus.Pending,
        created_at=datetime.now(),
        completed_at=None
    ),
    Task(
        id=3,
        title="Сходить на лекцию",
        description=None,
        quadrant=TaskQuadrant.Q3,
        status=TaskStatus.Pending,
        created_at=datetime.now(),
        completed_at=None
    ),
    Task(
        id=4,
        title="Посмотреть сериал",
        description="Новый сезон любимого сериала",
        quadrant=TaskQuadrant.Q4,
        status=TaskStatus.Pending,
        created_at=datetime.now(),
        completed_at=None
    )
]
