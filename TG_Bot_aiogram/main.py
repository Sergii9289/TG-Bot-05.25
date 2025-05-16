import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from app.handlers import router
from app.database.models import async_main

from dotenv import load_dotenv
import os


load_dotenv(dotenv_path='config.env')
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
