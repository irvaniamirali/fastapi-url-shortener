from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from redis.asyncio import Redis
from fastapi_limiter import FastAPILimiter
import logging

from app.database import init_database
from app.api.v1 import router as api_router
from app.core.config import settings

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """
    Manages the lifespan of the FastAPI application.
    Initializes the database and Redis for rate limiting before the application starts.
    """
    logger.info("Application startup: Initializing database...")
    await init_database()
    logger.info("Database initialized.")

    try:
        redis_client = Redis.from_url(settings.REDIS_URL, encoding="utf-8", decode_responses=True)
        await FastAPILimiter.init(redis_client)
        logger.info("FastAPI-Limiter initialized with Redis.")
    except Exception as e:
        logger.critical(f"Failed to connect to Redis for Rate Limiting: {e}", exc_info=True)

    logger.info("Application ready.")
    yield

    logger.info("Application shutdown: Cleaning up resources...")

    if FastAPILimiter.redis:
        await FastAPILimiter.redis.close()
        logger.info("FastAPI-Limiter Redis client closed.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    lifespan=lifespan
)

app.include_router(api_router)


@app.exception_handler(429)
async def rate_limit_exception_handler(request: Request, exc: Exception):
    logger.warning(f"Rate limit exceeded for client: {request.client.host}")  # لاگ
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={"detail": "Rate limit exceeded. Try again in a minute."},
    )
