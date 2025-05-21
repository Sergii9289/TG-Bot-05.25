from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from gpt import chat_gpt_service

from ..logger import log_to_file
import logging

router = Router()


@router.callback_query(F.data == "recomendations")
async def recomendations(callback: CallbackQuery):
    log_to_file("RECOMENDATIONS")  # Логуємо виклик функції
    logging.info(f"Користувач {callback.from_user.id} (@{callback.from_user.username}) викликав RECOMENDATIONS")
    await callback.answer()  # Підтверджуємо натискання кнопки
    image = FSInputFile('app/resources/images/recomend_logo.png')  # Підготовлене зображення
    # Надсилаємо зображення
    await callback.message.answer_photo(photo=image)
    await callback.message.answer('Оберіть тему:', reply_markup=kb.recomend_menu)


@router.callback_query(F.data.startswith("recomendations_handler"))
async def recomendations_handler(callback: CallbackQuery, state: FSMContext):
    _, topic = callback.data.split(":")  # Отримуємо мову перекладу
    print(topic)

    await callback.message.answer(f'Оберіть жанр для категорії: {topic.capitalize()}',
                                  reply_markup=getattr(kb, f'recomend_{topic}_menu'))


@router.callback_query(F.data.startswith("recomend_movies_handler"))
async def recomend_movies_handler(callback: CallbackQuery, state: FSMContext):
    _, topic = callback.data.split(":")  # Отримуємо жанр

    prompt = f"Назви 5 фільмів у жанрі {topic} (тільки назви і рік виробництва без опису) українською мовою."

    response = await chat_gpt_service.send_question(prompt, "")

    # Переконаємося, що текст не перевищує ліміт 4096 символів
    if len(response) > 1000:
        response = response[:1000] + "..."

    await callback.message.answer(f"От 5 фальмів в жанрі {topic}:\n{response}")


@router.callback_query(F.data.startswith("recomend_books_handler"))
async def recomend_books_handler(callback: CallbackQuery, state: FSMContext):
    _, topic = callback.data.split(":")  # Отримуємо жанр

    prompt = f"Назви 5 книг у жанрі {topic} (тільки назви і рік виробництва без опису) українською мовою."

    response = await chat_gpt_service.send_question(prompt, "")

    # Переконаємося, що текст не перевищує ліміт 4096 символів
    if len(response) > 1000:
        response = response[:1000] + "..."

    await callback.message.answer(f"От 5 книг в жанрі {topic}:\n{response}")


@router.callback_query(F.data.startswith("recomend_music_handler"))
async def recomend_music_handler(callback: CallbackQuery, state: FSMContext):
    _, topic = callback.data.split(":")  # Отримуємо жанр

    prompt = f"Назви 5 виконавців у жанрі {topic} (тільки назви і кращу пісню)."

    response = await chat_gpt_service.send_question(prompt, "")

    # Переконаємося, що текст не перевищує ліміт 4096 символів
    if len(response) > 1000:
        response = response[:1000] + "..."

    await callback.message.answer(f"От 5 книг в жанрі {topic}:\n{response}")