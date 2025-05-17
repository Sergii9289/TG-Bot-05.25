from aiogram import F, Router, types
from aiogram.types import Message, CallbackQuery, FSInputFile, ForceReply
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

import app.keyboards as kb
import app.database.requests as rq
import app.text as textfile
from gpt import chat_gpt_service
from app.utils import random_fact, talk_person, quiz_prompt

router = Router()

talk_with_pers = {}


class QuizState(StatesGroup):
    waiting_for_answer_quiz = State()


class GptState(StatesGroup):
    waiting_for_answer_gpt = State()


class TranslateState(StatesGroup):
    waiting_for_text = State()


@router.message(CommandStart())  # перша функція після входу в бот /start
async def cmd_start(message: Message):
    await rq.set_user(message.from_user.id)  # передаємо user.id для перевірки існування user
    await message.answer(textfile.greet.format(name=message.from_user.full_name),
                         reply_markup=kb.menu)


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


@router.callback_query(F.data == "gpt")
async def chat_gpt_interface(callback: CallbackQuery, state: FSMContext):
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


@router.callback_query(F.data == "talk")
async def talk(callback: CallbackQuery, state: FSMContext):
    await callback.answer()  # Підтверджуємо натискання кнопки
    image = FSInputFile('app/resources/images/talk_logo.png')  # Підготовлене зображення
    # Надсилаємо зображення
    await callback.message.answer_photo(photo=image)
    await callback.message.answer('Оберіть з ким спілкуватись:', reply_markup=kb.talk_keyboard)
    # Встановлюємо стан для очікування відповіді користувача
    await state.set_state(GptState.waiting_for_answer_gpt)
    current_state = await state.get_state()
    print(f"Стан встановлено: {current_state}")


@router.callback_query(F.data == "quiz")
async def quiz(callback: CallbackQuery):
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


@router.callback_query(F.data == "translate")
async def menu_callback(callback: CallbackQuery):
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


@router.callback_query(F.data == "menu")
async def menu_callback(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text("Оберіть дію:", reply_markup=kb.menu)


@router.callback_query()
async def process_personality_selection(callback: CallbackQuery):
    personalities = talk_person()
    name = callback.data
    prompt = personalities.get(name)
    global talk_with_pers
    talk_with_pers['prompt'] = prompt

    await callback.message.answer(f"Ви обрали: {name}\n\n{prompt}")
    await callback.message.answer("Введіть ваше повідомлення для ChatGPT або stop:", reply_markup=ForceReply())
