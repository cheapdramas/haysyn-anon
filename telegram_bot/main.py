import asyncio

from aiogram import Bot, Dispatcher
from handlers import router
from core.config import TELEGRAM_BOT_TOKEN
from db.utils import db_helper
from core.Redis.client import init_redis

async def main() -> None:
    await db_helper.db_init()
    await init_redis()


    bot = Bot(token=TELEGRAM_BOT_TOKEN)
   
    dp = Dispatcher()
    
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":

    asyncio.run(main())
