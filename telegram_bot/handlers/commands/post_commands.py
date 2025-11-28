from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp, keyboard_continue_viewing_posts
from core.config import CHANNEL_ID, WEBSITE_URL_BASE, ADMINS
from db.crud import ChanellMessagesCrud
from core.users import forward_user_posts_from_channel

router = Router()

@router.message(Command("myposts"))
async def myposts_command_handler(message: Message, bot: Bot) -> None:
    await forward_user_posts_from_channel(message, bot, amount=10, start=0)
