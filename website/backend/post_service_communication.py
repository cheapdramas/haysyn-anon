import aiohttp
from schemas.post import Post 

async def post_service_send_post(post_data: Post):
   async with aiohttp.ClientSession() as session:
       await session.post(WEBSITE_API_URL + 'post', json = post_data.model_dump())

