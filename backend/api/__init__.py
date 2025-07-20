"""
	API endpoints for CRUD
"""

from fastapi import APIRouter
from .api_v1 import router as v1_router

router = APIRouter()
router.include_router(v1_router,prefix="/api_v1")