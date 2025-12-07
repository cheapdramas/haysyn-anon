from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp, keyboard_continue_viewing_posts
from core.config import CHANNEL_ID, WEBSITE_URL_BASE, ADMINS, MAX_POSTS_AMOUNT_TO_USER 
from db.crud import ChanellMessagesCrud
from core.users import myposts
from keyboards.reply import buttons as reply_buttons
import asyncio

router = Router()

@router.message(Command("myposts"))
@router.message(F.text == reply_buttons["myposts"])
# @router.callback_query(lambda c: c.data and c.data.startswith("continue_viewing_posts_channel"))
async def myposts_command_handler(message: Message, bot: Bot) -> None:
    asyncio.create_task(
        myposts(
            message=message, 
            bot=bot, 
            offset=0,
            limit=MAX_POSTS_AMOUNT_TO_USER,
            load_from_website=False
        )
    )


