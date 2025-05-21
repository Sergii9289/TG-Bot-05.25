from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, ForceReply
from aiogram.fsm.context import FSMContext

from app.handlers.states import GptState
from .talk import reset_talk_with_pers

from ..logger import log_to_file
import logging


router = Router()


@router.callback_query(F.data == "gpt")
async def chat_gpt_interface(callback: CallbackQuery, state: FSMContext):
    log_to_file("chat_gpt_interface")  # Логуємо виклик функції
    logging.info(f"Користувач {callback.from_user.id} (@{callback.from_user.username}) викликав ChatGPT інтерфейс")
    reset_talk_with_pers()
    await callback.answer()  # Підтверджуємо натискання кнопки
    global talk_with_pers
    talk_with_pers = {}
    image = FSInputFile('app/resources/images/gpt_logo.png')  # Підготовлене зображення
    # Надсилаємо зображення
    await callback.message.answer_photo(photo=image, caption="Запит до ChatGPT...")
    await callback.message.answer("Введіть ваше повідомлення для ChatGPT або stop:", reply_markup=ForceReply())
    # Встановлюємо стан для очікування відповіді користувача
    await state.set_state(GptState.waiting_for_answer_gpt)
    current_state = await state.get_state()
    print(f"Стан встановлено: {current_state}")


@router.callback_query(F.data == "gpt_next")
async def chat_gpt_interface_next(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Підтверджуємо натискання кнопки
    await callback.message.answer("Введіть ваше повідомлення для ChatGPT або stop:", reply_markup=ForceReply())
    # Повторно встановлюємо стан для отримання нової відповіді
    await state.set_state(GptState.waiting_for_answer_gpt)
