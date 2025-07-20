"""
	HTML Endpoints
"""

from fastapi import APIRouter
from .index import router as index_router
from .post import router as posts_router
from fastapi.templating import Jinja2Templates
from pathlib import Path

router = APIRouter()
router.include_router(index_router)
router.include_router(posts_router)

