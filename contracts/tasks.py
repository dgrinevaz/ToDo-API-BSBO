from datetime import datetime
from enum import Enum
from pydantic import BaseModel


class TaskQuadrant(Enum):
    Q1 = "q1"
    Q2 = "q2"
    Q3 = "q3"
    Q4 = "q4"


class TaskStatus(Enum):
    Pending = "pending"
    InProgress = "in_progress"
    Completed = "completed"


class Task(BaseModel):
    id: int
    title: str
    description: str | None
    is_important: bool
    is_urgent: bool
    quadrant: TaskQuadrant
    status: TaskStatus
    created_at: datetime
