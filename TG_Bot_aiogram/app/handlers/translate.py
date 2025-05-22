from aiogram import F, Router
from aiogram.types import CallbackQuery, Message, ForceReply
from aiogram.fsm.context import FSMContext

from app.handlers.states import TranslateState
import app.keyboards as kb
import app.database.requests as rq
from gpt import chat_gpt_service

from ..logger import log_to_file
import logging

router = Router()

@router.callback_query(F.data == "translate")
async def menu_callback(callback: CallbackQuery):
    log_to_file("TRANSLATE")  # Логуємо виклик функції
    logging.info(f"Користувач {callback.from_user.id} (@{callback.from_user.username}) викликав TRANSLATE")

    await rq.update_user_activity(callback.from_user.id)  # Оновлюємо активність у БД

    await callback.answer()
    await callback.message.edit_text("Оберіть мову, на яку перекласти:", reply_markup=kb.translate_menu)


@router.callback_query(F.data.startswith("translate_handler"))
async def translate_handler(callback: CallbackQuery, state: FSMContext):
    _, topic = callback.data.split(":")  # Отримуємо мову перекладу
    print(topic)

    await callback.message.answer(f"Перекласти на мову: {topic.capitalize()}")
    await callback.answer()

    # Зберігаємо тему перекладу в стані
    await state.update_data(target_language=topic)

    # Запитуємо текст для перекладу
    await callback.message.answer("Введіть текст для перекладу:", reply_markup=ForceReply())

    # Встановлюємо стан очікування введення тексту
    await state.set_state(TranslateState.waiting_for_text)


@router.message(F.text, TranslateState.waiting_for_text)
async def process_translation(message: Message, state: FSMContext):
    user_data = await state.get_data()
    target_language = user_data.get("target_language", "українська")

    user_text = message.text.strip()
    print(f"Перекладаємо текст '{user_text}' на '{target_language}'")

    # Формуємо промпт для AI
    prompt = f"Переклади наступний текст на {target_language}: {user_text}"

    response = await chat_gpt_service.send_question(prompt, "")

    await message.answer(f"Переклад:\n\n{response}")

    # Очищаємо стан після перекладу
    await state.clear()
    await message.answer('Що хочеш зробити далі?', reply_markup=kb.translate_next_menu)