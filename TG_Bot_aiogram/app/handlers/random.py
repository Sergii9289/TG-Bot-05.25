from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile

from ..utils import random_fact
from gpt import chat_gpt_service

import app.keyboards as kb

router = Router()


@router.callback_query(F.data == "random")
async def random_ai(callback: CallbackQuery):
    await callback.answer()  # Підтверджуємо натискання кнопки
    prompt = "Ти AI-асистент, що надає випадкові цікаві факти користувачам."
    fact_prompt = random_fact()  # Генерація промпту для факту
    image = FSInputFile('app/resources/images/random_logo.png')
    # Надсилаємо зображення та повідомлення перед запитом до AI
    await callback.message.answer_photo(photo=image, caption=f"Ось випадковий факт:\n{fact_prompt}")
    # Запит до GPT
    fact = await chat_gpt_service.send_question(prompt, fact_prompt)
    # Надсилаємо відповідь користувачу
    await callback.message.answer(fact)

    await callback.message.answer('Що хочеш зробити далі?', reply_markup=kb.random_menu)
