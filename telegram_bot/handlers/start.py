from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp
from core.config import ADMINS 
from core.Redis.pubsub import listen_to_redis
import asyncio


router = Router()

#keeping admins_started
admins_started = []

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    user_id = str(message.chat.id)
    if user_id in ADMINS:
        if user_id not in admins_started:
            admins_started.append(user_id)
            asyncio.create_task(listen_to_redis(user_id,message))


    

    await message.answer("Hello! I'm a bot created with aiogram.")
