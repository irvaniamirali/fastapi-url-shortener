from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from app.errors import ErrorCode, error_messages


async def custom_http_exception_handler(request: Request, exc: HTTPException, headers=None) -> JSONResponse:
    error_code = exc.detail if isinstance(exc.detail, ErrorCode) else "unknown_error"
    message = error_messages.get(error_code, str(exc.detail))

    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_code.value,
            "message": message
        },
        headers=headers
    )
