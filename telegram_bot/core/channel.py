from aiogram import Bot
from aiogram.types import InlineKeyboardMarkup, Message
from core.Redis.scripts import UnprocessedPosts, UnsentTgChannelPosts 
from core.config import WEBSITE_URL_BASE, CHANNEL_NAME
from db.crud import ChanellMessagesCrud
from core.api_communication import api_get_post, api_set_post_in_tg_channel
from core.messages import message_post_format
from keyboards.inline import keyboard_link 
import asyncio

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

async def send_post_to_channel(post_id: str, bot: Bot) -> bool:
    # if this post is not published
    if await ChanellMessagesCrud.get(post_id=post_id) == []:
        try:
            print("POST_ID:", post_id)

            # make a request to api to get post data
            post_data = await api_get_post(post_id)
            if not post_data:
                return False

            msg = message_post_format(post_data) 
            keyboard = keyboard_link(text="Посилання на пост",url=f"{WEBSITE_URL_BASE}post/{post_id}")
            await send_message_to_channel(post_id ,post_data.get("telegram_user_id"), bot, msg, keyboard)
            
            # send a PATCH request to api to confirm that post was published
            await api_set_post_in_tg_channel(post_id, True)

            await UnsentTgChannelPosts.remove(post_id)


        except Exception as e:
            print(f"Failed to send post to telegram channel (sent_post_to_channel): ", str(e))
            return False

    return True



async def send_unsent_tg_posts_to_channel(bot: Bot):
    print(await UnsentTgChannelPosts.length())
    while await UnsentTgChannelPosts.length() > 0:
    
        await asyncio.sleep(0)

        try:
            posts_ids = await UnsentTgChannelPosts.get()
            
            print("post_ids: ", posts_ids)
            for post_id in posts_ids:
                sent_post = await send_post_to_channel(post_id, bot) 
                if not sent_post:
                    return
                
        except Exception as e:
            print("Error occured in send_unsent_tg_posts_to_channel: ", str(e))
            pass
