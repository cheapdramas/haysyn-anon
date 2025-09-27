from asyncio import start_server
from aiogram import Router, Bot 
from aiogram.types import CallbackQuery
from core.websocket_client import ws_tasks, manage_post
from schemas.post import PostModStatus as status

from db.mod_messages_crud import ModMessagesCrud 


router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("approve:"))
async def approve_handler(callback: CallbackQuery, bot: Bot):
    user_id = str(callback.from_user.id)

    if not ws_tasks.get(user_id, None):
        await callback.answer(f"/mod: Підключись до вебсокету")
        return


    post_id = callback.data.split(":")[1]
    print(callback.data)
    await callback.answer(f"Approved ✅")
    print(f"Approved post: {post_id}")

    await manage_post(user_id, str(post_id), "approved")

    messages_that_waits_for_mod = ModMessagesCrud.get(post_id)

    for msg in messages_that_waits_for_mod:
        await bot.delete_message(chat_id=msg.admin_id, message_id=msg.message_id)

    

    ModMessagesCrud.delete(post_id)


@router.callback_query(lambda c: c.data and c.data.startswith("decline:"))
async def decline_handler(callback: CallbackQuery, bot: Bot):
    user_id = str(callback.from_user.id)

    if not ws_tasks.get(user_id, None):
        await callback.answer(f"/mod: Підключись до вебсокету")
        return



    post_id = callback.data.split(":")[1]
    await callback.answer(f"Declined ❌")
    print(f"Declined post: {callback.data}")


    await manage_post(user_id, str(post_id), "declined")


    messages_that_waits_for_mod = ModMessagesCrud.get(post_id)

    for msg in messages_that_waits_for_mod:
        await bot.delete_message(chat_id=msg.admin_id, message_id=msg.message_id)

    ModMessagesCrud.delete(post_id)
