import aiohttp
from schemas.post import Post 
from core.config import WEBSITE_API_URL

async def send_approved_post(post_data: Post):
   async with aiohttp.ClientSession() as session:
       await session.post(WEBSITE_API_URL + 'post', json = post_data.model_dump())

