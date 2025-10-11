from core.Redis.client import get_redis

async def get_post(post_key: str) -> dict[str,str]:
    r = await get_redis()
    post = await r.hgetall(post_key)
    return post

async def remove_post(post_id: str):
    r = await get_redis()
    post_key = "post:" + post_id
    await r.delete(post_key)
