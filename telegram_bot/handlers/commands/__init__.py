from aiogram import Router
from .basic import router as base_commands_router
from .post import router as post_commands_router
from .anon_message import router as message_commands_router

router = Router()

router.include_router(base_commands_router)
router.include_router(post_commands_router)
router.include_router(message_commands_router)
