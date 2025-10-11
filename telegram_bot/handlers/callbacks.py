from aiogram import Router, Bot 
from aiogram.types import CallbackQuery
from db.mod_messages_crud import ModMessagesCrud 
from core.api_communication import send_approved_post
from core.Redis.scripts import remove_post as redis_remove_post

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("approve:"))
async def approve_handler(callback: CallbackQuery, bot: Bot):
    user_id = str(callback.from_user.id)


    post_id = callback.data.split(":")[1]
    await callback.answer(f"Approved ✅")
    print(f"Approved post: {post_id}")

    messages_that_waits_for_mod = await ModMessagesCrud.get(post_id)

    print("messages_that_waits_for_mod: ", messages_that_waits_for_mod)

    for msg in messages_that_waits_for_mod:
        print(msg)
        await bot.delete_message(chat_id=msg.admin_id, message_id=msg.message_id)

    

    await ModMessagesCrud.delete(post_id)

    await send_approved_post(post_id)
    


@router.callback_query(lambda c: c.data and c.data.startswith("decline:"))
async def decline_handler(callback: CallbackQuery, bot: Bot):
    user_id = str(callback.from_user.id)

    post_id = callback.data.split(":")[1]
    await callback.answer(f"Declined ❌")
    print(f"Declined post: {callback.data}")

    messages_that_waits_for_mod = await ModMessagesCrud.get(post_id)

    for msg in messages_that_waits_for_mod:
        await bot.delete_message(chat_id=msg.admin_id, message_id=msg.message_id)

    await ModMessagesCrud.delete(post_id)
    
    await redis_remove_post(post_id)
