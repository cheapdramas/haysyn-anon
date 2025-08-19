from asyncio import start_server
from aiogram import Router
from aiogram.types import CallbackQuery
from core.websocket_client import ws_tasks, manage_post
from schemas.post import PostStatus as status

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("approve:"))
async def approve_handler(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    if not ws_tasks.get(user_id, None):
        await callback.answer(f"/mod: Підключись до вебсокету")
        return


    post_id = callback.data.split(":")[1]
    print(callback.data)
    await callback.answer(f"Approved ✅")
    print(f"Approved post: {post_id}")

    await manage_post(user_id, str(post_id), "approved")


    await callback.message.delete()


@router.callback_query(lambda c: c.data and c.data.startswith("decline:"))
async def decline_handler(callback: CallbackQuery):
    user_id = str(callback.from_user.id)

    if not ws_tasks.get(user_id, None):
        await callback.answer(f"/mod: Підключись до вебсокету")
        return



    post_id = callback.data.split(":")[1]
    await callback.answer(f"Declined ❌")
    print(f"Declined post: {callback.data}")


    await manage_post(user_id, str(post_id), "declined")

    await callback.message.delete()
