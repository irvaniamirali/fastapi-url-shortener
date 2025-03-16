from fastapi import APIRouter, status
from fastapi.exceptions import HTTPException
from datetime import timedelta

from app import utils
from app.models import User
from app.schema import UserBase, UserCreate, UserToken, Token
from app.configs import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(prefix="/users", tags=["Users"])

async def authenticate_user(email, password):
    user = await User.filter(email=email).first()
    if not user or not utils.verify_password(password, user.password):
        return False
    return user


@router.post("/", response_model=UserBase, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate):
    """
    Register a new user with unique email.

    :param user: UserCreate schema containing user registration details.
    :return: The created UserBase object.
    :raises HTTPException: If the email is already taken.
    """
    exist_user = await User.filter(email=user.email).first()

    if exist_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already taken."
        )

    params = {
        "user_id": utils.generate_random_digit_number(),
        "full_name": user.full_name,
        "email": user.email,
        "password": utils.get_password_hash(user.password)
    }
    return await User.create(**params)


@router.post("/token", response_model=Token, status_code=status.HTTP_200_OK)
async def login_for_access_token(form_data: UserToken):
    """
    Authenticate user and return a JWT token.

    :param form_data: UserToken schema containing email and password.
    :return: Token schema containing access token.
    :raises HTTPException: If authentication fails.
    """
    user = await authenticate_user(form_data.email, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = utils.create_access_token(
        data={"sub": str(user.user_id)}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
