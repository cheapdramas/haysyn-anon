from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def keyboard_mod(post_id: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="✅ Approve", callback_data=f"approve:{post_id}")],
            [InlineKeyboardButton(text="❌ Decline", callback_data=f"decline:{post_id}")]
        ]
    )

    return keyboard

