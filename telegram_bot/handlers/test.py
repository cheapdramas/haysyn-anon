from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp
from core.config import WEBSITE_URL_BASE 
from core.auth import create_jwt

router = Router()

@router.message(Command("token"))
async def give_token(message: Message, bot: Bot) -> None:
    await message.answer(create_jwt())
