from backend.core import websockets_control
from fastapi import APIRouter
from .post import router as post_router
from .comment import router as comment_router 
from .ws import router as websocket_router 

router = APIRouter()
router.include_router(post_router)
router.include_router(comment_router) 
router.include_router(websocket_router) 
