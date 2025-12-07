import aiohttp
from core.config import WEBSITE_URL_BASE, API_VERSION
from core.auth import anonymize_user_id, create_jwt
import json

async def send_approved_post(post_id: str) -> None | dict:
    token = create_jwt()
    url = f"{WEBSITE_URL_BASE}{API_VERSION}post?post_id={post_id}" 
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(url, headers=headers)
            if resp.status == 200:
                return await resp.json()
        return None 
    except Exception:
        return None 

async def api_get_post(post_id: str) -> None | dict:
    url = f"{WEBSITE_URL_BASE}{API_VERSION}post?id={post_id}"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            if resp.status == 200:
                return await resp.json()
        return None 
    except Exception:
        return None 

async def api_get_posts(
    telegram_user_id: str,
    offset: int, 
    limit: int, 
    exclude: list[int] | list,
    in_tg_channel: bool | None = None
) -> list[dict] | list:
    url = f"{WEBSITE_URL_BASE}{API_VERSION}posts"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.post(url, json={"telegram_user_id":telegram_user_id, "offset": offset, "limit": limit, "exclude": exclude, "sort_by":"old", "in_tg_channel":in_tg_channel})
            print("MAKING REQUEST")
            if resp.status == 200:
                return await resp.json()
        return []
    except Exception:
        return []


async def api_set_post_in_tg_channel(
    post_id: int | str,
    set_to: bool
) -> bool:
    url = f"{WEBSITE_URL_BASE}{API_VERSION}post_in_tg_channel?post_id={post_id}&set_to={set_to}"
    token = create_jwt()
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.patch(url, headers=headers)
            if resp.status != 200:
                return False

    except Exception:
        return False 


    return True
