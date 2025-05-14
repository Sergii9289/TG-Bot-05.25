import asyncio

from aiogram import Bot, Dispatcher

from app.handlers import router
from app.database.models import async_main

from dotenv import load_dotenv
import os

# import openai
# import httpx

load_dotenv(dotenv_path='config.env')
TG_TOKEN = os.getenv('TG_TOKEN')
# AI_TOKEN = os.getenv('AI_TOKEN')


# class ChatGptService:
#     def __init__(self, token):
#         self.client = openai.OpenAI(
#             api_key=AI_TOKEN, http_client=httpx.Client(proxy="http://18.199.183.77:49232")
#         )
#         self.message_list = []
#
#     async def send_question(self, prompt_text: str, message_text: str) -> str:
#         self.message_list.clear()
#         self.message_list.append({"role": "system", "content": prompt_text})
#         self.message_list.append({"role": "user", "content": message_text})
#
#         completion = self.client.chat.completions.create(
#             model="gpt-4o", messages=self.message_list, max_tokens=300, temperature=0.9
#         )
#         return completion.choices[0].message.content
#
# # Ініціалізація GPT сервісу
# chat_gpt_service = ChatGptService(AI_TOKEN)


async def main():
    await async_main()

    bot = Bot(token=TG_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

    # # Ініціалізація GPT сервісу
    # chat_gpt_service = ChatGptService(AI_TOKEN)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Бот вимкнен...')
