from fastapi import APIRouter, WebSocket
from backend.core.auth import verify_token 
from backend.core.config import ADMINS
from backend.schemas.post import PostBase, PostInRedis 

import backend.core.Redis.scripts as redis_scripts


#admin_id: websocket
ws_connections: dict[str, WebSocket] = {}

async def send_to_admins(posts: list[PostInRedis]):
    # translate PostInRedis into dict
    for i in range(len(posts)):
        posts[i] = posts[i].model_dump()


    #to hold disconnected/connections where error occured
    disconnected = []
    
    for admin_id, ws in ws_connections.items():
        try:
            await ws.send_json(posts)
        except Exception as e:
            disconnected.append(admin_id)
    
    for admin_id in disconnected:
        popped = ws_connections.pop(admin_id, "Key not found")
