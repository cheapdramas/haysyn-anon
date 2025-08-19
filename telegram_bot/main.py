import asyncio

from aiogram import Bot, Dispatcher
from handlers import router
from core.config import TELEGRAM_BOT_TOKEN


async def main() -> None:
    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    dp = Dispatcher()
    
    dp.include_router(router)

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
