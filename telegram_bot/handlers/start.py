from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp

router = Router()

@router.message(Command("start"))
async def command_start_handler(message: Message) -> None:
    # await message.answer("Hello! I'm a bot created with aiogram.", reply_markup=keyboard_webapp())
    await message.answer("Hello! I'm a bot created with aiogram.")
