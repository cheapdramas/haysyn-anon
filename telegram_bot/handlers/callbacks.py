from aiogram import Router, Bot
from aiogram.fsm.context import FSMContext
from aiogram.methods import delete_message
from aiogram.types import CallbackQuery
from core.users import myposts
from db.crud import ModMessagesCrud, ChanellMessagesCrud
from core.api_communication import send_approved_post
from core.Redis.scripts import RawPost
from core.config import CHANNEL_NAME, WEBSITE_URL_BASE
from keyboards import reply
from keyboards.inline import keyboard_link
import asyncio

from states.states import AnonMessageStates

router = Router()


@router.callback_query(lambda c: c.data and c.data.startswith("cancel"))
async def cancel_handler(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await state.clear()
    await callback.message.answer("🐶", reply_markup=reply.keyboard_reply_menu())


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
        
        await RawPost.remove("post:" + post_id)


        await callback.answer(f"Declined ❌")
        print(f"Declined post: {callback.data}")

    except Exception as e:
        await callback.answer(f"Problem occured 😔")
        print("Decline post error: ", str(e))


# handle continue viewing posts
@router.callback_query(lambda c: c.data and c.data.startswith("continue_viewing_posts:"))
async def continue_view_posts_button_handler(callback: CallbackQuery, bot: Bot):
    callback_parts = callback.data.split(':')
    offset = int(callback_parts[1])
    print(offset)
    view_from = callback_parts[0].split('_')[-1]    
    print("view_from: ", view_from)

    if view_from == "channel":
        asyncio.create_task(myposts(callback.message, bot, offset, user_id=callback.from_user.id, load_from_website=False))
    elif view_from == "website":
        await myposts(callback.message, bot, offset, load_from_website=True) 


    await callback.message.delete()


@router.callback_query(lambda c: c.data and c.data.startswith("answer_message:"))
async def answer_message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    await callback.message.answer("Напишіть відповідь...")

    # await bot.delete_message(chat_id=callback.from_user.id, message_id=int(callback.message.message_id))
    anon_message_id = callback.message.message_id
    sender_user_id = callback.data.split(":")[1]

    await state.clear()
    await state.update_data(sender_user_id=sender_user_id)
    await state.update_data(anon_message_id=anon_message_id)
    await state.set_state(AnonMessageStates.answer)


@router.callback_query(lambda c: c.data and c.data.startswith("report:"))
async def report_message(callback: CallbackQuery, bot: Bot, state: FSMContext):
    pass

