from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict


class PendingTaskDeadlineResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    title: str = Field(..., description="Название задачи")
    description: Optional[str] = Field(None, description="Описание задачи")
    start_date: datetime = Field(..., description="Дата создания задачи")
    deadline_at: datetime = Field(..., description="Дедлайн задачи")
    remaining_days: int = Field(..., description="Оставшийся срок до дедлайна в днях")