from backend.schemas.post import PostCreate 
from backend.core.Redis.client import get_redis
from backend.core.config import REDIS_CHANNEL_NAME


async def add_post(post_id, payload: PostCreate, telegram_user_id:str | None = None) -> str:
    r = await get_redis()
    post_key = "post:" + post_id
    
    #add to payload telegram_user_id
    payload_dict: dict = payload.model_dump()
    if telegram_user_id:
        payload_dict["telegram_user_id"] = telegram_user_id

    #add new post to redis
    await r.hset(post_key, mapping=payload_dict)

    #add new post to UNPROCESSED posts
    #   (if tg bot is alive and listening to channel, 
    #    it will immediatly remove it from UNPROCESSED)
    await r.sadd("unprocessed_posts", post_key)

    #publish new post_key to channel
    await r.publish(REDIS_CHANNEL_NAME, post_id)
    return post_key

async def remove_post(post_id: str) -> dict:
    r = await get_redis()
    post_key = "post:" + post_id
    post_data = await r.hgetall(post_key)
    await r.delete(post_key)
    return post_data

