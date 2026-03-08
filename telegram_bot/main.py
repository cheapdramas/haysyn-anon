import asyncio
import core.admins as admins
import core.channel as channel
from aiogram import Bot, Dispatcher
from core.Redis.pubsub import listen_to_redis
from handlers import router
from core.config import TELEGRAM_BOT_TOKEN
from db.utils import db_helper
from core.Redis.client import init_redis
from utils.set_commands import set_commands


async def main() -> None:
    await db_helper.db_init()
    await init_redis()

    bot = Bot(token=TELEGRAM_BOT_TOKEN)
    # await set_commands(bot)

    await admins.send_unprocessed_posts(bot)
    await channel.send_unsent_tg_posts_to_channel(bot)
    # create a task that will listen to redis channel
    # and send new posts to admins
    asyncio.create_task(listen_to_redis(bot))

    dp = Dispatcher()
    dp.include_router(router)
    dp.startup.register(set_commands)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
