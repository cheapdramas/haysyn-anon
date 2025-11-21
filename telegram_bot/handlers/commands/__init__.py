from aiogram import Router
from .base_commands import router as base_commands_router
from .post_commands import router as post_commands_router

router = Router()

router.include_router(base_commands_router)
router.include_router(post_commands_router)
