from aiogram import Router, Bot, F
from aiogram.enums import parse_mode
from aiogram.types import Message, inline_keyboard_markup, FSInputFile
from aiogram.fsm.context import FSMContext
from core.config import VOICE_MESSAGES_PATH
from core.voice import apply_voice_filter, handle_voice_message
from states.states import AnonMessageStates
from core.messages import message_anon as msg_anon, message_answer, SENT_FAILURE, SENT_SUCCESS
from keyboards.reply import keyboard_reply_menu
from keyboards.inline import keyboard_anon_message
import asyncio


router = Router()

# User sharing contact


@router.message(AnonMessageStates.user_id)
async def process_contact(message: Message, state: FSMContext) -> None:
    try:
        user_id = str(message.user_shared.user_id)
    except:
        await message.answer("Не вдалося отримати контакт 🥲", reply_markup=keyboard_reply_menu())
        return

    await state.update_data(user_id=user_id)

    await state.set_state(AnonMessageStates.message)
    await message.answer(f"Чудовий вибір братух\n\nТепер напиши саме повідомлення", reply_markup=keyboard_reply_menu())

# handle message text


@router.message(AnonMessageStates.message, F.text)
async def process_text(message: Message, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    receiver_user_id = data.get("user_id", "")

    await state.clear()

    try:
        # Надсилаємо отримувачу повідомлення
        msg = msg_anon(message.text)
        await bot.send_message(text=msg, chat_id=receiver_user_id, parse_mode="HTML", reply_markup=keyboard_anon_message(sender_user_id=message.from_user.id))
        await message.answer(SENT_SUCCESS, reply_markup=keyboard_reply_menu())

    except Exception as e:
        print(str(e))
        await message.answer(SENT_FAILURE, reply_markup=keyboard_reply_menu())


@router.message(AnonMessageStates.message, F.voice)  # handle voice message
async def process_voice(message: Message, bot: Bot, state: FSMContext) -> None:
    asyncio.create_task(handle_voice_message(
        message,
        bot,
        state
    ))

# Reciever answers the message


@router.message(AnonMessageStates.answer)
async def process_answer(message: Message, bot: Bot, state: FSMContext):

    state_data = await state.get_data()
    sender_user_id = state_data.get("sender_user_id", "")
    anon_message_id = state_data.get("anon_message_id", "")
    answer_text = message.text
    receiver_username = message.from_user.username

    await state.clear()

    try:
        msg = message_answer(answer_text, receiver_username)
        await bot.send_message(text=msg, chat_id=int(sender_user_id), parse_mode="HTML")

        # edit anon message: remove answer button
        await bot.edit_message_reply_markup(chat_id=message.from_user.id, message_id=anon_message_id, reply_markup=keyboard_anon_message(sender_user_id, False))

        await message.answer(SENT_SUCCESS)

    except Exception as e:
        print(str(e))
        await message.answer(SENT_FAILURE, reply_markup=keyboard_reply_menu())
