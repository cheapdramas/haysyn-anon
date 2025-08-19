from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from core.config import ADMINS
from core.websocket_client import websocket_client, ws_tasks

import asyncio

router = Router()

@router.message(Command("mod"))
async def start_mod(message: Message):
    user_id = str(message.chat.id)
    
    if ws_tasks.get(user_id, None):
        await message.answer("Ти вже під'єднаний до вебсокету")
        return
    
    if user_id in ADMINS:
        await message.answer("Під'єднуюсь до вебсокету...")
        task = asyncio.create_task(websocket_client(user_id,message))
        ws_tasks[user_id] = {"task":task}
    else:
        await message.answer("Ти не адмiн братiшка")

@router.message(Command("stop_mod"))
async def stop_mod(message: Message):
    user_id = str(message.chat.id)
    if user_id not in ADMINS:
        await message.answer("Ти не адмiн братiшка")
        return

    
        
    task = ws_tasks.get(user_id,{}).get("task")
    if task:
        task.cancel()  
        ws_tasks.pop(user_id, None)
    else:
        await message.answer("❌ Немає активного вебсокет під'єднання")
