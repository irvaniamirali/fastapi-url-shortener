from configs import settings

from redis.asyncio import Redis

redis = Redis(host=settings.redis_host, port=settings.redis_port, decode_responses=True)
