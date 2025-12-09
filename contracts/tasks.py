from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class TaskQuadrant(Enum):
    Q1 = "Q1"
    Q2 = "Q2"
    Q3 = "Q3"
    Q4 = "Q4"

class TaskStatus(Enum):
    Pending = "PENDING"
    InProgress = "IN_PROGRESS"
    Completed = "COMPLETED"

class TaskResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

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

    deadline_at: datetime = Field(
        ...,
        description="Дата дедлайна")

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

    deadline_at: datetime = Field(
        ...,
        description="Плановая дата завершения")

class CreateTaskResponse(BaseModel):
    id: int = Field(
        ...,
        description="Идентификатор")

class UpdateTaskRequest(BaseModel):
    id: int = Field(
        ...,
        gt=0,
        description="Идентификатор")

    title: str = Field(
        None,
        min_length=3,
        max_length=100,
        description="Название")

    description: str = Field(
        None,
        max_length=500,
        description="Описание")

    quadrant: TaskQuadrant = Field(
        None,
        description="Квадрант")

    status: TaskStatus = Field(
        None,
        description="Статус")
