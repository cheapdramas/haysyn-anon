from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

def keyboard_mod(post_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve:{post_id}")],
            [InlineKeyboardButton(text="❌ Decline", callback_data=f"decline:{post_id}")]
        ]
    )

    return keyboard

def keyboard_link(url: str,text:str="Link") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=url)],
        ]
    )

    return keyboard

def keyboard_webapp(url: str,text:str="Link") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url))],
        ]
    )

    return keyboard
