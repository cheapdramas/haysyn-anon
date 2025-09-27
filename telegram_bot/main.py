import asyncio

from aiogram import Bot, Dispatcher
from handlers import router
from core.config import TELEGRAM_BOT_TOKEN
from db.utils import db_helper


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    db_helper.db_init()
    asyncio.run(main())
