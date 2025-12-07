from aiogram import Router
from .anon_message import router as anon_message_router

router = Router()
router.include_router(anon_message_router)
