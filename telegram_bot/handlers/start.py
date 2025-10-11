from aiogram import Router, Bot
from aiogram.filters import Command
from aiogram.types import Message
from core.messages import mod_message
from keyboards.inline import keyboard_mod, keyboard_webapp
from core.config import ADMINS 
from core.Redis.pubsub import listen_to_redis
from core.Redis.scripts import get_unprocessed_posts_data, remove_unprocessed_post
from db.mod_messages_crud import ModMessagesCrud
import asyncio


router = Router()

#keeping admins_started
admins_started = []

@router.message(Command("start"))
async def command_start_handler(message: Message, bot: Bot) -> None:
    user_id = str(message.chat.id)
    # Устанавливаем кнопку WebApp в меню бота
    await bot.set_chat_menu_button(
        chat_id=int(user_id),
        menu_button={
            "type": "web_app",
            "text": "Anon",
            "web_app": {"url": "https://extracapsular-earline-perspectiveless.ngrok-free.dev/"} 
        }
    )



    
    try: 
        if user_id in ADMINS:
            if user_id not in admins_started:
                admins_started.append(user_id)
                
                #send unprocessed posts
                unprocessed_posts = await get_unprocessed_posts_data()
                for post_data in unprocessed_posts:
                    post_id = post_data["id"]

                    msg = mod_message(post_data)
                    keyboard = keyboard_mod(post_id)

                    msg_sent = await message.answer(msg,reply_markup=keyboard, parse_mode="HTML")
                    
                    # add new message to database
                    await ModMessagesCrud.add(
                        message_id=msg_sent.message_id,
                        admin_id=user_id,
                        post_id=post_id
                    )

                    await remove_unprocessed_post("post:" + post_id)



                asyncio.create_task(listen_to_redis(user_id,message))
    except Exception as e:
        print("Start error occured!", str(e))

    await message.answer("Братік залітай ❤️",reply_markup=keyboard_webapp())
