from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, KeyboardButtonRequestChat, KeyboardButtonRequestUser
from core.config import WEBSITE_URL_BASE

buttons = {
    "web": "👤 Написати пост",
    "myposts": "📁 Мої пости",
    "anonmessage": "📨 Анонімно написати другу",
    "rules": "📜 Правила",
    "help": "🚑 Допомога"
}

def keyboard_reply_menu() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=buttons["web"])],
            [KeyboardButton(text=buttons["myposts"])],
            [KeyboardButton(text=buttons["anonmessage"])],
            [KeyboardButton(text=buttons["rules"])],
            [KeyboardButton(text=buttons["help"])]
        ],
        # resize_keyboard=True,
        one_time_keyboard=False,
        # input_field_placeholder="Оберіть дію…"
    )
    return keyboard

def keyboard_reply_request_chat() -> ReplyKeyboardMarkup:
    request_chat_button = KeyboardButtonRequestUser(request_id=123)
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Виберіть контакт", request_user=request_chat_button)],
        ],
        # resize_keyboard=True,
        one_time_keyboard=True,
        # input_field_placeholder="Оберіть дію…"
    )
    return keyboard 

