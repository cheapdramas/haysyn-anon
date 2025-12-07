from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

from core.config import WEBSITE_URL_BASE

def keyboard_mod(post_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve:{post_id}")],
            [InlineKeyboardButton(text="❌ Decline", callback_data=f"decline:{post_id}")]
        ]
    )

    return keyboard


def keyboard_continue_viewing_posts(offset: int, get_from_channel:bool) -> InlineKeyboardMarkup:
    callback_data = f"continue_viewing_posts_{'channel' if get_from_channel else 'website'}:{offset}"

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Завантажити ще", callback_data=callback_data)]
        ]
    )

    return keyboard


def keyboard_link(url: str, text: str = "Link") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, url=url)],
        ]
    )

    return keyboard

def keyboard_webapp(url: str = WEBSITE_URL_BASE,text:str="Link") -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text=text, web_app=WebAppInfo(url=url))],
        ]
    )

    return keyboard
