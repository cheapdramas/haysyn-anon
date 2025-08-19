
def mod_message(post_data: dict) -> str: 
    """Message in HTML FORMAT"""
    msg = (
        f"<b>📌 {post_data['title']}</b>\n"
        f"<i>{post_data['text']}</i>\n\n"
    )
    return msg
