from aiogram import Bot
from core.Redis.scripts import get_unprocessed_posts_data, remove_unprocessed_post, check_unprocessed_posts_len
from core.config import ADMINS
from core.messages import mod_message
from db.crud import ModMessagesCrud
from keyboards.inline import keyboard_mod
import asyncio

async def send_unprocessed_posts(bot: Bot):
    
    # while loop, to resend unprocessed posts if flood error appiers
    while await check_unprocessed_posts_len() > 0:

        # let the other tasks to start working
        await asyncio.sleep(0)

        try:

            unprocessed_posts = await get_unprocessed_posts_data()
            print(len(unprocessed_posts))

            for post in unprocessed_posts:
                print(post)
                msg = mod_message(post)
                keyboard = keyboard_mod(post["id"])

                for admin_id in ADMINS:
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
   
async def send_post_to_admin(admin_id: str, bot: Bot):
    pass 




