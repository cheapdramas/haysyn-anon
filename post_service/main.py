from fastapi import FastAPI, Depends, WebSocket
from contextlib import asynccontextmanager
from core.auth import verify_token, verify_token_depends, id_generator
from schemas.post import Post , PostSend
from core.websockets_control import router as ws_router, send_to_admins, ws_connections

import Redis.scripts as redis_scripts
import Redis.client as redis_client
import uvicorn

app = FastAPI()
app.include_router(ws_router)


@app.on_event("startup")
async def on_startup():
    await redis_client.init_redis()

@app.on_event("shutdown")
async def on_shutdown():
    await redis_client.close_redis()


@app.get("/")
async def test(token: str = Depends(verify_token_depends("bot"))):
    return "hello"


@app.post("/post")
async def add_post(post: Post, token: str = Depends(verify_token_depends("website"))):
    post_id = str(next(id_generator))

    await send_to_admins([PostSend(id=post_id,**post.model_dump())])

    seen_by=list(ws_connections.keys())
    await redis_scripts.add_post(post_id, post, seen_by)

    print(ws_connections)

    return post_id 


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0",port = 8001)
