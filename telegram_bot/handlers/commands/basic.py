from aiogram import Router, Bot, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from keyboards.inline import keyboard_webapp
import keyboards.reply as reply
from core.config import WEBSITE_URL_BASE 
from utils.set_commands import set_commands
from core.messages import GREETINGS, RULES

router = Router()

@router.message(Command("start"))
async def start_command_handler(message: Message, bot: Bot):
    user_id = str(message.chat.id)
    await bot.set_chat_menu_button(
        chat_id= int(user_id),
        menu_button = {
            "type": "web_app",
            "text": "Сайт",
            "web_app": {"url":WEBSITE_URL_BASE} 
        }
    )

    await message.answer(GREETINGS,reply_markup=reply.keyboard_reply_menu(), parse_mode="HTML")

@router.message(F.text==reply.buttons["cancel"])
@router.message(Command("cancel"))
async def cancel_command_handler(message: Message, bot: Bot, state: FSMContext):
    await state.clear()
    await message.answer("🐶", reply_markup=reply.keyboard_reply_menu())

@router.message(Command("menu"))
async def menu_command_handler(message: Message, bot: Bot) -> None:
    await message.answer("😜", reply_markup=reply.keyboard_reply_menu())


@router.message(Command("rules"))
@router.message(F.text==reply.buttons["rules"])
async def rules_command_handler(message: Message, bot: Bot) -> None:
    await message.answer(RULES)

@router.message(Command("help"))
@router.message(F.text==reply.buttons["help"])
async def help_command_handler(message: Message, bot: Bot) -> None:
    await message.answer("ну тот помощ короче")


@router.message(Command("web"))
@router.message(F.text==reply.buttons["web"])
async def web_command_handler(message: Message, bot: Bot) -> None:
    await message.answer("⬇️⬇️⬇️", reply_markup=keyboard_webapp(text="Написати пост"))

