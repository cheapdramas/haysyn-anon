import redis.asyncio as redis
from core.config import REDIS_HOST, REDIS_PORT

r: redis.Redis | None = None

async def init_redis() -> redis.Redis:
    global r
    if r is None:
        r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
    return r

def get_redis() -> redis.Redis:
    global r
    if r is None:
        raise RuntimeError("Redis not initialized. Did you forget app startup event?")
    return r

async def close_redis():
    global r
    if r is not None:
        await r.close()
        r = None

