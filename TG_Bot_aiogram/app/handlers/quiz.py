from aiogram import F, Router, types
from aiogram.types import CallbackQuery, FSInputFile, ForceReply
from aiogram.fsm.context import FSMContext

from app.handlers.states import QuizState
import app.keyboards as kb
from app.utils import quiz_prompt

from gpt import chat_gpt_service

from ..logger import log_to_file
import logging

router = Router()


@router.callback_query(F.data == "quiz")
async def quiz(callback: CallbackQuery):
    log_to_file("QUIZ")  # Логуємо виклик функції
    logging.info(f"Користувач {callback.from_user.id} (@{callback.from_user.username}) викликав QUIZ")
    await callback.answer()  # Підтверджуємо натискання кнопки
    image = FSInputFile('app/resources/images/quiz_logo.png')  # Підготовлене зображення
    # Надсилаємо зображення
    await callback.message.answer_photo(photo=image)
    await callback.message.answer('Оберіть тему:', reply_markup=kb.quiz_menu)


@router.callback_query(F.data.startswith("quiz_handler"))
async def quiz_handler(callback: CallbackQuery, state: FSMContext):
    _, topic = callback.data.split(":")  # Отримуємо тему

    await callback.message.answer(f"Ви обрали тему: {topic.capitalize()}")
    await callback.answer()

    prompt = quiz_prompt(topic)
    print(prompt)
    question = await chat_gpt_service.send_question(prompt, "")

    await callback.message.answer(f"Ось ваше запитання:\n\n{question}", reply_markup=ForceReply())

    # Зберігаємо запитання у стані
    await state.update_data(question=question)
    await state.set_state(QuizState.waiting_for_answer_quiz)
    current_state = await state.get_state()
    print(f"Поточний стан: {current_state}")


@router.message(F.text, QuizState.waiting_for_answer_quiz)
async def quiz_user_answer(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    print(f"Стан при отриманні відповіді: {current_state}")  # Перевірка стану

    # Отримуємо збережене запитання
    user_data = await state.get_data()
    question = user_data.get("question", "Запитання не знайдено.")
    user_answer = message.text

    print(f"Запитання: {question}")
    print(f"Відповідь користувача: {user_answer}")

    # Передаємо **і запитання, і відповідь** в ChatGPT
    feedback = await chat_gpt_service.send_question(
        f"Оціни відповідь користувача на запитання квізу: \"{question}\". Чи правильна вона? Дай пояснення.",
        user_answer
    )

    await message.answer(f"Оцінка вашої відповіді:\n\n{feedback}")

    # Скидаємо стан після отримання відповіді
    await state.clear()
    await message.answer('Що хочеш зробити далі?', reply_markup=kb.quiz_next_menu)