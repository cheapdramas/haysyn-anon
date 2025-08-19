import aiohttp
from backend.schemas.post import PostBase
from backend.core.config import POST_SERVICE_URL 

async def post_service_send_post(post_data: PostBase, token: str):
    headers = {
        "Authorization": f"Bearer {token}"
    }
    async with aiohttp.ClientSession() as session:
        await session.post(
            POST_SERVICE_URL + 'post',
            json=post_data.model_dump(),
            headers=headers
        )
