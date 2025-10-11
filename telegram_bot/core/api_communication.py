import aiohttp
from core.config import WEBSITE_URL_API 
from core.auth import create_jwt

async def send_approved_post(post_id: str):
    token = create_jwt()
    url = f"{WEBSITE_URL_API}post?post_id={post_id}" 
    headers = {
        "accept": "application/json",
        "Authorization": f"Bearer {token}"
    }

    async with aiohttp.ClientSession() as session:
        await session.post(url, headers=headers)
