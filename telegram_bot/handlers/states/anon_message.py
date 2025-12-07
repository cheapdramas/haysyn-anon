from aiogram import Router, Bot
from aiogram.types import Message
from aiogram.fsm.context import FSMContext 
from states.states import AnonMessageStates
from core.messages import message_anon
from keyboards.reply import keyboard_reply_menu


router = Router()

@router.message(AnonMessageStates.user_id)
async def process_contact(message: Message, state: FSMContext) -> None:
    try:
        user_id = str(message.user_shared.user_id)
    except:
        await message.answer("Не вдалося отримати контакт 🥲", reply_markup=keyboard_reply_menu())

    await state.update_data(user_id = user_id)

    await state.set_state(AnonMessageStates.text)
    await message.answer(f"Чудовий вибір братух\n\nТепер напиши саме повідомлення", reply_markup=keyboard_reply_menu())


@router.message(AnonMessageStates.text)
async def process_text(message: Message, bot: Bot, state: FSMContext) -> None:
    data = await state.get_data()
    user_id = data.get("user_id","")

    await state.clear()

    try:
        msg = message_anon(message.text)
        await bot.send_message(text=msg, chat_id=user_id, parse_mode="HTML")
        await message.answer("Повідомлення успішно відправилось 🚓", reply_markup=keyboard_reply_menu())
    except Exception as e:
        print(str(e))
        await message.answer("Не вдалось відправити повідмолення 🥲",reply_markup=keyboard_reply_menu()) 

