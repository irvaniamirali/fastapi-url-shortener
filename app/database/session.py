from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_async_engine(
    settings.DATABASE_URL,
    echo=settings.DATABASE_ECHO,
    future=True  # Use the SQLAlchemy 2.0 style future API
)

AsyncSessionLocal = sessionmaker(  # type: ignore
    autocommit=False,
    autoflush=False,
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False # Prevents objects from being expired after commit, allows access to attributes
)

async def get_async_session() -> AsyncSession:
    """
    Provides an asynchronous database session.
    This function is intended to be used directly where a session is needed,
    or wrapped by a FastAPI dependency.
    """
    async with AsyncSessionLocal() as session:
        yield session
