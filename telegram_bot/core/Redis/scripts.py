from core.Redis.client import get_redis
from redis import Redis
from core.config import REDIS_HOST, REDIS_PORT

class RawPost:
    "Post which just got submitted by user, unmoderated by admins"

    @staticmethod
    async def get(post_key: str) -> dict[str,str]:
        r = await get_redis()
        post = await r.hgetall(post_key)
        return post
    @staticmethod
    async def remove(post_key: str):
        r = await get_redis()
        await r.delete(post_key)

class UnprocessedPosts:
    "Posts that admins have not seen"
    key = "unprocessed_posts"

    @classmethod
    async def get_data(cls) -> list[dict[str,str]]:
        r = await get_redis()
        unproc_post_keys = await r.smembers(cls.key)
        unproc_posts_data = []
        for i in unproc_post_keys:
            post_data = await r.hgetall(i)
            post_data["id"] = i.split(":")[1]
            unproc_posts_data.append(post_data)
        return unproc_posts_data

    @classmethod
    async def length(cls) -> int:
        r = await get_redis()
        # get unprocessed_posts length
        unproc_len = await r.scard(cls.key)
        return unproc_len 

    @classmethod
    async def remove(cls, post_key: str):
        r = await get_redis()
        await r.srem(cls.key, post_key)



class UnsentTgChannelPosts:
    "Posts that need to be sent in telegram channel"
    key = "unsent_tg_channel_posts"

    @classmethod
    async def get(cls) -> set[str]:
        r = await get_redis()
        unsent_tg_channel_posts = await r.smembers(cls.key)
        return unsent_tg_channel_posts 

    @classmethod
    async def length(cls) -> int:
        r = await get_redis()
        res = await r.scard(cls.key)
        return res 

    @classmethod
    async def remove(cls, post_id: str):
        r = await get_redis()
        await r.srem(cls.key, post_id)
                     
