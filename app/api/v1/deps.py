from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncGenerator
from jose import JWTError, jwt

from app.database.session import AsyncSessionLocal
from app.core.security import decode_access_token
from app.services.user import get_user_by_email
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/token")

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependency to provide a database session.
    Ensures the session is properly closed after use.
    """
    async with AsyncSessionLocal() as db_session:
        try:
            yield db_session
        finally:
            await db_session.close()

async def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: AsyncSession = Depends(get_db)
) -> User:
    """
    Dependency to get the current authenticated user.
    Validates the JWT token and fetches the user from the database.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        token_data = decode_access_token(token)
    except JWTError as e:
        raise credentials_exception from e

    user = await get_user_by_email(db, email=token_data.username)
    if user is None:
        raise credentials_exception
    return user
