from aiogram import Bot
from aiogram.types import BotCommand,BotCommandScopeDefault

async def bot_commands(bot: Bot):
    commands = [
        BotCommand(
            command='start',
            description='Продолжите фразу: Сегодня я хочу...'
        )
    ]

    await bot.set_my_commands(commands, BotCommandScopeDefault())