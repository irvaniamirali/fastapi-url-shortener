from app.middleware.cors import setup_middleware_cors
from app.middleware.logging import RequestLoggingMiddleware
from app.middleware.error_handler import ExceptionHandlingMiddleware
from app.middleware.token_bucket_limiter import RedisTokenBucketLimiterMiddleware

from app.redis import redis


def add_middlewares(app) -> None:
    """
    Attach all global middlewares to the FastAPI application.
    """
    # Add CORS middleware
    setup_middleware_cors(app)

    app.add_middleware(RequestLoggingMiddleware)
    app.add_middleware(ExceptionHandlingMiddleware)
    app.add_middleware(RedisTokenBucketLimiterMiddleware, redis=redis)
