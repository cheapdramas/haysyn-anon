from typing import Tuple
from schemas.post import Post, PostSend
from core.config import ADMINS
from core.auth import id_generator
from Redis.client import get_redis

import asyncio
import redis.asyncio as redis



async def get_admins() -> set[str]:
    r = await get_redis()
    return await r.smembers("admins")

async def get_admin_unseen_posts(admin_id:str) -> list[dict]:
    r = await get_redis()
    result = []
    unseen_post_keys = await r.smembers(f"admin_unseen:{admin_id}")
    
    for post_key in unseen_post_keys:
        post_data = await r.hgetall(post_key)
        post_data["id"] = post_key.split(":")[1]
        print("Post data:", post_data)
        result.append(post_data)
    return result

async def clear_admin_unseen_posts(admin_id: str) -> None:
    r = await get_redis()
    await r.delete(f"admin_unseen:{admin_id}")

async def add_post(post_id, payload: Post, seen_by:list[str] | list) -> str:
    payload = payload.model_dump()
    post_key = "post:" + post_id
    

    r = await get_redis()
    await r.hset(post_key, mapping=payload)

    all_admins = await get_admins()
    
    for admin_id in all_admins:
        if admin_id not in seen_by:
            # this admin did not saw the post
            await r.sadd(f"admin_unseen:{admin_id}", post_key)


async def remove_post(post_id: str) -> dict:
    r = await get_redis()

    post_key = "post:" + post_id
    post_data = await r.hgetall(post_key)

    await r.delete(post_key)

    all_admins = await get_admins()
    for admin_id in all_admins:
        await r.srem(f"admin_unseen:{admin_id}", post_key)
    return post_data



