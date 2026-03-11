import asyncio
import os
from environs import Env

from aiogram import Bot, Dispatcher


from database.db import DatabaseBot
from handlers import bot_handlers
from keyboards.menu_commands import set_main_menu


async def main():
    env = Env()
    env.read_env()
    bot_token = env("BOT_TOKEN")

    bot = Bot(token=bot_token)
    dp = Dispatcher()

    user_db = DatabaseBot()
    await user_db.connect_with_database()
    bot_handlers.user_db = user_db

    await set_main_menu(bot)

    dp.include_router(bot_handlers.user_router)
    try:
        await dp.start_polling(bot)
    finally:
        await user_db.close_connection()

    await user_db.close_connection()


if __name__ == "__main__":
    asyncio.run(main())