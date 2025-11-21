import aiohttp
from core.config import WEBSITE_URL_BASE, API_VERSION
from core.auth import create_jwt

async def send_approved_post(post_id: str) -> any:
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
