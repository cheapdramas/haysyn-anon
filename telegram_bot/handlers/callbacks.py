from aiogram import Router, Bot 
from aiogram.types import CallbackQuery
from db.crud import ModMessagesCrud, ChanellMessagesCrud
from core.api_communication import send_approved_post
from core.Redis.scripts import remove_post as redis_remove_post
from core.config import CHANNEL_NAME, WEBSITE_URL_BASE
from keyboards.inline import keyboard_link
from core.users import forward_user_posts_from_channel  

router = Router()

@router.callback_query(lambda c: c.data and c.data.startswith("approve:"))
async def approve_handler(callback: CallbackQuery, bot: Bot):
    post_id = callback.data.split(":")[1]

    api_answer = await send_approved_post(post_id)

    if api_answer:

        messages_that_waits_for_mod = await ModMessagesCrud.get(post_id)
        
        #delete messages with this post_id approve in admins chat
        for msg in messages_that_waits_for_mod:
            await bot.delete_message(chat_id=msg.admin_id, message_id=msg.message_id)
        #delete this messages from database
        await ModMessagesCrud.delete(post_id)

        await callback.answer(f"Approved ✅")

        # send post to telegram channel
        # post_url = f"{WEBSITE_URL_BASE}post/{api_answer['id']}"
        # channel_message = await bot.send_message(
        #     chat_id=CHANNEL_NAME,
        #     text=callback.message.text, 
        #     entities=callback.message.entities,
        #     reply_markup=keyboard_link(text="Посилання на пост", url=post_url)
        # )
        #
        # # if telegram_user_id is in api_answer
        # if telegram_user_id := api_answer.get("telegram_user_id"):
        #     # add message to channel messages table
        #     await ChanellMessagesCrud.add(
        #         user_id=telegram_user_id,
        #         message_id=str(channel_message.message_id)
        #     )
        #




        print(f"Approved post: {post_id}")
    else:
        await callback.answer(f"Connection with API failed 😔")


@router.callback_query(lambda c: c.data and c.data.startswith("decline:"))
async def decline_handler(callback: CallbackQuery, bot: Bot):
    post_id = callback.data.split(":")[1]

    try:
        messages_that_waits_for_mod = await ModMessagesCrud.get(post_id)
        for msg in messages_that_waits_for_mod:
            await bot.delete_message(chat_id=msg.admin_id, message_id=msg.message_id)
        await ModMessagesCrud.delete(post_id)
        
        await redis_remove_post("post:" + post_id)


        await callback.answer(f"Declined ❌")
        print(f"Declined post: {callback.data}")

    except Exception as e:
        await callback.answer(f"Problem occured 😔")
        print("Decline post error: ", str(e))


#handle continue viewing posts button 
@router.callback_query(lambda c: c.data and c.data.startswith("last_post_index:"))
async def continue_view_posts_button_handler(callback: CallbackQuery, bot: Bot):
    last_post_index = callback.data.split(":")[1]
    await forward_user_posts_from_channel(callback.message, bot, start=last_post_index, amount=10, last_post_index=int(last_post_index))

    await callback.message.delete()
    
    


