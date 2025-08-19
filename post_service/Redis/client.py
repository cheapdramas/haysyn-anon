import redis.asyncio as redis
from core.config import ADMINS

r: redis.Redis | None = None

async def init_redis() -> redis.Redis:
    global r
    if r is None:
        r = redis.Redis(host="localhost", port=6379, decode_responses=True)
        await r.flushdb()
        await r.sadd("admins", *ADMINS)
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
