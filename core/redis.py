import redis.asyncio as redis
from .config import REDIS_URL

redis_client: redis.Redis | None = None

async def init_redis() -> None:
    global redis_client
    redis_client = redis.from_url(REDIS_URL)

async def close_redis() -> None:
    if redis_client is not None:
        await redis_client.close()
