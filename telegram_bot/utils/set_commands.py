from aiogram import Bot, Dispatcher, types


async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Запустити бота"),
        types.BotCommand(command="/help", description="Що вміє бот"),
        types.BotCommand(command="/myposts", description="Показує ваші авторські пости з каналу"),
    ]
    await bot.set_my_commands(commands, scope=types.BotCommandScopeAllGroupChats())
