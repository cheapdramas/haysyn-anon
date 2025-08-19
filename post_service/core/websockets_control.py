from fastapi import APIRouter, WebSocket
from core.auth import verify_token 
from core.config import ADMINS
from schemas.post import Post , PostSend
from core.website_communication import send_approved_post

import Redis.scripts as redis_scripts


router = APIRouter()

#admin_id: websocket
ws_connections: dict[str, WebSocket] = {}

async def send_to_admins(posts: list[PostSend]):
    # translate PostSend into dict
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
            await websocket.send_json(unseen_posts)
            await redis_scripts.clear_admin_unseen_posts(admin_id)
        while True:
            #verify token
            try:
                verify_token(token, "bot")
            except Exception as e:
                ws_connections.pop(admin_id)
                await websocket.close(code=1008)
            
            #{"post_id": str, "status": "decline/approve"}
            got_data = await websocket.receive_json()
            post_id = got_data["post_id"]
            status = got_data["status"]

            # Handle post approve or decline
            if status == "decline" or status == "approved":
                post_data = await redis_scripts.remove_post(post_id)

                if status == "approved":
                    # send POST request with post data to main service API /post
                    print(post_data)
                    post_send = Post(**post_data)
                    await send_approved_post(post_send)

    except Exception as e:
        print("Error occurred in websocket work: ", str(e))
        ws_connections.pop(admin_id)




