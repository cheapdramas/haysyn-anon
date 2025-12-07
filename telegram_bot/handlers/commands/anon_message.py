from aiogram import Router, Bot, F
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.reply import buttons as reply_buttons, keyboard_reply_request_chat 
from aiogram.fsm.context import FSMContext 
from states.states import AnonMessageStates

router = Router()

@router.message(Command("anonmessage"))
@router.message(F.text == reply_buttons["anonmessage"])
async def start_command_handler(message: Message, state: FSMContext) -> None:
    await state.set_state(AnonMessageStates.user_id)
    await message.answer("Виберіть контакт", reply_markup=keyboard_reply_request_chat())

