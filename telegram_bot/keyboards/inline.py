from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo,ReplyKeyboardMarkup, KeyboardButton

def keyboard_mod(post_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve:{post_id}")],
            [InlineKeyboardButton(text="❌ Decline", callback_data=f"decline:{post_id}")]
        ]
    )

    return keyboard


def keyboard_webapp()  -> InlineKeyboardMarkup:
    web_button = InlineKeyboardButton(
        text="Anon",
        web_app=WebAppInfo(url="https://extracapsular-earline-perspectiveless.ngrok-free.dev/")
    )

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[web_button]]  # одна кнопка в одной строке
    )

    return keyboard
