from aiogram import F, Router
from aiogram.types import CallbackQuery, FSInputFile, ForceReply
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.handlers.states import GptState
from app.utils import talk_person

from ..logger import log_to_file
import logging

router = Router()

talk_with_pers = {}

def reset_talk_with_pers():
    global talk_with_pers
    talk_with_pers.clear()
    print(f'talk_with_pers was reseted: {talk_with_pers}')


@router.callback_query(F.data == "talk")
async def talk(callback: CallbackQuery, state: FSMContext):
    log_to_file("TALK to Famous Person")  # Логуємо виклик функції
    logging.info(f"Користувач {callback.from_user.id} (@{callback.from_user.username}) викликав TALK to Famous Person")
    await callback.answer()  # Підтверджуємо натискання кнопки
    image = FSInputFile('app/resources/images/talk_logo.png')  # Підготовлене зображення
    # Надсилаємо зображення
    await callback.message.answer_photo(photo=image)
    await callback.message.answer('Оберіть з ким спілкуватись:', reply_markup=kb.talk_keyboard)
    # Встановлюємо стан для очікування відповіді користувача
    await state.set_state(GptState.waiting_for_answer_gpt)
    current_state = await state.get_state()
    print(f"Стан встановлено: {current_state}")


@router.callback_query(F.data.in_(talk_person().keys()))
async def process_personality_selection(callback: CallbackQuery):
    personalities = talk_person()
    name = callback.data
    prompt = personalities.get(name)
    global talk_with_pers
    talk_with_pers['prompt'] = prompt

    await callback.message.answer(f"Ви обрали: {name}\n\n{prompt}")
    await callback.message.answer("Введіть ваше повідомлення для ChatGPT або stop:", reply_markup=ForceReply())
