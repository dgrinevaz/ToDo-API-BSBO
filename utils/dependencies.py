from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database.database import get_database_session
from contracts.authorization import UserRole
from utils.auth_utils import decode_access_token
from typing import Optional
from database.tables.user import User
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

bearer_scheme = HTTPBearer()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v3/authorization/login")

async def get_current_user(
 credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
 db: AsyncSession = Depends(get_database_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"})

    token = credentials.credentials
    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    user_id: Optional[int] = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    result = await db.execute(
    select(User).where(User.id == int(user_id)) )
    user = result.scalar_one_or_none()

    if user is None:
        raise credentials_exception

    return user

async def get_current_admin(
 current_user: User = Depends(get_current_user)
) -> User:
    if current_user.role != UserRole.ADMIN.value:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Недостаточно прав доступа")

    return current_user