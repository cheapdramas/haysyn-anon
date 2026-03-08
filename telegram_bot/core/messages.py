GREETINGS = """Вітаю! Це офіційний бот платформи <b>Haysyn Anon</b>.

Бот створений для зручного користування сервісом і дає кілька додаткових можливостей:

• Публікуй анонімні пости

• Відстежуй опубліковані тобою пости: /myposts

• Пиши анонімні повідомлення другу (другу приходить повідомлення в бот): /anonmessage

<b>Дотримуйся правил</b> /rules (за бажанням)

Користуйся меню /menu для зручного використання команд
"""

RULES = """
📜
• Не бути свинею
• Не публікуйте особисту інформацію

🔈 У поста 5 лайків на сайті -> пост летить у тг канал @haysynanon

Пости переглядаються адмінами. Якщо пост не відповідає правилам, він не публікується

Зворотній зв'язок: haysynanon@gmail.com
"""

SENT_SUCCESS = "Повідомлення успішно відправилось 🚓"

SENT_FAILURE = "Не вдалось відправити повідмолення 🥲"


def message_post_format(post_data: dict) -> str:
    """Message in HTML FORMAT"""
    msg = (
        f"<b>{post_data['title']}</b>\n"
        f"<i>{post_data['text']}</i>\n\n"
    )
    return msg


def message_anon(text: str):
    msg = (
        f"<b>Тобі прийшло анонімне повідомлення!</b> 💌\n"
        f"<i>{text}</i>\n\n"
    )
    return msg


def message_answer(text: str, receiver_username: str):
    msg = (
        f"<b>Тобі прийшла відповідь від @{receiver_username}!</b> 💌\n"
        f"<i>{text}</i>\n\n"
    )
    return msg
