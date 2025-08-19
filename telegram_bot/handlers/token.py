from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from core.auth import create_jwt

router = Router()

@router.message(Command("token"))
async def command_token_handler(message: Message) -> None:
    token1 = create_jwt("bot")
    token2 = create_jwt("website")
    await message.answer(f"{token1}")
    await message.answer(f"{token2}")
