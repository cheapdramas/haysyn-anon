from aiogram.types import InlineKeyboardMarkup
from core.config import WEBSITE_URL_BASE, CHANNEL_NAME
from aiogram import Bot
from db.crud import ChanellMessagesCrud

# send post to telegram channel
async def send_message_to_channel(post_id: str, user_id: str | None, bot: Bot, message: str, reply_markup: InlineKeyboardMarkup):
    channel_message = await bot.send_message(
        chat_id=CHANNEL_NAME,
        text=message,
        reply_markup=reply_markup,
        parse_mode="HTML"
    )

    # add message to channel messages table
    await ChanellMessagesCrud.add(
        post_id=post_id,
        user_id=user_id,
        message_id=str(channel_message.message_id)
    )


