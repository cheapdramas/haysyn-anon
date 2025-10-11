from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from core.config import ADMINS

import asyncio

router = Router()

@router.message(Command("mod"))
async def start_mod(message: Message):
    user_id = str(message.chat.id)
    
    if user_id in ADMINS:
        pass
    else:
        await message.answer("Ти не адмiн братiшка")

@router.message(Command("stop_mod"))
async def stop_mod(message: Message):
    user_id = str(message.chat.id)
    if user_id not in ADMINS:
        await message.answer("Ти не адмiн братiшка")
        return

    
        
