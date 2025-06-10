import aioredis
from .config import REDIS_URL

redis: aioredis.Redis | None = None

async def init_redis() -> None:
    global redis
    redis = aioredis.from_url(REDIS_URL)

async def close_redis() -> None:
    if redis is not None:
        await redis.close()
