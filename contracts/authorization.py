from enum import Enum
from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class UserRole(Enum):
    USER = "user"
    ADMIN = "admin"

class CreateUserRequest(BaseModel):
    username: str = Field(
    ...,
    min_length=3,
    max_length=50,
    description="Никнейм пользователя")

    email: EmailStr = Field(
    ...,
    description="Email пользователя")

    password: str = Field(
    ...,
    min_length=6,
    description="Пароль (минимум 6 символов)")

class LoginUserRequest(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

class Config:
    from_attributes = True

class Token(BaseModel):
    token_type: str = "bearer"
    access_token: str

class TokenData(BaseModel):
    user_id: Optional[int] = None
    role: Optional[str] = None
