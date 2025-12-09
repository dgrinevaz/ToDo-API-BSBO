from pydantic import BaseModel, Field, EmailStr

class UserWithTasksResponse(BaseModel):
    id: int = Field(..., description="Идентификатор пользователя")
    username: str = Field(..., description="Никнейм пользователя")
    email: EmailStr = Field(..., description="Email пользователя")
    role: str = Field(..., description="Роль пользователя")
    tasks_count: int = Field(
        ...,
        ge=0,
        description="Количество задач, принадлежащих пользователю",
    )