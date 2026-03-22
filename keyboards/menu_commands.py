from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats

async def set_main_menu(bot: Bot):
    menu_commands = [
        BotCommand(command = "start", description="🚀 Тренировка"),
        BotCommand(command = "profile", description="📊 Мои достижения"),
        BotCommand(command = "top", description="🏆 Зал славы"),
        BotCommand(command = "help", description="🆘 Помощь"),
    ]
    await bot.set_my_commands(commands=menu_commands, scope=BotCommandScopeAllPrivateChats())