from aiogram import Bot
from aiogram.types import Message
from core.api_communication import get_posts_by_tg_user_id
from keyboards.inline import keyboard_link, keyboard_webapp, keyboard_continue_viewing_posts
from core.config import CHANNEL_ID, WEBSITE_URL_BASE
from db.crud import ChanellMessagesCrud
from core.auth import  anonymize_user_id
from core.messages import mod_message


async def forward_user_posts_from_channel(message: Message , bot: Bot, start: int = 0, amount: int = 10, last_post_index:int = 0) -> None:
    user_id = message.chat.id
    anon_user_id = anonymize_user_id(str(user_id))
    print(start)

    posts_channel = await ChanellMessagesCrud.get(anon_user_id, start=start, amount = amount)
    print(posts_channel)
    if posts_channel == []:
        if last_post_index:   # means that function was called from continue watching posts callback
            # parse posts from api
            posts_api = await get_posts_by_tg_user_id(str(user_id)) # ALL posts from user
            # get all chanell posts from user for comparison
            for post in posts_api:
                if not await ChanellMessagesCrud.get(post_id=post['id'], start=None, amount = None):
                    msg = mod_message(post)
                    await message.answer(text=msg, reply_markup=keyboard_link(text="Посилання на пост",url=f"{WEBSITE_URL_BASE}post/{post['id']}"), parse_mode="HTML")
            
            await message.answer(text="❌ Кінець твоїх постів ")


        else:
            await message.answer(text="❌Ти ще не написав жодного посту❌\n\n⬇",reply_markup=keyboard_webapp(text="Написати пост",url=WEBSITE_URL_BASE))
        return
    try:    
        #forward posts from channel to user
        await bot.forward_messages(
            chat_id=user_id,
            from_chat_id=CHANNEL_ID,
            message_ids=[i.message_id for i in posts_channel]
        )

        #send message to continue viewing posts
        await bot.send_message(
            chat_id=user_id,
            text="Продовжити дивитись пости?",
            reply_markup=keyboard_continue_viewing_posts(last_post_index + len(posts_channel))
        )
        
        
    except:
        print(f"Post forwarding failed for {user_id}")



