from backend.schemas.post import PostCreate 
from backend.core.Redis.client import get_redis
from backend.core.config import REDIS_CHANNEL_NAME
from backend.core.auth import anonymize_user_id


async def add_post(post_id, payload: PostCreate) -> str:
    r = await get_redis()
    post_key = "post:" + post_id
    
    payload_dict: dict = payload.model_dump()
    if tg_user_id := payload_dict.get("telegram_user_id"):
        print(f"sykkakaaaaaaa {tg_user_id}")
        payload_dict["telegram_user_id"] = anonymize_user_id(tg_user_id)
    else:
        payload_dict.pop("telegram_user_id")
    print(payload_dict)

    #add new post to redis
    await r.hset(post_key, mapping=payload_dict)

    #add new post to UNPROCESSED posts
    #   (if tg bot is alive and listening to channel, 
    #    it will immediatly remove it from UNPROCESSED)
    await r.sadd("unprocessed_posts", post_key)

    #publish new post_key to channel
    await r.publish(REDIS_CHANNEL_NAME, f"new_post:{post_id}")
    
    return post_key


async def remove_post(post_id: str) -> dict:
    r = await get_redis()
    post_key = "post:" + post_id
    post_data = await r.hgetall(post_key)
    await r.delete(post_key)
    return post_data

async def publish_post_in_channel(prefix: str, post_id: int):
    r = await get_redis()

    await r.sadd("unsent_tg_channel_posts", str(post_id))
    await r.publish(REDIS_CHANNEL_NAME, f"{prefix}:{post_id}")


