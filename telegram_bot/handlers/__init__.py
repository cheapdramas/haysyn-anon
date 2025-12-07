from aiogram import Router
from handlers.callbacks import router as callbacks_router
from .commands import router as commands_router
from handlers.states import router as states_router

router = Router()

router.include_router(callbacks_router)
router.include_router(commands_router)
router.include_router(states_router)
