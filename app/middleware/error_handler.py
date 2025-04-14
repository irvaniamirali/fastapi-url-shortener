import logging
import traceback
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

logger = logging.getLogger("uvicorn.error")

class ExceptionHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        try:
            response = await call_next(request)
            return response

        except RequestValidationError as e:
            logger.warning(f"Validation error: {e.errors()}")
            return JSONResponse(
                status_code=422,
                content={
                    "detail": "Invalid request parameters",
                    "errors": e.errors(),
                },
            )

        except StarletteHTTPException as e:
            logger.warning(f"HTTP error: {e.detail}")
            return JSONResponse(
                status_code=e.status_code,
                content={"detail": e.detail},
            )

        except Exception as e:
            # Log full traceback
            logger.error(f"Unhandled error: {str(e)}")
            logger.debug(traceback.format_exc())

            return JSONResponse(
                status_code=500,
                content={"detail": "Internal Server Error. Please try again later."},
            )
