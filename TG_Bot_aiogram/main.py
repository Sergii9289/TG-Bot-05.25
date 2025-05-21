import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import router
from app.database.models import async_main

from dotenv import load_dotenv
import os
import logging

logging.getLogger("aiogram").setLevel(logging.WARNING)
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

load_dotenv()
TG_TOKEN = os.getenv('TG_TOKEN')


async def main():
    await async_main()

    bot = Bot(token=TG_TOKEN)
    storage = MemoryStorage()
    dp = Dispatcher(storage=storage)
    dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнен...')
