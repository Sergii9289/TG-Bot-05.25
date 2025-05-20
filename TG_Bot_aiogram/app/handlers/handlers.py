from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.filters.state import StateFilter

import app.keyboards as kb
from app.handlers.states import QuizState, GptState, TranslateState, VoiceInputState

from gpt import chat_gpt_service
from app.utils import quiz_prompt, convert_speech_to_text, convert_text_to_speech


from app.handlers.talk import talk_with_pers

router = Router()


#  ------------------------------Обробник сповіщень для 'gpt' та 'talk' --------------------

@router.message(F.text, GptState.waiting_for_answer_gpt)
async def process_user_message(message: Message):
    # Переконуємось, що повідомлення є відповіддю на запит "Введіть ваше повідомлення..."
    if not message.reply_to_message or "Введіть ваше повідомлення для ChatGPT або stop:" not in message.reply_to_message.text:
        return  # Ігноруємо повідомлення, що не є відповіддю на наш запит

    user_message = message.text.strip().lower()  # Очищаємо текст від пробілів і робимо нечутливим до регістру

    if user_message == "stop":
        await message.answer("Повертаємось в головне меню...", reply_markup=kb.menu)
    else:
        prompt = talk_with_pers.get('prompt', "Ти AI-асистент, який відповідає на запити користувачів.")
        print(f'Prompt is: {prompt}')
        response = await chat_gpt_service.send_question(prompt, user_message)
        await message.answer(response)
        await message.answer('Що хочеш зробити далі?', reply_markup=kb.gpt_menu)




# ----------------------------------voice---------------------------------------------------------------

@router.callback_query(F.data == "start_voice_input")
async def start_voice_input(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Підтверджуємо натискання кнопки
    await callback.message.answer("Надішліть голосове повідомлення 🎤")

    # Встановлюємо стан очікування голосового повідомлення
    await state.set_state(VoiceInputState.waiting_for_voice)
    print(f"Стан після встановлення: {await state.get_state()}")


# TODO: бібліотека DeepVoice витягує голосове повідомлення

@router.message(F.voice, StateFilter(VoiceInputState.waiting_for_voice))
async def process_voice_message(message: Message, state: FSMContext):
    current_state = await state.get_state()
    print(f"Стан перед обробкою: {current_state}")

    voice_file_id = message.voice.file_id
    file_info = await message.bot.get_file(voice_file_id)
    file_path = file_info.file_path

    # Завантажуємо голосовий файл
    voice_file = await message.bot.download_file(file_path)

    # Викликаємо функцію для розпізнавання тексту
    text = await convert_speech_to_text(voice_file)

    if not text:
        await message.answer("Не вдалося розпізнати голосове повідомлення. Спробуйте ще раз.")
        return

    await message.answer(f"Розпізнаний текст:\n{text}")

    # Очищаємо стан після обробки
    await state.clear()


