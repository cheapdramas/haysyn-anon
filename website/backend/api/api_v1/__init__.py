from fastapi import APIRouter
from .post import router as post_router
from .comment import router as comment_router 

router = APIRouter()
router.include_router(post_router)
router.include_router(comment_router) 
