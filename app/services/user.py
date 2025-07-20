from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """
    Asynchronously retrieves a user from the database by their email address.

    Args:
        db (AsyncSession): The asynchronous database session.
        email (str): The email address of the user to retrieve.

    Returns:
        User | None: The User object if found, otherwise None.
    """
    result = await db.execute(select(User).where(User.email == email))
    return result.scalars().first()


async def create_user(db: AsyncSession, user_create: UserCreate) -> User:
    """
    Asynchronously creates a new user in the database.

    Args:
        db (AsyncSession): The asynchronous database session.
        user_create (UserCreate): The schema containing user creation data (email and password).

    Returns:
        User: The newly created User object.

    Raises:
        IntegrityError: If a user with the given email already exists (e.g., due to unique constraint).
    """
    hashed_password = get_password_hash(user_create.password)
    db_user = User(email=str(user_create.email), hashed_password=hashed_password)

    try:
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return db_user
    except IntegrityError:
        await db.rollback()
        raise
    except Exception:
        await db.rollback()
        raise
