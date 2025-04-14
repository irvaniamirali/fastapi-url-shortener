import time
from typing import Optional
from redis.asyncio import Redis
from fastapi import status
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from jose import jwt, JWTError
from starlette.responses import JSONResponse

from configs import settings


class RedisTokenBucketLimiterMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, redis: Redis):
        super().__init__(app)
        self.redis = redis
        self.max_tokens = settings.max_tokens
        self.refill_rate = settings.refill_rate_per_second

    async def dispatch(self, request: Request, call_next):
        identifier = await self._get_identifier(request)

        allowed = await self._allow_request(identifier)
        if not allowed:
            return JSONResponse(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                content={
                    "error": "rate_limit_exceeded",
                    "message": "Rate limit exceeded. Please try again later."
                }
            )

        return await call_next(request)

    async def _get_identifier(self, request: Request) -> str:
        token = self._extract_token(request)
        if token:
            try:
                payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
                user_id = payload.get("sub")
                if user_id:
                    return f"user:{user_id}"
            except JWTError:
                pass
        return f"ip:{request.client.host}"

    def _extract_token(self, request: Request) -> Optional[str]:
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.lower().startswith("bearer "):
            return auth_header[7:]
        return None

    async def _allow_request(self, identifier: str) -> bool:
        key = f"bucket:{identifier}"
        now = time.time()
        pipe = self.redis.pipeline()
        await pipe.hgetall(key)
        result = await pipe.execute()
        data = result[0] or {}

        tokens = float(data.get("tokens", self.max_tokens))
        last_refill = float(data.get("last_refill", now))
        elapsed = now - last_refill
        refill_amount = elapsed * self.refill_rate

        tokens = min(self.max_tokens, tokens + refill_amount)
        allowed = tokens >= 1
        if allowed:
            tokens -= 1

        await self.redis.hset(
            key, mapping={
                "tokens": tokens,
                "last_refill": now
            }
        )
        return allowed
