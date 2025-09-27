from fastapi import APIRouter, WebSocket
from backend.core.auth import verify_token 
from backend.core.config import ADMINS
from backend.schemas.post import PostCreate, PostInRedis, WSPostModerate
from backend.core.websockets_control import ws_connections
from backend.db.crud import PostCrud
from backend.db.utils import db_helper 

import backend.core.Redis.scripts as redis_scripts

router = APIRouter()

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    token = websocket.query_params.get("token")
    admin_id = websocket.query_params.get("admin_id")

    if not token or admin_id not in ADMINS or admin_id in ws_connections:
        await websocket.close(code=1008)
        return
    verify_token(token, "bot")

    await websocket.accept()
    ws_connections[admin_id]=websocket

    try:
        # send unseen posts
        unseen_posts = await redis_scripts.get_admin_unseen_posts(admin_id)
        if unseen_posts != []:
            for post in unseen_posts:
                await websocket.send_json([post])
            await redis_scripts.clear_admin_unseen_posts(admin_id)
        while True:
            #verify token
            try:
                verify_token(token, "bot")
            except Exception as e:
                ws_connections.pop(admin_id)
                await websocket.close(code=1008)
            
            #{"post_id": str, "status": "decline/approve"}
            got_data = WSPostModerate(**await websocket.receive_json())
            post_id = got_data.post_id
            status = got_data.status.value

            post_data = await redis_scripts.remove_post(post_id)
            if status == "approved" and post_data != {}:
                #add post to database
                with db_helper.session_factory() as session:
                    PostCrud.create_post(PostCreate(**post_data), session)
                    
    except Exception as e:
        print("Error occurred in websocket work: ", str(e))
        ws_connections.pop(admin_id)
