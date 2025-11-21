from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp
from core.config import WEBSITE_URL_BASE 
from utils.set_commands import set_commands

router = Router()

@router.message(Command("start"))
async def myposts_command_handler(message: Message, bot: Bot) -> None:
    user_id = str(message.chat.id)
    await bot.set_chat_menu_button(
        chat_id= int(user_id),
        menu_button = {
            "type": "web_app",
            "text": "Anon",
            "web_app": {"url":WEBSITE_URL_BASE} 
        }
    )

    # await set_commands(bot)

    await message.answer("Братік залітай ❤️",reply_markup=keyboard_webapp(text="Anon",url=WEBSITE_URL_BASE))
