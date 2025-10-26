from aiogram import Bot
from core.Redis.scripts import get_unprocessed_posts_data, remove_unprocessed_post
from core.config import ADMINS
from core.messages import mod_message
from db.mod_messages_crud import ModMessagesCrud
from keyboards.inline import keyboard_mod

async def send_unprocessed_posts(bot: Bot):
    try:
        for admin_id in ADMINS:
            unprocessed_posts = await get_unprocessed_posts_data()

            for post in unprocessed_posts:
                msg = mod_message(post)
                keyboard = keyboard_mod(post["id"])

                msg_sent = await bot.send_message(
                    text=msg,
                    chat_id=admin_id,
                    reply_markup=keyboard,
                    parse_mode="HTML"
                )
                await ModMessagesCrud.add(
                    message_id=msg_sent.message_id,
                    admin_id=admin_id,
                    post_id=post["id"]
                )
                await remove_unprocessed_post("post:" + post["id"])

    except Exception as e:
        print(f"Error in send_unprocessed_posts: ",str(e)) 
   




