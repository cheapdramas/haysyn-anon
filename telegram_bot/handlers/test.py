from asyncio import start_server
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp
from core.messages import mod_message
from aiogram import Router, Bot 
from aiogram.types import CallbackQuery
from schemas.post import PostModStatus as status
from keyboards.inline import keyboard_mod
from db.mod_messages_crud import ModMessagesCrud 
from core.config import ADMINS
from random import randint 

router = Router()

@router.message(Command("add_post"))
async def test_handler(message: Message,bot: Bot) -> None:
    user_id = str(message.chat.id)
    if user_id not in ADMINS:
        return 
    post_id = str(randint(2,500))

    post = {
        "title": "Nevermind",
        "text": "it doesn't matter"
    }
    msg = mod_message(post)
    keyboard = keyboard_mod(post_id)

    msg_sent = await message.answer(msg,reply_markup=keyboard, parse_mode="HTML")

    added_to_db = await ModMessagesCrud.add(
        message_id=msg_sent.message_id,
        admin_id=user_id,
        post_id=post_id
    )

    print("TEST: ADDED POST TO DB: ", added_to_db)
