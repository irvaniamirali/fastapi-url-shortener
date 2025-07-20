from app.database.session import engine
from app.database.base import Base

async def init_database():
    """
    Initializes the database by creating all defined tables.
    This function should be called at application startup.
    """
    print("Attempting to create database tables...")
    async with engine.begin() as conn:
        # Run synchronous metadata creation operation within the async context
        await conn.run_sync(Base.metadata.create_all)
    print("Database tables created or already exist.")
