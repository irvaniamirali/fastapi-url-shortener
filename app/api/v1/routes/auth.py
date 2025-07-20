from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_limiter.depends import RateLimiter
from datetime import timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
import logging

from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.services.user import create_user, get_user_by_email
from app.core.security import verify_password, create_access_token
from app.api.v1.deps import get_db, get_current_user
from app.models.user import User
from app.core.config import settings

router = APIRouter(tags=["Authentication"])
logger = logging.getLogger(__name__)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user account",
    dependencies=[
        Depends(
            RateLimiter(
                times=settings.RATE_LIMIT_REGISTER_TIMES,
                seconds=settings.RATE_LIMIT_REGISTER_SECONDS
            )
        )
    ]
)
async def register_user(
    user_create: UserCreate,
    db: AsyncSession = Depends(get_db),
):
    """
    Register a new user account with a unique email and password.
    Returns the created user's details.
    """
    logger.info(f"Registration attempt for email: {user_create.email}")
    existing_user = await get_user_by_email(db, email=user_create.email)
    if existing_user:
        logger.warning(f"Registration failed: Email '{user_create.email}' is already registered.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email is already registered.",
        )

    try:
        new_user = await create_user(db=db, user_create=user_create)
        logger.info(f"User '{new_user.email}' registered successfully with ID: {new_user.id}")
        return new_user
    except IntegrityError:
        logger.error(f"Database integrity error during registration for {user_create.email}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Failed to register user due to an internal database error (e.g., duplicate email)."
        )
    except Exception as e:
        logger.critical(f"Unexpected error during registration for {user_create.email}: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred during registration."
        )


@router.post(
    "/token",
    response_model=Token,
    summary="Authenticate user and return access token",
    dependencies=[
        Depends(
            RateLimiter(
                times=settings.RATE_LIMIT_LOGIN_TIMES,
                seconds=settings.RATE_LIMIT_LOGIN_SECONDS
            )
        )
    ]
)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db),
):
    """
    Authenticate user using email (as username) and password.
    Returns a JWT access token if successful.
    """
    logger.info(f"Login attempt for username: {form_data.username}")
    user = await get_user_by_email(db, email=form_data.username)

    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.warning(f"Login failed: Incorrect credentials for username '{form_data.username}'")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email},
        expires_delta=token_expires,
    )
    logger.info(f"User '{user.email}' logged in successfully and received access token.")
    return {"access_token": access_token, "token_type": "bearer"}


@router.get(
    "/me",
    response_model=UserResponse,
    summary="Get current authenticated user"
)
async def read_current_user(current_user: User = Depends(get_current_user)):
    """
    Return current authenticated user information based on the provided JWT token.
    """
    logger.debug(f"Fetching current user info for ID: {current_user.id}, Email: {current_user.email}")
    return current_user
