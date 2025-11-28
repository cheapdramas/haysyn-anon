import aiohttp
from core.config import WEBSITE_URL_BASE, API_VERSION
from core.auth import anonymize_user_id, create_jwt

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

async def get_post(post_id: str) -> None | dict:
    url = f"{WEBSITE_URL_BASE}{API_VERSION}post?id={post_id}"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            if resp.status == 200:
                return await resp.json()
        return None 
    except Exception:
        return None 

async def get_posts_by_tg_user_id(telegram_user_id: str) -> None | dict:
    url = f"{WEBSITE_URL_BASE}{API_VERSION}posts_by_tg_user_id?telegram_user_id={anonymize_user_id(telegram_user_id)}"
    try:
        async with aiohttp.ClientSession() as session:
            resp = await session.get(url)
            if resp.status == 200:
                return await resp.json()
        return None 
    except Exception:
        return None 
