from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.filters import CommandStart

import app.keyboards as kb
import app.database.requests as rq
import app.text as textfile
from app.main_API import PrivatAPI, MonoAPI
from gpt import chat_gpt_service

import os
from app.utils import make_random_prompt

router = Router()


@router.callback_query(F.data == "random")
async def random_ai(callback: CallbackQuery):
    await callback.answer()  # Підтверджуємо натискання кнопки

    # Запит до GPT
    prompt = "Ти AI-асистент, що допомагає користувачам."

    image_url, user_message = make_random_prompt()

    # image_url = 'app/resources/images/1_cat.jpg'
    # image_url = make_random_prompt()['image_url']
    image = FSInputFile(image_url)

    # Виводимо питання користувачу перед відправкою в ШІ
    await callback.message.answer_photo(photo=image, caption=f"Спитаємо у ШІ:\n{user_message}")

    # Викликаємо GPT без зайвого аргументу
    # answer = await chat_gpt_service.send_question(prompt, user_message)

    # Відправка відповіді користувачу
    # await callback.message.answer(answer)

    await callback.message.answer('Наші подальші дії:', reply_markup=kb.random_menu)


@router.message(CommandStart())  # перша функція після входу в бот /start
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)  # передаємо user.id для перевірки існування user
    await message.answer(textfile.greet.format(name=message.from_user.full_name),
                         reply_markup=kb.menu)


@router.callback_query(F.data == "menu")
async def menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Оберіть дію:", reply_markup=kb.menu)



# @router.callback_query(F.data == "random")
# async def random_ai_image(callback: CallbackQuery):
#     await callback.answer()  # Підтверджуємо натискання кнопки
#
#     # Запит до GPT
#     prompt = "Ти AI-асистент, що допомагає користувачам."
#     print(os.getcwd())  # Виведе поточну папку запуску
#     # Читаємо текстовий файл з промптами
#     with open('app/resources/prompts/message_random.txt', 'r', encoding='utf-8') as file:
#         prompts = file.read().splitlines()  # Отримуємо список рядків
#         line = prompts[0]
#         user_message = line
#     # Читаємо зображення
#     image_path = 'app/resources/images/1_cat.jpg'
#
#     # Виводимо питання користувачу перед відправкою в ШІ
#     await callback.message.answer(f"🔹 **Запит у ШІ:**\n{user_message}")
#
#     # Викликаємо GPT без зайвого аргументу
#     answer = await chat_gpt_service.send_question_with_image(prompt, user_message, image_path)
#
#     # Відправка відповіді користувачу
#     await callback.message.answer(answer)
