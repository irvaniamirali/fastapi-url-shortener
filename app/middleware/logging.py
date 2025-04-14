import time
import os
import logging
from logging.handlers import RotatingFileHandler
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# Configure the logger with rotation
logger = logging.getLogger("app.request")
logger.setLevel(logging.INFO)

# RotatingFileHandler: Automatically rotates log files when size exceeds 20MB.
handler = RotatingFileHandler(
    "logs/app.log", maxBytes=20 * 1024 * 1024, backupCount=10
)
handler.setFormatter(logging.Formatter("%(asctime)s | %(levelname)s | %(message)s"))
logger.addHandler(handler)

class RequestLoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response: Response = await call_next(request)
        process_time = (time.time() - start_time) * 1000

        user_id = request.headers.get("user_id", "anonymous")
        logger.info(
            f"{request.method} {request.url} | "
            f"Status: {response.status_code} | "
            f"User: {user_id} | "
            f"Time: {process_time:.2f} ms"
        )
        return response
