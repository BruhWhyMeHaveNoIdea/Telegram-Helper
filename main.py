import sys
import logging
import asyncio

from aiogram import Dispatcher

from bot.bot import bot
from bot.user.handlers import router as user_router
# from bot.admin.handlers import router as admin_router
import bot.database.database as db


async def main():
    db.create_tables()
    dp = Dispatcher()
    # dp.include_router(admin_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    try:
        asyncio.run(main())
    except Exception as exception:
        print(f"Exit! - {exception}")