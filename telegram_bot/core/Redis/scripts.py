from core.Redis.client import get_redis

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
    return unproc_posts_data

async def remove_unprocessed_post(post_key: str):
    r = await get_redis()
    await r.srem("unprocessed_posts", post_key)


async def remove_post(post_key: str):
    r = await get_redis()
    await r.delete(post_key)
