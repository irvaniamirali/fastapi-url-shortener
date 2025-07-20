from datetime import datetime, timedelta, timezone
from typing import Optional, Final
from jose import JWTError, jwt
from passlib.context import CryptContext
from app.schemas.token import TokenData
from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

JWT_ALGORITHM: Final[str] = settings.ALGORITHM
JWT_SECRET_KEY: Final[str] = settings.SECRET_KEY


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verifies a plain-text password against a hashed password.

    Args:
        plain_password (str): The password provided by the user (in plain text).
        hashed_password (str): The hashed password stored in the database.

    Returns:
        bool: True if the passwords match, False otherwise.
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hashes a plain-text password using bcrypt.

    Args:
        password (str): The plain-text password to hash.

    Returns:
        str: The hashed password.
    """
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Creates a JWT access token.

    Args:
        data (dict): The payload data to encode in the token (e.g., {"sub": user_email}).
        expires_delta (Optional[timedelta]): Optional timedelta for token expiration.
                                            If None, uses ACCESS_TOKEN_EXPIRE_MINUTES from settings.

    Returns:
        str: The encoded JWT access token.
    """
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """
    Decodes a JWT access token and extracts the payload.

    Args:
        token (str): The JWT access token string.

    Returns:
        TokenData: An object containing the decoded token data.

    Raises:
        JWTError: If the token is invalid, expired, or cannot be decoded.
    """
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_ALGORITHM])
        username: str | None = payload.get("sub")

        if username is None:
            raise JWTError("Token payload missing 'sub' claim.")

        token_data = TokenData(username=username)
    except JWTError:
        raise JWTError("Could not validate credentials (invalid token).")
    except Exception as e:
        raise JWTError(f"An unexpected error occurred during token decoding: {e}") from e
    return token_data
