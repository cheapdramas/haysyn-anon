from core.Redis.client import get_redis
from redis import Redis
from core.config import REDIS_HOST, REDIS_PORT

async def get_post(post_key: str) -> dict[str,str]:
    r = await get_redis()
    post = await r.hgetall(post_key)
    return post

async def get_unprocessed_posts_data() -> list[dict[str,str]]:
    r = await get_redis()
    unproc_post_keys = await r.smembers("unprocessed_posts")
    unproc_posts_data = []
    for i in unproc_post_keys:
        post_data = await r.hgetall(i)
        post_data["id"] = i.split(":")[1]
        unproc_posts_data.append(post_data)
    print("unproc_post_data: ", unproc_posts_data)
    return unproc_posts_data

async def check_unprocessed_posts_len() -> int:
    r = await get_redis()
    # get unprocessed_posts length
    unproc_len = await r.scard("unprocessed_posts")
    return unproc_len 

async def remove_unprocessed_post(post_key: str):
    r = await get_redis()
    await r.srem("unprocessed_posts", post_key)


async def remove_post(post_key: str):
    r = await get_redis()
    await r.delete(post_key)
