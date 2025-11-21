from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp
from core.config import CHANNEL_ID, WEBSITE_URL_BASE
from db.crud import ChanellMessagesCrud

router = Router()

@router.message(Command("myposts"))
async def myposts_commands_handler(message: Message, bot: Bot) -> None:
    user_id = message.chat.id

    posts = await ChanellMessagesCrud.get(str(user_id))
    if posts == []:
        await message.answer(text="❌Ти ще не написав жодного посту❌\n\n⬇",reply_markup=keyboard_webapp(text="Написати пост",url=WEBSITE_URL_BASE))
        return

    await bot.forward_messages(
        chat_id=message.chat.id,
        from_chat_id=CHANNEL_ID,
        message_ids=[i.message_id for i in posts]
    )


