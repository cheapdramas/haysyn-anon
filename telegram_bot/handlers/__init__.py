from aiogram import Router
from handlers.start import router as router_start
from handlers.moderation import router as router_mod
from handlers.token import router as router_token
from handlers.callbacks import router as callbacks_router

router = Router()

router.include_router(router_start)
router.include_router(router_mod)
router.include_router(router_token)
router.include_router(callbacks_router)
