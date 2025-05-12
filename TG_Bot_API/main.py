import asyncio
import os

from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main

from dotenv import load_dotenv
import os


load_dotenv(dotenv_path='config.env')
tg_token = os.getenv('TG_TOKEN')


async def main():
    await async_main()  # await дозволяє викликати coroutine (асинхронні функції)
    # # та інші об'єкти, які підтримують асинхронні операції
    bot = Bot(token=tg_token)
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнен...')
