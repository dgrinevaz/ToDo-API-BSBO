from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field


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
    id: int = Field(
        ...,
        description="Идентификатор")

    title: str = Field(
     ...,
     min_length=3,
     max_length=100,
     description="Название")

    description: Optional[str] = Field(
     None,
     max_length=500,
     description="Описание")

    quadrant: TaskQuadrant = Field(
        ...,
        description="Квадрант")

    status: TaskStatus = Field(
        ...,
        description="Статус")

    created_at: datetime = Field(
        ...,
        description="Дата создания")

    completed_at: Optional[datetime] = Field(
        ...,
        description="Дата закрытия")

class CreateTaskRequest(BaseModel):
    title: str = Field(
     ...,
     min_length=3,
     max_length=100,
     description="Название")

    description: Optional[str] = Field(
     None,
     max_length=500,
     description="Описание")

    quadrant: TaskQuadrant = Field(
        ...,
        description="Квадрант")

    status: TaskStatus = Field(
        ...,
        description="Статус")

class CreateTaskResponse(BaseModel):
    id: int = Field(
        ...,
        description="Идентификатор")

class UpdateTaskRequest(BaseModel):
    id: int = Field(
        ...,
        gt=0,
        description="Идентификатор")

    title: Optional[str] = Field(
     ...,
     min_length=3,
     max_length=100,
     description="Название")

    description: Optional[str] = Field(
     None,
     max_length=500,
     description="Описание")

    quadrant: Optional[TaskQuadrant] = Field(
        ...,
        description="Квадрант")

    status: Optional[TaskStatus] = Field(
        ...,
        description="Статус")
