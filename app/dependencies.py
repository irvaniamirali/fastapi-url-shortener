from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt

from app.models.users import User
from app.schema.token import TokenData
from app.errors import ErrorCode
from configs import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Exception reused to avoid duplication
credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail=ErrorCode.UNAUTHORIZED,
    headers={"WWW-Authenticate": "Bearer"},
)

async def get_user_by_id(user_id: int):
    return await User.filter(user_id=user_id).first()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        token_data = TokenData(user_id=int(user_id))
    except (JWTError, ValueError):
        raise credentials_exception

    user = await get_user_by_id(token_data.user_id)
    if user is None:
        raise credentials_exception
    return user
