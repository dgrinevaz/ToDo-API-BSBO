from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_database_session
from database.tables.user import User
from contracts.authorization import UserRole
from contracts.authorization import CreateUserRequest, UserResponse, Token
from utils.auth_utils import verify_password, get_password_hash, create_access_token
from utils.dependencies import get_current_user

router = APIRouter(
 prefix="/authorization",
 tags=["authorization"]
)

@router.post("/register", response_model=UserResponse,
 status_code=status.HTTP_201_CREATED)
async def register(
 user_data: CreateUserRequest,
 db: AsyncSession = Depends(get_database_session)
):
    result = await db.execute(
    select(User).where(User.email == user_data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует")

    result = await db.execute(
    select(User).where(User.username == user_data.username))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким никнеймом уже существует")

    new_user = User(
        username=user_data.username,
        email=user_data.email,
        password=get_password_hash(user_data.password),
        role=UserRole.USER.value)

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login", response_model=Token)
async def login(
 form_data: OAuth2PasswordRequestForm = Depends(),
 db: AsyncSession = Depends(get_database_session)
):
    result = await db.execute(
    select(User).where(User.email == form_data.username))
    user = result.scalar_one_or_none()

    if not user or not verify_password(form_data.password, user.password):
     raise HTTPException(
         status_code=status.HTTP_401_UNAUTHORIZED,
         detail="Неверный email или пароль",
         headers={"WWW-Authenticate": "Bearer"})

    access_token = create_access_token(data={"sub": str(user.id), "role": user.role})
    return {"token_type": "bearer", "access_token": access_token}

@router.get("/me", response_model=UserResponse)
async def get_me(
 current_user: User = Depends(get_current_user)
):
    return current_user